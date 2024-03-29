import pytest
from backend.util import http_errors
from ensemble_request.admin.analytics import get_analytics
from tests.integration.conftest import ISimpleUsers, IMakePosts
from ensemble_request.browse import (
    post,
    comment,
    reply
)


def get_group_stats_by_name(group_data, name):
    for g in group_data:
        if g["permission_group_name"] == name:
            return g["stats"]
    return None


def test_mod_no_permission(
    simple_users: ISimpleUsers,
):
    """
    Mods do not have permission to view analytics
    """
    with pytest.raises(http_errors.Forbidden):
        get_analytics(simple_users["mod"]["token"])


def test_user_no_permission(
    simple_users: ISimpleUsers
):
    """
    Users do not have permission to view analytics
    """
    with pytest.raises(http_errors.Forbidden):
        get_analytics(simple_users["user"]["token"])


def test_total_posts(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Do we get the correct total number of posts?
    """
    token = simple_users["admin"]["token"]

    assert get_analytics(token)["total_posts"] == 2


def test_total_comments(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Do we get the correct total number of comments?
    """
    admin_token = simple_users["admin"]["token"]
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]

    post_id1 = make_posts["post1_id"]
    post_id2 = make_posts["post2_id"]

    for _ in range(3):
        comment.create(user_token, post_id1, "hello")

    for _ in range(2):
        comment.create(mod_token, post_id2, "hello")

    assert get_analytics(admin_token)["total_comments"] == 5


def test_total_replies(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Do we get the correct total number of comments?
    """
    admin_token = simple_users["admin"]["token"]
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]

    post_id1 = make_posts["post1_id"]
    post_id2 = make_posts["post2_id"]
    comment_id1 = comment.create(user_token, post_id1, "hello")["comment_id"]
    comment_id2 = comment.create(mod_token, post_id2, "hello")["comment_id"]

    for _ in range(3):
        reply.create(user_token, comment_id1, "hello")

    for _ in range(2):
        reply.create(mod_token, comment_id2, "hello")

    assert get_analytics(admin_token)["total_replies"] == 5


def test_all_top_posters(
    simple_users: ISimpleUsers
):
    """
    Are the stats for the top posters among everyone on the forum correct?
    """
    admin_token = simple_users["admin"]["token"]
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]
    admin_id = simple_users["admin"]["user_id"]
    user_id = simple_users["user"]["user_id"]
    mod_id = simple_users["mod"]["user_id"]

    # User has 2 posts
    for _ in range(2):
        post.create(user_token, "heading", "text", [])

    # Mod and admin each have 1 post
    post.create(mod_token, "heading", "text", [])
    post.create(admin_token, "heading", "text", [])

    data = get_analytics(admin_token)

    all_data = data["all_users"]["top_posters"]
    # Sorted from most to least number of posts, then by first name
    assert [i["user_id"] for i in all_data] == [user_id, admin_id, mod_id]
    assert [i["count"] for i in all_data] == [2, 1, 1]

    groups_data = data["groups"]

    admin_data = get_group_stats_by_name(
        groups_data, "Administrator")["top_posters"]
    assert [i["user_id"] for i in admin_data] == [admin_id]
    assert [i["count"] for i in admin_data] == [1]

    mod_data = get_group_stats_by_name(
        groups_data, "Moderator")["top_posters"]
    assert [i["user_id"] for i in mod_data] == [mod_id]
    assert [i["count"] for i in mod_data] == [1]

    user_data = get_group_stats_by_name(
        groups_data, "User")["top_posters"]
    assert [i["user_id"] for i in user_data] == [user_id]
    assert [i["count"] for i in user_data] == [2]


def test_all_top_commenters(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Are the stats for the top commenters among everyone on the forum correct?
    """
    admin_token = simple_users["admin"]["token"]
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]
    admin_id = simple_users["admin"]["user_id"]
    user_id = simple_users["user"]["user_id"]
    mod_id = simple_users["mod"]["user_id"]

    post_id = make_posts["post1_id"]

    # User has 2 comments
    for _ in range(2):
        comment.create(user_token, post_id, "text")

    # Mod and admin each have 1 post
    comment.create(admin_token, post_id, "text")
    comment.create(mod_token, post_id, "text")

    data = get_analytics(admin_token)

    all_data = data["all_users"]["top_commenters"]
    # Sorted from most to least number of posts, then by first name
    assert [i["user_id"] for i in all_data] == [user_id, admin_id, mod_id]
    assert [i["count"] for i in all_data] == [2, 1, 1]

    groups_data = data["groups"]

    admin_data = get_group_stats_by_name(
        groups_data, "Administrator")["top_commenters"]
    assert [i["user_id"] for i in admin_data] == [admin_id]
    assert [i["count"] for i in admin_data] == [1]

    mod_data = get_group_stats_by_name(
        groups_data, "Moderator")["top_commenters"]
    assert [i["user_id"] for i in mod_data] == [mod_id]
    assert [i["count"] for i in mod_data] == [1]

    user_data = get_group_stats_by_name(
        groups_data, "User")["top_commenters"]
    assert [i["user_id"] for i in user_data] == [user_id]
    assert [i["count"] for i in user_data] == [2]


