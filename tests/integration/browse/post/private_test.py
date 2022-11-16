"""
# Tests / Integration / Browse / Create
# Tests / Integration / Browse / Post List
# Tests / Integration / Browse / Post View

Tests for creating and viewing private posts

* Test for author of private post able to see his private post
* Test for mods and admins being able to see private posts
* Test for author of a private post still able to see public posts
* Test for users who do not have permission to view private posts can only view
  public posts
"""
import pytest
from ...conftest import ISimpleUsers, IAllUsers
from backend.util import http_errors
from ensemble_request.browse import post_list, post_create, post_view


def test_create_one_post_list(simple_users: ISimpleUsers):
    """
    Can we create a private post and can the author get it successfully?
    """
    token = simple_users["user"]["token"]
    heading = "First heading"
    text = "First text"
    tags: list[int] = []
    post_id = post_create(token, heading, text, tags, private=True)["post_id"]

    posts = post_list(token)
    assert len(posts["posts"]) == 1
    post = posts["posts"][0]
    assert post_id == post["post_id"]
    assert heading == post["heading"]
    assert tags == post["tags"]
    assert post["me_too"] == 0
    assert post["private"]


def test_diff_users_private_post_list(all_users: IAllUsers):
    """
    Can users with permissions to view private posts
    view private posts in post_list?
    """
    # User 1 creates a private post
    user_token1 = all_users["users"][0]["token"]
    heading = "First heading"
    text = "First text"
    tags: list[int] = []
    post_id1 = post_create(user_token1, heading,
                           text, tags, private=True)["post_id"]

    # User 2 creates a public post
    user_token2 = all_users["users"][1]["token"]
    heading = "Second heading"
    text = "Second text"
    post_id2 = post_create(user_token2, heading,
                           text, tags, private=False)["post_id"]

    # User 1 can view both posts
    posts = post_list(user_token1)["posts"]
    assert len(posts) == 2
    post_ids = sorted([p["post_id"] for p in posts])
    assert post_ids == sorted([post_id1, post_id2])

    # User 2 cannot view User 1's post
    posts = post_list(user_token2)["posts"]
    assert len(posts) == 1
    post_ids = sorted([p["post_id"] for p in posts])
    assert post_ids == sorted([post_id2])

    # Admin can view both posts
    admin_token = all_users["admins"][0]["token"]
    posts = post_list(admin_token)["posts"]
    assert len(posts) == 2
    post_ids = sorted([p["post_id"] for p in posts])
    assert post_ids == sorted([post_id1, post_id2])

    # Mod can view both posts
    mod_token = all_users["mods"][0]["token"]
    posts = post_list(mod_token)["posts"]
    assert len(posts) == 2
    post_ids = sorted([p["post_id"] for p in posts])
    assert post_ids == sorted([post_id1, post_id2])


def test_post_view_diff_users(all_users: IAllUsers):
    """
    Can users with permissions to view private posts
    view private posts in post_view?
    """
    user_token1 = all_users["users"][0]["token"]
    user_token2 = all_users["users"][1]["token"]
    admin_token = all_users["admins"][0]["token"]
    mod_token = all_users["mods"][0]["token"]

    # User 1 creates a private post
    heading = "heading"
    text = "text"
    tags: list[int] = []
    post_id = post_create(user_token1, heading,
                          text, tags, private=True)["post_id"]

    # User 1 can view his own post
    post = post_view(user_token1, post_id)
    assert post["heading"] == heading
    assert post["text"] == text
    assert post["comments"] == []
    assert post["tags"] == []
    assert post["me_too"] == 0
    assert post["private"]

    # Admin can view User 1's post
    assert post_view(admin_token, post_id)

    # Mod can view User 1's post
    assert post_view(mod_token, post_id)

    # User 2 cannot view User 1's post
    with pytest.raises(http_errors.Forbidden):
        post_view(user_token2, post_id)
