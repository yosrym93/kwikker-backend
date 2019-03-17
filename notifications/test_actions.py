"""
    Your unit tests should reside here.
"""
from . import actions


def test_get_notifications():
    username = "khaled"
    list_notifications = actions.get_notifications(username)
    assert list_notifications == []


def test_create_notifications():
    old_size = actions.get_list_size_notification()
    actions.create_notifications('khaled', 'REKWEEK', 1)
    new_size = actions.get_list_size_notification()
    assert new_size > old_size
