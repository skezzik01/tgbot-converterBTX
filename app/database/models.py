from sqlalchemy import BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import SQLALCHEMY_URL
from sqlalchemy import ForeignKey

engine = create_async_engine(SQLALCHEMY_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    limit: Mapped[int] = mapped_column(nullable=False, default=350)
    count_convert: Mapped[int] = mapped_column(nullable=False, default=0)
    date: Mapped[str] = mapped_column(nullable=False)
    
class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    convert_type: Mapped[str] = mapped_column(nullable=False)
    files_id: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        