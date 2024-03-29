import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from sqlalchemy.pool import StaticPool


SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(db_file):
    """Initialization of the main functionality."""

    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f"sqlite:///{db_file.strip()}?check_same_thread=False"

    engine = sa.create_engine(conn_str, poolclass=StaticPool, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    """Creation of a new session."""

    global __factory
    return __factory()

