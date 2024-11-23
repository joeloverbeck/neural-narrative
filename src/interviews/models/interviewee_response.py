from pydantic import BaseModel, Field


class IntervieweeResponse(BaseModel):
    interviewee_response: str = Field(
        ...,
        description="The answer to the interviewer's latest question.",
    )
