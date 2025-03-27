from pydantic import BaseModel


class UserNameStatus(BaseModel):
    first_name: str
    status: str