from contextlib import contextmanager

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
    func,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Channel(Base):
    __tablename__ = "channel"

    channel_id = Column(Integer, primary_key=True, index=True)
    purpose_id = Column(String)
    channel_input = Column(Boolean)
    channel_url = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    logs = relationship("ChannelLog", back_populates="channel")


class Database(Base):
    __tablename__ = "database"

    db_id = Column(String, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())

    notion_posts = relationship("NotionPost", back_populates="database")


class NotionPost(Base):
    __tablename__ = "notion_posts"

    id = Column(Integer, primary_key=True, index=True)
    db_id = Column(String, ForeignKey("database.db_id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    database = relationship("Database", back_populates="notion_posts")


class ChannelLog(Base):
    __tablename__ = "channel_log"

    log_id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    io = Column(Boolean)
    channel_id = Column(Integer, ForeignKey("channel.channel_id"))
    created_at = Column(DateTime, server_default=func.now())

    channel = relationship("Channel", back_populates="logs")


DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)


@contextmanager
def session_scope(commit: bool = False):
    session = SessionLocal()
    try:
        yield session
        if commit:
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("✅ DB tables ensured.")