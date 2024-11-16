import logging
from enum import Enum
from typing import List, Optional, Dict, Any

import chromadb
from chromadb.api.types import IncludeEnum  # noqa
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from src.base.validators import validate_non_empty_string
from src.databases.abstracts.database import Database
from src.filesystem.path_manager import PathManager

logger = logging.getLogger(__name__)


class ChromaDbDatabase(Database):

    class DataType(Enum):
        CHARACTER_IDENTIFIER = "character_identifier"
        FACT = "fact"
        MEMORY = "memory"

    def __init__(
        self, playthrough_name: str, path_manager: Optional[PathManager] = None
    ):
        validate_non_empty_string(playthrough_name, "playthrough_name")

        self._path_manager = path_manager or PathManager()

        # Initialize Chroma client with per-playthrough persistent storage.
        self._chroma_client = chromadb.PersistentClient(
            path=self._path_manager.get_database_path(playthrough_name).as_posix(),
            settings=Settings(anonymized_telemetry=False, allow_reset=True),
        )

        # Use a single collection for all data types within the playthrough
        self._collection = self._chroma_client.get_or_create_collection(
            name="playthrough_data"
        )

        self._embedding_function = embedding_functions.DefaultEmbeddingFunction()

    def _determine_where_clause(
        self, data_type: str, character_identifier: Optional[str] = None
    ) -> Dict[str, Any]:
        where_clause = {"type": data_type}
        if character_identifier:
            # Must use the "$and" operator.
            where_clause = {
                "$and": [
                    where_clause,
                    {self.DataType.CHARACTER_IDENTIFIER.value: character_identifier},
                ]
            }

        return where_clause

    def _insert_data(
        self,
        text: str,
        data_type: str,
        character_identifier: Optional[str] = None,
        data_id: Optional[str] = None,
    ):
        if not data_id:
            data_id = str(self._collection.count())

        metadata = {"type": data_type}
        if character_identifier:
            metadata[self.DataType.CHARACTER_IDENTIFIER.value] = character_identifier

        # Upsert updates existing items, or adds them if they don't exist.
        # If an id is not present in the collection, the corresponding items will
        # be created as per add. Items with existing ids will be updated as per update.
        self._collection.upsert(
            ids=[data_id],
            documents=[text],
            embeddings=self._embedding_function([text]),
            metadatas=[metadata],
        )

    def _retrieve_data(
        self,
        query_text: str,
        data_type: str,
        character_identifier: Optional[str] = None,
        top_k: int = 5,
    ) -> List[Dict[str, str]]:
        results = self._collection.query(
            query_embeddings=self._embedding_function([query_text]),
            n_results=top_k,
            where=self._determine_where_clause(data_type, character_identifier),
            include=[IncludeEnum.documents],
        )

        # Safely extract ids and documents, defaulting to empty lists if not present
        ids_nested = results.get("ids", [])
        documents_nested = results.get("documents", [])

        if not ids_nested or not documents_nested:
            return []

        # Assuming a single query, access the first sublist
        ids = ids_nested[0]
        documents = documents_nested[0]

        # Pair each id with its corresponding document
        paired_results = [
            {"id": id_, "document": doc} for id_, doc in zip(ids, documents)
        ]

        return paired_results

    def insert_fact(self, fact: str) -> None:
        self._insert_data(fact, data_type=self.DataType.FACT.value)

    def insert_memory(
        self, character_identifier: str, memory: str, data_id: Optional[str] = None
    ) -> None:
        self._insert_data(
            memory,
            data_type=self.DataType.MEMORY.value,
            character_identifier=character_identifier,
            data_id=data_id,
        )

    def retrieve_facts(self, query_text: str, top_k: int = 5) -> List[Dict[str, str]]:
        return self._retrieve_data(
            query_text, data_type=self.DataType.FACT.value, top_k=top_k
        )

    def retrieve_memories(
        self, character_identifier: str, query_text: str, top_k: int = 5
    ) -> List[Dict[str, str]]:
        return self._retrieve_data(
            query_text,
            data_type=self.DataType.MEMORY.value,
            character_identifier=character_identifier,
            top_k=top_k,
        )
