from pydantic import BaseModel


class WallPostCount(BaseModel):
    count: int