# """
# # Tests / Integration / Browse / Delete Queue

# Tests for the deleting queues

# * Invalid ID
# * No permission
# * Delete queue success
# """

# import pytest
# from backend.types.identifiers import QueueId
# from backend.util.http_errors import BadRequest, Forbidden
# from backend.util import http_errors
# from ensemble_request.browse import post_create
# from ensemble_request.taskboard import (
#     queue_list,
#     post_list,
#     queue_post_add,
# )
# from tests.integration.conftest import (
#     ISimpleUsers,
#     IMakeQueues,
#     IMakePosts
# )


# def test_no_permission(
#     simple_users: ISimpleUsers,
#     make_queues: IMakeQueues,
#     make_posts: IMakePosts,
# ):
#     """
#     Is an error raised when a user without the permission to
#     delegate posts to specialised queues tries to do so?
#     """
#     token = simple_users["user"]["token"]
#     post_id = make_posts["post1_id"]
#     queue_id = make_queues["queue1_id"]

#     with pytest.raises(http_errors.Forbidden):
#         queue_post_add(token, queue_id, post_id)


# # def test_success(
# #     simple_users: ISimpleUsers,
# #     make_queues: IMakeQueues,
# # ):
# #     user_token = simple_users["user"]["token"]
# #     admin_token = simple_users["admin"]["token"]

# #     post_id = post_create(user_token, "heading", "text", [])["post_id"]
