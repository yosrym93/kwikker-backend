from . import actions


def test_get_notifications():
    """
    this function tests if username "khaled" is in the database if he is in the database ,test should pass

    """
    username = "khaled"
    list_notifications = actions.get_notifications(username)
    assert list_notifications == []


def test_create_notifications():
    """
    this function tests if notification is created in the database by counting number of notification in the database

    """
    old_size = actions.get_list_size_notification()
    actions.create_notifications('khaled', 'REKWEEK', 1)
    new_size = actions.get_list_size_notification()
    assert new_size > old_size
