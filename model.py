from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# table class
class PostModel(Base):
    __tablename__ = 'Posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, primary_key=False, nullable=False)
    content = Column(String, primary_key=False, nullable=False)
    published = Column(Boolean, primary_key=False, nullable=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey('Users.id', ondelete="CASCADE"), nullable=False)
    user = relationship("UserModel")

class UserModel(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, primary_key=False, nullable=False)
    password = Column(String, primary_key=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
