from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Depends
from models import (
    Channel,
    NotionDB,
    RelateChanDB,
    MessageLog,
    NotionPostLog,
    Alert,
)

from models import get_db
# ============================
# Channel
# ============================

def create_channel(purpose: str, token: str, channel_io=True,db: Session = Depends(get_db)):
    obj = Channel(
        purpose=purpose,
        channel_token=token,
        channel_io=channel_io,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_channel(channel_id: int,db: Session = Depends(get_db)):
    return db.query(Channel).filter(Channel.channel_id == channel_id).first()


def get_channel_by_token(token: str,db: Session = Depends(get_db)):
    return db.query(Channel).filter(Channel.channel_token == token).first()

def get_channels_by_purpose(purpose: str, db: Session = Depends(get_db)):
    return db.query(Channel).filter(Channel.purpose == purpose)

def list_channels(db: Session = Depends(get_db)):
    return db.query(Channel).all()


def delete_channel( channel_id: int,db: Session = Depends(get_db)):
    obj = get_channel(db, channel_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


# ============================
# NotionDB
# ============================

def create_notion_db(purpose_id: str,db: Session = Depends(get_db)):
    obj = NotionDB(
        purpose_id=purpose_id,
        created_at=datetime.utcnow(),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_notion_db(db_id: int,db: Session = Depends(get_db)):
    return db.query(NotionDB).filter(NotionDB.db_id == db_id).first()


def list_notion_dbs(db: Session = Depends(get_db)):
    return db.query(NotionDB).all()


def delete_notion_db(db_id: int,db: Session = Depends(get_db)):
    obj = get_notion_db(db, db_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


# ============================
# RelateChanDB
# ============================

def relate_channel_db(channel_id: int, db_id: int,db: Session = Depends(get_db)):
    obj = RelateChanDB(
        channel_id=channel_id,
        db_id=db_id,
    )
    db.add(obj)
    db.commit()
    return obj


def unrelate_channel_db(channel_id: int, db_id: int,db: Session = Depends(get_db)):
    obj = (
        db.query(RelateChanDB)
        .filter(
            RelateChanDB.channel_id == channel_id,
            RelateChanDB.db_id == db_id,
        )
        .first()
    )
    if not obj:
        return None

    db.delete(obj)
    db.commit()
    return obj


# ============================
# MessageLog
# ============================

def create_message_log(channel_id: int, message: str,db: Session = Depends(get_db)):
    obj = MessageLog(
        channel_id=channel_id,
        message=message,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_channel_messages(channel_id: int,db: Session = Depends(get_db)):
    return (
        db.query(MessageLog)
        .filter(MessageLog.channel_id == channel_id)
        .order_by(MessageLog.log_id.desc())
        .all()
    )


# ============================
# NotionPostLog
# ============================

def create_notion_post_log(db_id: int, message: str,db: Session = Depends(get_db)):
    obj = NotionPostLog(
        db_id=db_id,
        message=message,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_notion_posts(db_id: int,db: Session = Depends(get_db)):
    return (
        db.query(NotionPostLog)
        .filter(NotionPostLog.db_id == db_id)
        .order_by(NotionPostLog.log_id.desc())
        .all()
    )


# ============================
# Alert
# ============================

def create_alert(
    channel_id: int,
    message: str,
    alert_at: datetime,
    db: Session = Depends(get_db)
):
    obj = Alert(
        channel_id=channel_id,
        message=message,
        alert_at=alert_at,
        created_at=datetime.utcnow(),
        is_done=False,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_alert(alert_id: int,db: Session = Depends(get_db)):
    return db.query(Alert).filter(Alert.alert_id == alert_id).first()


def list_pending_alerts(db: Session = Depends(get_db)):
    return (
        db.query(Alert)
        .filter(Alert.is_done.is_(False))
        .order_by(Alert.alert_at)
        .all()
    )


def mark_alert_done(alert_id: int,db: Session = Depends(get_db)):
    obj = get_alert(db, alert_id)
    if not obj:
        return None

    obj.is_done = True
    db.commit()
    db.refresh(obj)
    return obj


def delete_alert(alert_id: int,db: Session = Depends(get_db)):
    obj = get_alert(db, alert_id)
    if not obj:
        return None

    db.delete(obj)
    db.commit()
    return obj