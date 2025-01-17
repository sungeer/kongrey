from typing import List

from pydantic import BaseModel


# 响应分页数据的数据模型
class PageResponse(BaseModel):
    count: int  # 总记录数
    list: List  # 数据列表
