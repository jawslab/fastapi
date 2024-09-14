from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Integer, String, text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # owner = relationship("User")