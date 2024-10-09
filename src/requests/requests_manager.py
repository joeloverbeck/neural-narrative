import logging
from typing import Optional, Any

import requests
import runpod

from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class RequestsManager:
    def __init__(self, filesystem_manager: Optional[FilesystemManager] = None):

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def _get_runpod_endpoint_url(self) -> Optional[str]:
        # Could be that the endpoint ain't even running.
        runpod.api_key = self._filesystem_manager.load_runpod_secret_key()

        # Fetching all available endpoints
        pods = runpod.get_pods()

        # At this point, pods could be an empty list.

        if not pods:
            return None

        xtts_pod = pods[0]
        pod_id = xtts_pod["id"]

        # At this point it could be that the pod is not running.
        if pod_id and not xtts_pod["desiredStatus"].lower() == "running":
            logger.warning(f"There's a pod, but it isn't running: {xtts_pod}")
            return None

        return f"https://{pod_id}-8020.proxy.runpod.net"

    def get_available_speakers(self) -> dict[str, Any]:
        # Code to request and return the list of available models
        try:
            xtts_url = self._get_runpod_endpoint_url()

            if not xtts_url:
                return {}

            # At this point, we should be able to get a list of speakers.
            response_speakers = requests.get(f"{xtts_url}/speakers_list")

            if response_speakers.status_code == 200:
                all_speakers = response_speakers.json()
                current_language_speakers = all_speakers.get("en", {}).get(
                    "speakers", []
                )
                return current_language_speakers
            else:
                return {}
        except requests.exceptions.ConnectionError as e:
            logging.warning(e)
            return {}

    def get_xtts_endpoint(self) -> Optional[str]:
        # Could be that there's no pod or that it isn't running yet.
        xtts_pod = self._get_runpod_endpoint_url()

        if not xtts_pod:
            return None

        return f"{xtts_pod}/tts_to_audio/"
