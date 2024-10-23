from pydantic import BaseModel, Field


class PlotBlueprint(BaseModel):
    plot_blueprint: str = Field(
        ...,
        description=(
            "A magnificent plot blueprint for a full story. Follow the provided instructions."
        ),
    )
