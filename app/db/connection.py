from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_MODE = config('TEST_MODE', default=False, cast=bool)
DB_URL = config('DB_URL_TEST') if TEST_MODE else config('DB_URL')

engine = create_engine(DB_URL, pool_pre_ping=True, echo=TEST_MODE) # echo print no terminal todas as queries sql executadas no sqlalchemy
# guarda a session mas nao cria, só cria quando chamar.
Session = sessionmaker(bind=engine)
