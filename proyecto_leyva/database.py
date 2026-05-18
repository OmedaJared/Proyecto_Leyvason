import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# DATABASE_URL example:
# - SQLite file: sqlite:///vida_saludable.db
# - Postgres: postgresql+psycopg2://user:pass@host:port/dbname
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///vida_saludable.db")

Base = declarative_base()

class BMIHistory(Base):
    __tablename__ = "bmi_history"
    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    imc = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)


_engine = None
_Session = None


def init_db(database_url: str | None = None):
    global _engine, _Session
    url = database_url or DATABASE_URL
    _engine = create_engine(url, echo=False)
    _Session = sessionmaker(bind=_engine)
    Base.metadata.create_all(_engine)


def save_bmi(weight: float, height: float, imc: float, category: str):
    if _Session is None:
        init_db()
    session = _Session()
    entry = BMIHistory(weight=weight, height=height, imc=imc, category=category, date=datetime.utcnow())
    session.add(entry)
    session.commit()
    session.close()


def get_history(limit: int = 100):
    if _Session is None:
        init_db()
    session = _Session()
    rows = session.query(BMIHistory).order_by(BMIHistory.date.desc()).limit(limit).all()
    session.close()
    return rows