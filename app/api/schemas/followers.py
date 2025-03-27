from pydantic import BaseModel


class FollowersCount(BaseModel):
    count: int