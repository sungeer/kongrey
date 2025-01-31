from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from nucleic.person.models import PersonInDB
from nucleic.person.schemas import Person


# 定义依赖函数
async def get_params(
    xm: Optional[str] = None,
    lxdh: Optional[str] = None,
    jzdz: Optional[str] = None,
    page: Optional[int] = 1,
    size: Optional[int] = 10
):
    return {'xm': xm, 'lxdh': lxdh, 'jzdz': jzdz, 'page': page, 'size': size}


# 保存预约信息
def save_person(db: Session, data: Person):
    dbdata = PersonInDB(**data.model_dump())
    db.add(dbdata)
    db.commit()
    db.refresh(dbdata)
    return dbdata


def get_person(db: Session, zjhm):
    stmt = select(PersonInDB).where(PersonInDB.zjhm == zjhm)  # type: ignore
    data = db.scalars(stmt).first()
    return data


# 分页取出预约信息列表,默认第1页，10条记录
def list_person(db: Session, params):
    # 查询当前条件下的总数量
    stmt_cnt = select(func.count(PersonInDB.id))

    # 查询数据
    stmt = select(PersonInDB)

    # 动态过滤条件
    if params['xm']:
        stmt = stmt.where(PersonInDB.xm == params['xm'])  # type: ignore
        stmt_cnt = stmt_cnt.where(PersonInDB.xm == params['xm'])  # type: ignore
    if params['lxdh']:
        stmt = stmt.where(PersonInDB.lxdh == params['lxdh'])  # type: ignore
        stmt_cnt = stmt_cnt.where(PersonInDB.lxdh == params['lxdh'])  # type: ignore
    if params['jzdz']:
        stmt = stmt.where(PersonInDB.jzdz.like(f"%{params['jzdz']}%"))
        stmt_cnt = stmt_cnt.where(PersonInDB.jzdz.like(f"%{params['jzdz']}%"))

    # 分页
    stmt = stmt.limit(params['size']).offset((params['page'] - 1) * params['size'])

    # 执行查询
    cnt = db.scalar(stmt_cnt)  # 获取总条数
    data = db.scalars(stmt).all()  # 获取分页数据

    return {"count": cnt, "list": data}
