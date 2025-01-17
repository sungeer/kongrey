from sqlalchemy import Column, String, Integer

from nucleic.app.database import Base


class UserInDB(Base):
    __tablename__ = 'auth_user'

    id = Column('id', Integer, autoincrement=True, primary_key=True, doc='ID')
    username = Column('username', String(50))
    hashed_password = Column('hashed_password', String(64))
