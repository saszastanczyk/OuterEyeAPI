from pydantic import BaseModel


class PrayResponseRequest(BaseModel):
    u: str
    t: str
    k: int


