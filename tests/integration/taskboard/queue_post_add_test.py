"""
# Tests / Integration / Taskboard / Post Add

Tests for taskboard/queue/post_add

* Fails when person without permission tries to move posts in the taskboard
* Succeeds in moving post to different queues
"""

import pytest
from backend.util import http_errors
from ensemble_request.browse import post_view, close_post
from tests.integration.helpers import get_queue
from ensemble_request.taskboard import (
    queue_post_list,
    queue_post_add,
    queue_list,
)
from tests.integration.conftest import (
    ISimpleUsers,
    IMakeQueues,
    IMakePosts
)


def test_no_permission(
    simple_users: ISimpleUsers,
    make_queues: IMakeQueues,
    make_posts: IMakePosts,
):
    """
    Is an error raised when a user without the permission to
    delegate posts to specialised queues tries to do so?
    """
    token = simple_users["user"]["token"]
    post_id = make_posts["post1_id"]
    queue_id = make_queues["queue1_id"]

    with pytest.raises(http_errors.Forbidden):
        queue_post_add(token, queue_id, post_id)


def test_success(
    simple_users: ISimpleUsers,
    make_queues: IMakeQueues,
    make_posts: IMakePosts,
):
    """
    We can send a post to multiple specialised queues
    """
    token = simple_users["mod"]["token"]
    post_id = make_posts["post1_id"]

    # Send post to "First Queue" specialised queue
    queue_id1 = make_queues["queue1_id"]
    queue_name1 = make_queues["queue_name1"]

    queue_post_add(token, queue_id1, post_id)
    post_queue_name = post_view(token, post_id)["queue"]
    assert post_queue_name == queue_name1

    queue = queue_post_list(token, queue_id1)
    assert post_id in queue["posts"]

    # Send post to "Second Queue" specialised queue
    queue_id2 = make_queues["queue2_id"]
    queue_name2 = make_queues["queue_name2"]

    queue_post_add(token, queue_id2, post_id)
    post_queue_name = post_view(token, post_id)["queue"]
    assert post_queue_name == queue_name2

    queue = queue_post_list(token, queue_id2)
    assert post_id in queue["posts"]

    # Post no longer in "First Queue" specialised queue
    queue = queue_post_list(token, queue_id1)
    assert post_id not in queue["posts"]


def test_add_post_to_view_only_queue(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Is an error raised when we try to move a post to a view_only queue
    using the taskboard/queue/post_add route?
    """
    token = simple_users["mod"]["token"]
    post_id = make_posts["post1_id"]
    queues = queue_list(token)['queues']
    closed_queue_id = get_queue(queues, "Closed queue")["queue_id"]
    with pytest.raises(http_errors.BadRequest):
        queue_post_add(token, closed_queue_id, post_id)


def test_add_post_from_view_only_queue(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Is an error raised when we try to move a post from a view_only queue
    using the taskboard/queue/post_add route?
    """
    token = simple_users["mod"]["token"]
    post_id = make_posts["post1_id"]
    queues = queue_list(token)['queues']
    main_queue_id = get_queue(queues, "Main queue")["queue_id"]

    close_post(token, post_id)

    with pytest.raises(http_errors.BadRequest):
        queue_post_add(token, main_queue_id, post_id)
