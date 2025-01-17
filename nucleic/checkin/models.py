from sqlalchemy import Column, String, Integer, ForeignKey

from nucleic.app.database import Base


# 登记数据库模型
class CheckInDB(Base):
    __tablename__ = 'checkin'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    bqbh = Column('bqbh', String(50), doc='标签编号')
    bqxh = Column('bqxh', Integer, doc='本组标签序号')
    cjdd = Column('cjdd', String(50), doc='采集地点')
    cjry = Column('cjry', Integer, doc='采集人员')

    person_id = Column('person_id', Integer, ForeignKey('person.id'), doc='外键关联到个人信息')
