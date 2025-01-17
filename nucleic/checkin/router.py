from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from nucleic.conf.database import get_db
from nucleic.utils.resp_util import PageResponse
from nucleic.checkin.schemas import CheckIn
from nucleic.checkin.services import QueryParams, save_checkin, list_checkin

route = APIRouter(tags=['登记'])


@route.post('/submit', response_model=CheckIn)
async def submit(data: CheckIn, db: Session = Depends(get_db)):
    return save_checkin(db, data)


@route.get('/list', response_model=PageResponse)
async def checkin_list(params: QueryParams = Depends(), db: Session = Depends(get_db)):
    return list_checkin(db, params)
