from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from nucleic.person.models import PersonInDB
from nucleic.checkin.models import CheckInDB
from nucleic.checkin.schemas import CheckIn


# 定义依赖类，用于解析参数
class QueryParams:
    def __init__(
            self,
            xm: Optional[str] = None,
            lxdh: Optional[str] = None,
            jzdz: Optional[str] = None,
            bqbh: Optional[str] = None,
            cjry: Optional[int] = None,
            zjhm: Optional[str] = None,
            page: Optional[int] = 1,
            size: Optional[int] = 10
    ):
        self.xm = xm
        self.lxdh = lxdh
        self.jzdz = jzdz
        self.bqbh = bqbh
        self.cjry = cjry
        self.zjhm = zjhm
        self.page = page
        self.size = size


# 保存登记数据
def save_checkin(db: Session, data: CheckIn):
    dbdata = CheckInDB(
        person_id=data.person_id,
        bqbh=data.bqbh,
        bqxh=data.bqxh,
        cjdd=data.cjdd,
        cjry=data.cjry
    )
    db.add(dbdata)
    db.commit()
    db.refresh(dbdata)
    return dbdata


# 返回登记数据列表
def list_checkin(db: Session, params: QueryParams):
    # 总条数查询
    stmt_cnt = select(func.count(CheckInDB.id)).join(PersonInDB, isouter=True)

    # 数据查询
    stmt = select(
        CheckInDB.id.label('id'),
        CheckInDB.bqbh.label('bqbh'),
        CheckInDB.bqxh.label('bqxh'),
        CheckInDB.cjdd.label('cjdd'),
        CheckInDB.cjry.label('cjry'),
        PersonInDB.djrq.label('djrq'),
        PersonInDB.id.label('person_id'),
        PersonInDB.xm.label('xm'),
        PersonInDB.xb.label('xb'),
        PersonInDB.nl.label('nl'),
        PersonInDB.nldw.label('nldw'),
        PersonInDB.hjdz.label('hjdz'),
        PersonInDB.jzdz.label('jzdz'),
        PersonInDB.csrq.label('csrq'),
        PersonInDB.dw.label('dw'),
        PersonInDB.lxdh.label('lxdh'),
        PersonInDB.zjlb.label('zjlb'),
        PersonInDB.zjhm.label('zjhm'),
        PersonInDB.tw.label('tw'),
        PersonInDB.bz.label('bz'),
    ).join(PersonInDB, isouter=True)

    # 动态过滤条件
    conditions = []
    if params.xm:
        conditions.append(PersonInDB.xm == params.xm)
    if params.lxdh:
        conditions.append(PersonInDB.lxdh == params.lxdh)
    if params.jzdz:
        conditions.append(PersonInDB.jzdz == params.jzdz)
    if params.zjhm:
        conditions.append(PersonInDB.zjhm == params.zjhm)
    if params.bqbh:
        conditions.append(CheckInDB.bqbh == params.bqbh)
    if params.cjry:
        conditions.append(CheckInDB.cjry == params.cjry)

    # 应用过滤条件
    stmt_cnt = stmt_cnt.where(*conditions)
    stmt = stmt.where(*conditions)

    # 分页
    stmt = stmt.limit(params.size).offset((params.page - 1) * params.size)

    # 执行查询
    cnt = db.scalar(stmt_cnt)  # 获取总条数
    data = db.execute(stmt).all()  # 获取分页数据

    return {'count': cnt, 'list': data}
