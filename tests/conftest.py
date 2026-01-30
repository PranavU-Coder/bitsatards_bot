import os

# dummy DATABASE_URL for testing-purposes only.
os.environ.setdefault('DATABASE_URL', 'postgresql://dummy:dummy@localhost/dummy')

import pytest
import database.models as models
from unittest.mock import Mock, patch
from services.exam_tracker import ExamTracker

@pytest.fixture
def exam_columns():
    return models.UserExam.__table__.columns

@pytest.fixture
def mock_repo():
    return Mock()

@pytest.fixture
def tracker(mock_repo):
    with patch('services.exam_tracker.ExamRepository', return_value=mock_repo):
        return ExamTracker()

@pytest.fixture
def reminder(mock_repo):
    with patch('services.reminder.ExamRepository', return_value=mock_repo):
        from services.reminder import Reminder
        return Reminder()
