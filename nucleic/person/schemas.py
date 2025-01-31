from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# 个人信息数据模型
class Person(BaseModel):
    id: Optional[int] = None
    djrq: datetime
    xm: str
    xb: str
    nl: Optional[int] = None
    nldw: Optional[str] = '年'
    hjdz: Optional[str] = None
    jzdz: Optional[str] = None
    csrq: Optional[datetime] = None
    dw: Optional[str]
    lxdh: str
    zjlb: Optional[str] = '身份证'
    zjhm: str
    tw: Optional[str]
    bz: Optional[str]

    class Config:
        orm_mode = True
