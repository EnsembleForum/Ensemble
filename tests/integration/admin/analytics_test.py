from ensemble_request.admin.analytics import get_analytics
from tests.integration.conftest import ISimpleUsers, IMakePosts


def test_mod_mark_accepted(
    simple_users: ISimpleUsers,
    make_posts: IMakePosts
):
    admin_token = simple_users["admin"]["token"]
    admin_id = simple_users["admin"]["user_id"]

    data = get_analytics(admin_token)

    assert len(data["top_posters"]) == 1
    assert data["top_posters"][0] == {
        "user_id": admin_id,
        "count": 2
    }
