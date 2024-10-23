from pydantic import BaseModel, Field, conlist


class Dilemmas(BaseModel):
    dilemmas: conlist(str, min_length=3, max_length=3) = Field(
        ...,
        description=(
            "A list of three intriguing moral and ethical dilemmas that could stem "
            "from the provided information. Follow the provided instructions."
        ),
    )
