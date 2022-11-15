"""
# Tests / Integration / Browse / Post View / Report
# Tests / Integration / Browse / Post View / Unreport

Tests for post_view/report
Tests for post_view/unreport

* Fails when no permission to unreport post
* Post_list correctly shows that a post is reported
* Post_view correctly shows that a post is reported
* Mods and admins can unreport reported posts
* Un-reporting an unanswered post sends it back to the main queue
* Un-reporting an answered post sends it back to the answered queue
"""
import pytest
from backend.util import http_errors
from resources import consts
from tests.integration.conftest import (
    ISimpleUsers,
    IMakePosts,
)
from ensemble_request.browse import (
    post_list,
    post_view,
    post_create,
    report_post,
    unreport_post,
    add_comment,
    accept_comment
)
from ensemble_request.taskboard import queue_post_list, queue_list
from tests.integration.helpers import get_queue


@pytest.mark.core
def test_reported_post_view(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Does post_view correctly show whether the post is reported or not?
    """
    user_token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]

    post = post_view(user_token, post_id)
    assert not post["reported"]

    assert report_post(user_token, post_id)["reported"]
    post = post_view(user_token, post_id)
    assert post["reported"]


def test_reported_post_list(
    simple_users: ISimpleUsers,
):
    """
    Does post_list correctly show whether the post is reported or not?
    """
    user_token = simple_users["user"]["token"]
    post_id = post_create(user_token, "head", "text", [])["post_id"]

    post = post_list(user_token)["posts"][0]
    assert not post["reported"]

    assert report_post(user_token, post_id)["reported"]
    post = post_list(user_token)["posts"][0]
    assert post["reported"]


def test_reported_queue(
    simple_users: ISimpleUsers
):
    """
    Does reporting a post send it to the reported queue?
    Does un-reporting a unanswered post send it to the main queue?
    """
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]

    post_id = post_create(user_token, "head", "text", [])["post_id"]

    # Reporting a post sends it to the reported queue
    report_post(user_token, post_id)
    post_queue_name = post_view(user_token, post_id)["queue"]
    assert post_queue_name == consts.REPORTED_QUEUE

    queue_id = get_queue(queue_list(mod_token)['queues'],
                         consts.REPORTED_QUEUE)["queue_id"]
    queue = queue_post_list(mod_token, queue_id)
    assert post_id in queue["posts"]

    # Un-reporting a post sends it back to the main queue
    assert not unreport_post(mod_token, post_id)["reported"]
    post_queue_name = post_view(user_token, post_id)["queue"]
    assert post_queue_name == consts.MAIN_QUEUE

    queue_id = get_queue(queue_list(mod_token)['queues'],
                         consts.MAIN_QUEUE)["queue_id"]
    queue = queue_post_list(mod_token, queue_id)
    assert post_id in queue["posts"]


def test_report_answered_post(
    simple_users: ISimpleUsers
):
    """
    Does un-reporting an answered post send it to the answered queue?
    """
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]

    post_id = post_create(mod_token, "head", "text", [])["post_id"]
    comment_id = add_comment(user_token, post_id, "first")["comment_id"]
    accept_comment(mod_token, comment_id)
    report_post(user_token, post_id)

    # Un-reporting a post sends it back to the answered queue
    unreport_post(mod_token, post_id)
    post_queue_name = post_view(user_token, post_id)["queue"]
    assert post_queue_name == consts.ANSWERED_QUEUE

    queue_id = get_queue(queue_list(mod_token)['queues'],
                         consts.ANSWERED_QUEUE)["queue_id"]
    queue = queue_post_list(mod_token, queue_id)
    assert post_id in queue["posts"]


def test_no_permission_unreport(
    simple_users: ISimpleUsers
):
    """
    Users cannot un-report posts
    """
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]

    post_id = post_create(mod_token, "head", "text", [])["post_id"]
    report_post(user_token, post_id)
    with pytest.raises(http_errors.Forbidden):
        unreport_post(user_token, post_id)
