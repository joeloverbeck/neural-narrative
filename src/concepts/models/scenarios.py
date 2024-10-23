from pydantic import BaseModel, Field, conlist


class Scenarios(BaseModel):
    scenarios: conlist(str, min_length=3, max_length=3) = Field(
        ...,
        description=(
            "A list of three very interesting and intriguing scenarios that could stem from the information provided, "
            "as per the above instructions."
        ),
    )
