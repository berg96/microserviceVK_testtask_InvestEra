from pydantic import BaseModel

from app.api.schemas.followers import FollowersCount
from app.api.schemas.user import UserNameStatus
from app.api.schemas.video import Videos
from app.api.schemas.wall import WallPostCount


class AllInfo(BaseModel):
    user: UserNameStatus
    posts: WallPostCount
    followers: FollowersCount
    videos: Videos