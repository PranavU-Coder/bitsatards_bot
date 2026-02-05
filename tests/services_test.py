from datetime import date
from unittest.mock import Mock, patch


# a lot of unit-tests from here and on.
class TestExamTracker:
    @patch("services.exam_tracker.date")
    def test_set_exam_date_future(self, mock_date_class, tracker, mock_repo):
        mock_date_class.today.return_value = date(2026, 1, 1)
        exam_date = date(2026, 4, 15)
        result = tracker.set_exam_date(123, "testuser", 456, exam_date)
        mock_repo.set_user_exam.assert_called_once_with(123, "testuser", 456, exam_date)
        assert "exam date set for **15 April 2026**" in result
        assert "**104 days** remaining" in result

    @patch("services.exam_tracker.date")
    def test_set_exam_date_today(self, mock_date_class, tracker, mock_repo):
        today = date(2026, 4, 15)
        mock_date_class.today.return_value = today
        result = tracker.set_exam_date(123, "testuser", 456, today)
        assert "which is btw today, best of luck soldier!" in result

    @patch("services.exam_tracker.date")
    def test_past(self, mock_date_class, tracker, mock_repo):
        mock_date_class.today.return_value = date(2026, 4, 15)
        past_date = date(2026, 1, 1)
        result = tracker.set_exam_date(123, "testuser", 456, past_date)
        assert "has already been passed" in result

    @patch("services.exam_tracker.date")
    def test_future_date(self, mock_date_class, tracker, mock_repo):
        mock_date_class.today.return_value = date(2026, 1, 1)
        mock_exam = Mock()
        mock_exam.exam_date = date(2026, 4, 15)
        mock_repo.get_user_exam.return_value = mock_exam
        result = tracker.get_countdown(123)
        assert "exam date: 15 April 2026" in result
        assert "**104 days**" in result
        assert "14 weeks and 6 days" in result

    @patch("services.exam_tracker.date")
    def test_today(self, mock_date_class, tracker, mock_repo):
        today = date(2026, 4, 15)
        mock_date_class.today.return_value = today
        mock_exam = Mock()
        mock_exam.exam_date = today
        mock_repo.get_user_exam.return_value = mock_exam
        result = tracker.get_countdown(123)
        assert "**TODAY**" in result

    @patch("services.exam_tracker.date")
    def test_past_date(self, mock_date_class, tracker, mock_repo):
        mock_date_class.today.return_value = date(2026, 4, 15)
        mock_exam = Mock()
        mock_exam.exam_date = date(2026, 1, 1)
        mock_repo.get_user_exam.return_value = mock_exam
        result = tracker.get_countdown(123)
        assert "Your exam is over" in result
        assert "It's been 104 days since your exam" in result
        assert "time -r command" in result

    @patch("services.exam_tracker.date")
    def test_less_than_week(self, mock_date_class, tracker, mock_repo):
        mock_date_class.today.return_value = date(2026, 4, 10)
        mock_exam = Mock()
        mock_exam.exam_date = date(2026, 4, 15)
        mock_repo.get_user_exam.return_value = mock_exam
        result = tracker.get_countdown(123)

        assert "**5 days**" in result
        assert "exam date: 15 April 2026" in result

    def test_reset_success(self, tracker, mock_repo):
        mock_repo.delete_user_exam.return_value = True
        result = tracker.reset(123)
        mock_repo.delete_user_exam.assert_called_once_with(123)
        assert result == "record cleared"

    def test_reset_no_record(self, tracker, mock_repo):
        mock_repo.delete_user_exam.return_value = False
        result = tracker.reset(123)
        assert result == "no exam has been set."


