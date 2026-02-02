from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


# ========================
# Channel
# ========================

class Channel(Base):
    __tablename__ = "channels"

    channel_id = Column(Integer, primary_key=True, index=True)
    purpose = Column(String, nullable=True)
    channel_io = Column(Boolean, default=True)
    channel_token = Column(String, nullable=False)

    # relations
    messages = relationship("MessageLog", back_populates="channel")
    alerts = relationship("Alert", back_populates="channel")
    relate_dbs = relationship("RelateChanDB", back_populates="channel")


# ========================
# NotionDB
# ========================

class NotionDB(Base):
    __tablename__ = "notion_dbs"

    db_id = Column(Integer, primary_key=True, index=True)
    purpose_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # relations
    channels = relationship("RelateChanDB", back_populates="notion_db")
    post_logs = relationship("NotionPostLog", back_populates="notion_db")


# ========================
# RelateChanDB (N:M 테이블)
# ========================

class RelateChanDB(Base):
    __tablename__ = "relate_chan_db"

    db_id = Column(
        Integer,
        ForeignKey("notion_dbs.db_id", ondelete="CASCADE"),
        primary_key=True,
    )

    channel_id = Column(
        Integer,
        ForeignKey("channels.channel_id", ondelete="CASCADE"),
        primary_key=True,
    )

    notion_db = relationship("NotionDB", back_populates="channels")
    channel = relationship("Channel", back_populates="relate_dbs")


# ========================
# MessageLog
# ========================

class MessageLog(Base):
    __tablename__ = "message_logs"

    log_id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)

    channel_id = Column(
        Integer,
        ForeignKey("channels.channel_id", ondelete="CASCADE"),
        nullable=False,
    )

    channel = relationship("Channel", back_populates="messages")


# ========================
# NotionPostLog
# ========================

class NotionPostLog(Base):
    __tablename__ = "notion_post_logs"

    log_id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)

    db_id = Column(
        Integer,
        ForeignKey("notion_dbs.db_id", ondelete="CASCADE"),
        nullable=False,
    )

    notion_db = relationship("NotionDB", back_populates="post_logs")


# ========================
# Alert
# ========================

class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    alert_at = Column(DateTime, nullable=False)

    message = Column(Text, nullable=False)
    is_done = Column(Boolean, default=False)

    channel_id = Column(
        Integer,
        ForeignKey("channels.channel_id", ondelete="CASCADE"),
        nullable=False,
    )

    channel = relationship("Channel", back_populates="alerts")

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("DB 완성")