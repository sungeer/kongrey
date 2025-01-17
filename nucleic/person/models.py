from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from nucleic.app.database import Base


# 个人信息数据库模型
class PersonInDB(Base):
    __tablename__ = 'person'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    djrq = Column('djrq', DateTime, doc='登记日期')
    xm = Column('xm', String(50), doc='姓名')
    xb = Column('xb', String(10), doc='性别')
    nl = Column('nl', Integer, doc='年龄')
    nldw = Column('nldw', String(10), doc='年龄单位，年、月')
    hjdz = Column('hjdz', String(50), doc='户籍地址')
    jzdz = Column('jzdz', String(50), doc='居住地址')
    csrq = Column('csrq', DateTime, doc='出生日期')
    dw = Column('dw', String(100), doc='工作单位')
    lxdh = Column('lxdh', String(20), doc='联系电话')
    zjlb = Column('zjlb', String(20), doc='证件类型，身份证、户口本、护照')
    zjhm = Column('zjhm', String(20), doc='证件号码')
    tw = Column('tw', String(10), doc='体温')
    bz = Column('bz', String(50), doc='备注')

    checkin = relationship('CheckInDB', uselist=False, backref='person')