def test_all_top_repliers(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Are the stats for the top repliers among everyone on the forum correct?
    """
    admin_token = simple_users["admin"]["token"]
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]
    admin_id = simple_users["admin"]["user_id"]
    user_id = simple_users["user"]["user_id"]
    mod_id = simple_users["mod"]["user_id"]

    post_id = make_posts["post1_id"]
    comment_id = comment.create(user_token, post_id, "text")["comment_id"]

    # User has 2 comments
    for _ in range(2):
        reply.create(user_token, comment_id, "text")

    # Mod and admin each have 1 post
    reply.create(admin_token, comment_id, "text")
    reply.create(mod_token, comment_id, "text")

    data = get_analytics(admin_token)

    all_data = data["all_users"]["top_repliers"]
    # Sorted from most to least number of posts, then by first name
    assert [i["user_id"] for i in all_data] == [user_id, admin_id, mod_id]
    assert [i["count"] for i in all_data] == [2, 1, 1]

    groups_data = data["groups"]

    admin_data = get_group_stats_by_name(
        groups_data, "Administrator")["top_repliers"]
    assert [i["user_id"] for i in admin_data] == [admin_id]
    assert [i["count"] for i in admin_data] == [1]

    mod_data = get_group_stats_by_name(
        groups_data, "Moderator")["top_repliers"]
    assert [i["user_id"] for i in mod_data] == [mod_id]
    assert [i["count"] for i in mod_data] == [1]

    user_data = get_group_stats_by_name(
        groups_data, "User")["top_repliers"]
    assert [i["user_id"] for i in user_data] == [user_id]
    assert [i["count"] for i in user_data] == [2]


def test_all_top_me_too(simple_users: ISimpleUsers):
    """
    Are the stats for the top me_too's among everyone on the forum correct?
    """
    admin_token = simple_users["admin"]["token"]
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]
    admin_id = simple_users["admin"]["user_id"]
    user_id = simple_users["user"]["user_id"]
    mod_id = simple_users["mod"]["user_id"]

    user_post = post.create(user_token, "heading", "text", [])["post_id"]
    mod_post = post.create(mod_token, "heading", "text", [])["post_id"]
    admin_post = post.create(admin_token, "heading", "text", [])["post_id"]

    # User has 2 me_too's
    post.react(mod_token, user_post)
    post.react(admin_token, user_post)

    # Mod and admin each have 1 post
    post.react(user_token, mod_post)
    post.react(user_token, admin_post)

    data = get_analytics(admin_token)

    all_data = data["all_users"]["top_me_too"]
    # Sorted from most to least number of posts, then by first name
    assert [i["user_id"] for i in all_data] == [user_id, admin_id, mod_id]
    assert [i["count"] for i in all_data] == [2, 1, 1]

    groups_data = data["groups"]

    admin_data = get_group_stats_by_name(
        groups_data, "Administrator")["top_me_too"]
    assert [i["user_id"] for i in admin_data] == [admin_id]
    assert [i["count"] for i in admin_data] == [1]

    mod_data = get_group_stats_by_name(
        groups_data, "Moderator")["top_me_too"]
    assert [i["user_id"] for i in mod_data] == [mod_id]
    assert [i["count"] for i in mod_data] == [1]

    user_data = get_group_stats_by_name(
        groups_data, "User")["top_me_too"]
    assert [i["user_id"] for i in user_data] == [user_id]
    assert [i["count"] for i in user_data] == [2]


def test_all_top_thanks(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    """
    Are the stats for the top thanks among everyone on the forum correct?
    """
    admin_token = simple_users["admin"]["token"]
    user_token = simple_users["user"]["token"]
    mod_token = simple_users["mod"]["token"]
    admin_id = simple_users["admin"]["user_id"]
    user_id = simple_users["user"]["user_id"]
    mod_id = simple_users["mod"]["user_id"]

    post_id = make_posts["post1_id"]
    comment_id = comment.create(user_token, post_id, "text")["comment_id"]
    user_reply = reply.create(user_token, comment_id, "text")["reply_id"]
    mod_reply = reply.create(mod_token, comment_id, "text")["reply_id"]
    admin_reply = reply.create(admin_token, comment_id, "text")["reply_id"]

    reply.react(user_token, mod_reply)
    reply.react(user_token, admin_reply)
    comment.react(mod_token, comment_id)
    reply.react(mod_token, user_reply)
    reply.react(admin_token, user_reply)

    data = get_analytics(admin_token)

    all_data = data["all_users"]["top_thanks"]
    # Sorted from most to least number of posts, then by first name
    assert [i["user_id"] for i in all_data] == [user_id, admin_id, mod_id]
    assert [i["count"] for i in all_data] == [3, 1, 1]

    groups_data = data["groups"]

    admin_data = get_group_stats_by_name(
        groups_data, "Administrator")["top_thanks"]
    assert [i["user_id"] for i in admin_data] == [admin_id]
    assert [i["count"] for i in admin_data] == [1]

    mod_data = get_group_stats_by_name(
        groups_data, "Moderator")["top_thanks"]
    assert [i["user_id"] for i in mod_data] == [mod_id]
    assert [i["count"] for i in mod_data] == [1]

    user_data = get_group_stats_by_name(
        groups_data, "User")["top_thanks"]
    assert [i["user_id"] for i in user_data] == [user_id]
    assert [i["count"] for i in user_data] == [3]
