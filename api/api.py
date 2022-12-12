import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from Utils.database_conn import db
import config as cfg

app = FastAPI()


def start_server():
    uvicorn.run(app, host=cfg.host_url, port=cfg.port)


class ExecuteDb(BaseModel):
    list_args: list


@app.post('/execute_db')
def execute_db(item: ExecuteDb):
   return db.execute_db(item.list_args)


