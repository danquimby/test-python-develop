from sqlalchemy import TIMESTAMP, BigInteger, Column, Identity
from sqlalchemy.orm import declarative_base

from my_project.database.utils import utcnow

SABase = declarative_base()


class Base(SABase):
    __abstract__ = True

    user_id = Column(BigInteger, Identity(always=True), primary_key=True)
    create_at = Column(
        TIMESTAMP(timezone=True),
        server_default=utcnow(),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=utcnow(),
        default=utcnow(),
        onupdate=utcnow(),
    )
