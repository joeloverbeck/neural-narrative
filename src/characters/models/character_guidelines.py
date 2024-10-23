from pydantic import BaseModel, Field, conlist


class CharacterGuidelines(BaseModel):
    guidelines: conlist(str, min_length=3, max_length=3) = Field(
        ...,
        description=(
            "A list of three guidelines for creating interesting characters based on the provided "
            "combination of places. Each guideline should be about 4-5 sentences. Follow "
            "the provided instructions for what elements the guideline should include."
        ),
    )
