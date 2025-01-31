from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from nucleic.conf.database import get_db
from nucleic.auth.services import AUTH_SCHEMA
from nucleic.utils.resp_util import PageResponse
from nucleic.person.schemas import Person
from nucleic.person.services import save_person, list_person, get_person, get_params

route = APIRouter(tags=['预约'])


@route.post('/submit', response_model=Person)
async def submit(data: Person, db: Session = Depends(get_db)):
    return save_person(db, data)


@route.get('/get', response_model=Person, dependencies=[Depends(AUTH_SCHEMA)])
async def get(zjhm: str, db: Session = Depends(get_db)):
    return get_person(db, zjhm)


@route.get('/list', response_model=PageResponse, dependencies=[Depends(AUTH_SCHEMA)])
async def person_list(params: dict = Depends(get_params), db: Session = Depends(get_db)):
    return list_person(db, params)
