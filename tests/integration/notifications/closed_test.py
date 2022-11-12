"""
# Tests / Integration / Notifications / Closed test

Tests for notifications when closing posts

* Users get notified when their post is closed
* User doesn't get notified if they close their own post
"""
import jestspectation as expect
from ..conftest import ISimpleUsers, IMakePosts, IBasicServerSetup
from ensemble_request import notifications, browse


def test_closed_post_notification(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """Do users get notified when their posts are closed?"""
    ...
