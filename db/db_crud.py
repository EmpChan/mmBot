from typing import List, Optional

from . import Channel, ChannelLog, Database, NotionPost, session_scope


# Channel CRUD
def create_channel(purpose_id: Optional[str], channel_url: str) -> Channel:
    with session_scope(commit=True) as session:
        channel = Channel(purpose_id=purpose_id, channel_url=channel_url)
        session.add(channel)
        session.flush()
        session.refresh(channel)
        return channel


def get_channel(channel_id: int) -> Optional[Channel]:
    with session_scope() as session:
        return session.get(Channel, channel_id)


def get_channel_by_url(channel_url: str) -> Optional[Channel]:
    with session_scope() as session:
        return session.query(Channel).filter(Channel.channel_url == channel_url).first()

def get_channels_by_purpose(purpose: str) -> Optional[Channel]:
    with session_scope() as session:
        return session.query(Channel).filter(Channel.purpose_id == purpose)
    
def list_channels(limit: Optional[int] = None) -> List[Channel]:
    with session_scope() as session:
        query = session.query(Channel).order_by(Channel.created_at.desc())
        if limit:
            query = query.limit(limit)
        return query.all()


def update_channel(
    channel_id: int,
    *,
    purpose_id: Optional[str] = None,
    channel_url: Optional[str] = None,
) -> Optional[Channel]:
    updates = {}
    if purpose_id is not None:
        updates["purpose_id"] = purpose_id
    if channel_url is not None:
        updates["channel_url"] = channel_url
    if not updates:
        return get_channel(channel_id)

    with session_scope(commit=True) as session:
        channel = session.get(Channel, channel_id)
        if channel is None:
            return None
        for key, value in updates.items():
            setattr(channel, key, value)
        session.flush()
        session.refresh(channel)
        return channel


def delete_channel(channel_id: int) -> bool:
    with session_scope(commit=True) as session:
        channel = session.get(Channel, channel_id)
        if channel is None:
            return False
        session.delete(channel)
        return True


def list_databases() -> List[Database]:
    with session_scope() as session:
        return session.query(Database).order_by(Database.created_at.desc()).all()


def create_database(db_id: str) -> Database:
    with session_scope(commit=True) as session:
        database = Database(db_id=db_id)
        session.add(database)
        session.flush()
        session.refresh(database)
        return database


def get_database(db_id: str) -> Optional[Database]:
    with session_scope() as session:
        return session.get(Database, db_id)


def update_database(db_id: str, *, new_db_id: Optional[str] = None) -> Optional[Database]:
    if not new_db_id:
        return get_database(db_id)

    with session_scope(commit=True) as session:
        database = session.get(Database, db_id)
        if database is None:
            return None
        database.db_id = new_db_id
        session.flush()
        session.refresh(database)
        return database


def delete_database(db_id: str) -> bool:
    with session_scope(commit=True) as session:
        database = session.get(Database, db_id)
        if database is None:
            return False
        session.delete(database)
        return True


def create_notion_post(db_id: str) -> NotionPost:
    with session_scope(commit=True) as session:
        post = NotionPost(db_id=db_id)
        session.add(post)
        session.flush()
        session.refresh(post)
        return post


def get_notion_post(post_id: int) -> Optional[NotionPost]:
    with session_scope() as session:
        return session.get(NotionPost, post_id)


def list_notion_posts(db_id: Optional[str] = None, limit: Optional[int] = None) -> List[NotionPost]:
    with session_scope() as session:
        query = session.query(NotionPost).order_by(NotionPost.created_at.desc())
        if db_id is not None:
            query = query.filter(NotionPost.db_id == db_id)
        if limit:
            query = query.limit(limit)
        return query.all()


def update_notion_post(post_id: int, *, db_id: Optional[str] = None) -> Optional[NotionPost]:
    if db_id is None:
        return get_notion_post(post_id)

    with session_scope(commit=True) as session:
        post = session.get(NotionPost, post_id)
        if post is None:
            return None
        post.db_id = db_id
        session.flush()
        session.refresh(post)
        return post


def delete_notion_post(post_id: int) -> bool:
    with session_scope(commit=True) as session:
        post = session.get(NotionPost, post_id)
        if post is None:
            return False
        session.delete(post)
        return True


def saveLog(content: str, io: bool = False, channel_id: Optional[int] = None) -> ChannelLog:
    return create_channel_log(content=content, io=io, channel_id=channel_id)


def create_channel_log(content: str, io: bool = False, channel_id: Optional[int] = None) -> ChannelLog:
    with session_scope(commit=True) as session:
        log = ChannelLog(content=content, io=io, channel_id=channel_id)
        session.add(log)
        session.flush()
        session.refresh(log)
        return log


def get_channel_log(log_id: int) -> Optional[ChannelLog]:
    with session_scope() as session:
        return session.get(ChannelLog, log_id)


def get_logs_by_channel(channel_id: int, limit: Optional[int] = None) -> List[ChannelLog]:
    with session_scope() as session:
        query = (
            session.query(ChannelLog)
            .filter(ChannelLog.channel_id == channel_id)
            .order_by(ChannelLog.created_at.desc())
        )
        if limit:
            query = query.limit(limit)
        return query.all()


def delete_channel_log(log_id: int) -> bool:
    with session_scope(commit=True) as session:
        log = session.get(ChannelLog, log_id)
        if log is None:
            return False
        session.delete(log)
        return True


def list_channel_logs(channel_id: Optional[int] = None, limit: Optional[int] = None) -> List[ChannelLog]:
    with session_scope() as session:
        query = session.query(ChannelLog).order_by(ChannelLog.created_at.desc())
        if channel_id is not None:
            query = query.filter(ChannelLog.channel_id == channel_id)
        if limit:
            query = query.limit(limit)
        return query.all()
