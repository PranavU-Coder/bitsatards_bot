import pytest
from sqlalchemy import Integer, BigInteger, String, Date

# basic tests to assert datatype & existence.
class TestDatabase:

    def test_column_types(self, exam_columns):
        assert isinstance(exam_columns['id'].type, Integer)
        assert isinstance(exam_columns['user_id'].type, BigInteger)
        assert isinstance(exam_columns['username'].type, String)
        assert isinstance(exam_columns['exam_date'].type, Date)
        assert isinstance(exam_columns['channel_id'].type, BigInteger)

    def test_all_columns_exist(self, exam_columns):
        expected_columns = {'id', 'user_id', 'username', 'exam_date', 'channel_id'}
        actual_columns = set(exam_columns.keys())
        
        assert actual_columns == expected_columns
