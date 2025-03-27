from typing import List, Optional

from pydantic import BaseModel


class Likes(BaseModel):
    count: int


class VideoItem(BaseModel):
    views: int
    comments: Optional[int] = None
    likes: Optional[Likes] = None


class Videos(BaseModel):
    count: int
    items: List[VideoItem]