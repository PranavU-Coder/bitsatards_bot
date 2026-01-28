from datetime import date, datetime
from typing import Optional
from database.repository import ExamRepository

class ExamTracker:
    """
    this is what we will use in main.py
    """

    def __init__(self):
        self.repo = ExamRepository()

    def set_exam_date(self, user_id: int, username: str, channel_id: int, exam_date: date) -> str:
        """
        set user's exam date and return confirmation message
        """

        self.repo.set_user_exam(user_id, username, channel_id, exam_date)
        days_left = (exam_date - date.today()).days

        if days_left > 0:
            return f"exam date set for **{exam_date.strftime('%d %B %Y')}**\n**{days_left} days** remaining"
        elif days_left == 0:
            return f"exam date set for **{exam_date.strftime('%d %B %Y')}**\nwhich is btw today, best of luck soldier!"
        else:
            return f"the date you set ({exam_date.strftime('%d %B %Y')}) has already been passed mate, please focus on the future."

    def get_countdown(self, user_id: int) -> str:
        """
        countdown message for user
        """

        user_exam = self.repo.get_user_exam(user_id)

        if not user_exam:
            return "no record for user found.\nuse `!!time -s DD-MM-YYYY` to set it.\nexample: `!!time -s 15-04-2026`"

        today = date.today()
        exam_date = user_exam.exam_date
        days_left = (exam_date - today).days

        exam_date_str = exam_date.strftime('%d %B %Y')

        if days_left > 0:
            weeks = days_left // 7
            remaining_days = days_left % 7

            time_str = f"**{days_left} days**"
            if weeks > 0:
                time_str += f" ({weeks} weeks and {remaining_days} days)"

            return f"exam date: {exam_date_str}\ntime remaining: {time_str}"

        elif days_left == 0:
            return f"**TODAY**\nBITSAT: {exam_date_str}\nIt all comes down to this."

        else:
            days_since = abs(days_left)
            return f"Your exam is over\nBITSAT was on {exam_date_str}\nIt's been {days_since} days since your exam\nHoping you did well soldier!\nIf you want to track for second session, please run the time -r command."

    def reset(self, user_id: int) -> str:
        """
        remove user's exam tracking record completely from database.
        """

        if self.repo.delete_user_exam(user_id):
            return "record cleared"
        return "no exam has been set."

    def __del__(self):
        self.repo.close()
