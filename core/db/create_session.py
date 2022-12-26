from uuid import uuid4

from .session import (
    remove_session,
    set_session_context,
    reset_session_context,
)
from core.db import session


def create_session(func):
    async def _create_session(*args, **kwargs):
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            await func(*args, **kwargs)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            remove_session()
            reset_session_context(context=context)

    return _create_session
