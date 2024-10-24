from pydantic import BaseModel, Field


class AmbientNarration(BaseModel):
    ambient_narration: str = Field(
        ...,
        description=(
            "The three or four sentences of ambient narration that enhances the scene without interfering with the ongoing dialogue. Follow the provided instructions."
        ),
    )