class TestReminder:
    @patch("services.reminder.date")
    def test_reminder_30_days(self, mock_date_class, reminder, mock_repo):
        mock_date_class.today.return_value = date(2026, 3, 16)

        mock_user = Mock()
        mock_user.user_id = 123
        mock_user.exam_date = date(2026, 4, 15)
        mock_user.channel_id = 456

        mock_repo.get_all_users.return_value = [mock_user]
        reminders = reminder.users_to_remind()

        assert len(reminders) == 1
        assert reminders[0]["user_id"] == 123
        assert "**30 Days Until BITSAT**" in reminders[0]["message"]
        assert "15 April 2026" in reminders[0]["message"]
        assert reminders[0]["channel_id"] == 456

    @patch("services.reminder.date")
    def test_reminder_7_days(self, mock_date_class, reminder, mock_repo):
        mock_date_class.today.return_value = date(2026, 4, 8)

        mock_user = Mock()
        mock_user.user_id = 123
        mock_user.exam_date = date(2026, 4, 15)
        mock_user.channel_id = 456

        mock_repo.get_all_users.return_value = [mock_user]
        reminders = reminder.users_to_remind()

        assert len(reminders) == 1
        assert "**1 Week Until BITSAT!**" in reminders[0]["message"]
        assert "Final week" in reminders[0]["message"]

    @patch("services.reminder.date")
    def test_reminder_tomorrow(self, mock_date_class, reminder, mock_repo):
        mock_date_class.today.return_value = date(2026, 4, 14)
        mock_user = Mock()
        mock_user.user_id = 123
        mock_user.exam_date = date(2026, 4, 15)
        mock_user.channel_id = 456

        mock_repo.get_all_users.return_value = [mock_user]
        reminders = reminder.users_to_remind()

        assert len(reminders) == 1
        assert "**Tomorrow is BITSAT!**" in reminders[0]["message"]
        assert "Get good sleep for tomorrow" in reminders[0]["message"]

    @patch("services.reminder.date")
    def test_reminder_2_to_6_days(self, mock_date_class, reminder, mock_repo):
        mock_date_class.today.return_value = date(2026, 4, 10)

        mock_user = Mock()
        mock_user.user_id = 123
        mock_user.exam_date = date(2026, 4, 15)
        mock_user.channel_id = 456

        mock_repo.get_all_users.return_value = [mock_user]
        reminders = reminder.users_to_remind()

        assert len(reminders) == 1
        assert "**5 Days Until BITSAT**" in reminders[0]["message"]
        assert "Please close discord & study" in reminders[0]["message"]

    @patch("services.reminder.date")
    def test_reminder_today(self, mock_date_class, reminder, mock_repo):
        today = date(2026, 4, 15)
        mock_date_class.today.return_value = today

        mock_user = Mock()
        mock_user.user_id = 123
        mock_user.exam_date = today
        mock_user.channel_id = 456

        mock_repo.get_all_users.return_value = [mock_user]

        reminders = reminder.users_to_remind()

        assert len(reminders) == 1
        assert "**TODAY IS THE DAY!**" in reminders[0]["message"]
        assert "Good luck Soldier" in reminders[0]["message"]

    @patch("services.reminder.date")
    def test_multiple_users_different_dates(self, mock_date_class, reminder, mock_repo):
        mock_date_class.today.return_value = date(2026, 4, 14)

        user1 = Mock()
        user1.user_id = 123
        user1.exam_date = date(2026, 4, 15)
        user1.channel_id = 456

        user2 = Mock()
        user2.user_id = 456
        user2.exam_date = date(2026, 4, 21)
        user2.channel_id = 789

        user3 = Mock()
        user3.user_id = 789
        user3.exam_date = date(2026, 5, 1)
        user3.channel_id = 111

        mock_repo.get_all_users.return_value = [user1, user2, user3]
        reminders = reminder.users_to_remind()

        assert len(reminders) == 2
        assert reminders[0]["user_id"] == 123
        assert reminders[1]["user_id"] == 456

    @patch("services.reminder.date")
    def test_empty_user_list(self, mock_date_class, reminder, mock_repo):
        mock_date_class.today.return_value = date(2026, 4, 15)
        mock_repo.get_all_users.return_value = []
        reminders = reminder.users_to_remind()
        assert len(reminders) == 0
