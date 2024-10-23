from pydantic import BaseModel, Field, conlist


class PlotTwists(BaseModel):
    plot_twists: conlist(str, min_length=3, max_length=3) = Field(
        ...,
        description=(
            "A list of three captivating plot twists that could dramatically alter the storyline. "
            "Follow the provided instructions."
        ),
    )
