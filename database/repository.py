from datetime import date
from typing import Optional, List
from .models import UserExam
from .connection import SessionLocal

class ExamRepository:
    """
    handles database operations for user-exam tracking.
    """

    def __init__(self):
        self.db = SessionLocal()

    def set_user_exam(self, user_id: int, username: str, channel_id: int, exam_date: date) -> UserExam:
        """
        set/update user's exam date
        """

        user_exam = self.db.query(UserExam).filter(
            UserExam.user_id == user_id
        ).first()

        if user_exam:
            user_exam.exam_date = exam_date
            user_exam.username = username
            user_exam.channel_id = channel_id
        else:
            user_exam = UserExam(
                user_id=user_id,
                username=username,
                channel_id=channel_id,
                exam_date=exam_date
            )
            self.db.add(user_exam)

        self.db.commit()
        return user_exam

    def get_user_exam(self, user_id: int) -> Optional[UserExam]:
        """
        get details.
        """

        return self.db.query(UserExam).filter(
            UserExam.user_id == user_id
        ).first()

    def get_all_users(self) -> List[UserExam]:
        """
        get all users with exam dates.
        """
        
        return self.db.query(UserExam).all()

    def delete_user_exam(self, user_id: int) -> bool:
        """
        remove user-records from the database.
        """

        user_exam = self.get_user_exam(user_id)
        if user_exam:
            self.db.delete(user_exam)
            self.db.commit()
            return True
        return False

    def close(self):
        self.db.close()
