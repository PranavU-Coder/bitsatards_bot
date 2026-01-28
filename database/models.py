from sqlalchemy import Column, Integer, BigInteger, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserExam(Base):
    __tablename__ = 'bitsat'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String)
    exam_date = Column(Date, nullable=False)
    channel_id = Column(BigInteger, nullable=False)

    def __repr__(self):
        return f"<UserExam(user={self.username}, date={self.exam_date})>"
