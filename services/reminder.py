from datetime import date
from database.repository import ExamRepository


class Reminder:
    """
    sends user reminders when their exam will take place if they have set a date.
    """

    def __init__(self):
        self.repo = ExamRepository()
        self.sent_today = set()

    def users_to_remind(self):
        """
        get users who need reminders today
        """

        reminders = []
        all_users = self.repo.get_all_users()
        today = date.today()

        for user_exam in all_users:
            days_until = (user_exam.exam_date - today).days
            user_id = user_exam.user_id

            # if already sent, don't send again :p
            if user_id in self.sent_today:
                continue

            message = None

            if days_until == 30:
                message = f"**30 Days Until BITSAT**\nExam: {user_exam.exam_date.strftime('%d %B %Y')}\nOne month to go"

            elif days_until == 7:
                message = f"**1 Week Until BITSAT!**\nExam: {user_exam.exam_date.strftime('%d %B %Y')}\nFinal week"

            elif 1 <= days_until <= 6:
                if days_until == 1:
                    message = f"**Tomorrow is BITSAT!**\n{user_exam.exam_date.strftime('%d %B %Y')}\nGet good sleep for tomorrow"
                else:
                    message = f"**{days_until} Days Until BITSAT**\n{user_exam.exam_date.strftime('%d %B %Y')}\nPlease close discord & study for your own sake"
            elif days_until == 0:
                message = f"**TODAY IS THE DAY!**\nBITSAT: {user_exam.exam_date.strftime('%d %B %Y')}\nGood luck Soldier"
            if message:
                reminders.append(
                    {
                        "user_id": user_id,
                        "message": message,
                        "channel_id": user_exam.channel_id,
                    }
                )
                self.sent_today.add(user_id)

        return reminders

    def reset_daily_tracking(self):
        self.sent_today.clear()

    def __del__(self):
        self.repo.close()
