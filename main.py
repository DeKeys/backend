from fastapi import FastAPI
from routers import auth, passwords
from fastapi.logger import logger
import logging
import os
import data.db_session as db_session


db_session.global_init(os.path.join("db", "db.sqlite3"))

logger.setLevel(logging.DEBUG)

app = FastAPI()
app.include_router(auth.router)
app.include_router(passwords.router)

