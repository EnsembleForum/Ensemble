from ensemble_request.admin.analytics import get_analytics
from tests.integration.conftest import ISimpleUsers, IMakePosts
from ensemble_request.browse import (
    post_react,
    post_view,
    post_create,
    add_comment,
    add_reply,
    reply_react,
    comment_react
)


def test_mod_mark_accepted(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    admin_token = simple_users["admin"]["token"]
    admin_id = simple_users["admin"]["user_id"]

    data = get_analytics(admin_token)

    assert len(data["staff"]["top_posters"]) == 1
    assert data["staff"]["top_posters"][0] == {
        "user_id": admin_id,
        "count": 2
    }
    assert data["total_posts"] == 2
    assert data["total_comments"] == 0


def test_react_multiple_users1(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Successful reacts and un-reacts by multiple users
    """
    token1 = simple_users["user"]["token"]
    token2 = simple_users["mod"]["token"]
    post_id = make_posts["post1_id"]

    post_id1 = make_posts["post2_id"]

    post_react(token1, post_id)["user_reacted"]

    post_react(token2, post_id)

    post_react(token2, post_id1)
    
    post_create(token2, "heading", "text", [])
    post_create(token1, "heading", "text", [])
    

    admin_token = simple_users["admin"]["token"]
    admin_id = simple_users["admin"]["user_id"]

    data = get_analytics(admin_token)
    staff_data = data["staff"]
    student_data = data["students"]

    assert len(staff_data["top_posters"]) == 2
    
    assert staff_data["top_me_too"][0]["user_id"] == admin_id
    assert staff_data["top_me_too"][0]["count"] == 3
    assert len(staff_data["top_me_too"]) == 1

    assert len(student_data["top_posters"]) == 1
    
    assert len(data["all_users"]["top_posters"]) == 3
    
    
def test_react_multiple_users(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts,
):
    """
    Successful reacts and un-reacts by multiple users
    """
    token1 = simple_users["user"]["token"]
    token2 = simple_users["mod"]["token"]
    post_id = make_posts["post1_id"]
    comment_id = add_comment(token2, post_id, "first")["comment_id"]
    reply_id = add_reply(token1, comment_id, "helo")["reply_id"]

    reply_react(token1, reply_id)

    reply_react(token2, reply_id)
    
    comment_react(token1, comment_id)

    admin_token = simple_users["admin"]["token"]
    admin_id = simple_users["admin"]["user_id"]

    data = get_analytics(admin_token)
    staff_data = data["staff"]
    student_data = data["students"]
    
    assert student_data["top_thanks"][0]["user_id"] == simple_users["user"]["user_id"]
    assert student_data["top_thanks"][0]["count"] == 2