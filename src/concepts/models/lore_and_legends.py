from pydantic import BaseModel, Field


class LoreAndLegends(BaseModel):
    lore_or_legend: str = Field(
        ...,
        description=(
            "A fascinating piece of world lore or legend. "
            "Follow the provided instructions."
        ),
    )
