from pydantic import BaseModel
from typing import Optional
from nucleic.person.schemas import Person


# 登记数据模型
class CheckIn(BaseModel):
    id: Optional[int] = None
    bqbh: str
    bqxh: int
    cjdd: Optional[str]
    cjry: Optional[int] = None
    person_id: Optional[int]

    class Config:
        orm_mode = True


# 登记响应模型
class CheckInResponse(CheckIn, Person):
    pass
