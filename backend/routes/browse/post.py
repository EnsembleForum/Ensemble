"""
# Backend / Routes / Browse / Post View

Post View routes
"""
import json
from flask import Blueprint, request
from backend.models.notifications import (
    NotificationClosed,
    NotificationReacted,
    NotificationReported,
    NotificationDeleted,
)
from backend.models import Permission, Post, User, Queue, ExamMode, Tag
from backend.types.identifiers import PostId, TagId
from backend.types.post import (
    IPostFullInfo,
    IPostClosed,
    IPostBasicInfoList,
    IPostId,
)
from backend.types.react import IUserReacted
from backend.util import http_errors
from backend.util.tokens import uses_token

post = Blueprint("post", "post")


@post.get("/list")
@uses_token
def post_list(user: User, *_) -> IPostBasicInfoList:
    user.permissions.assert_can(Permission.PostView)
    search_term: str = request.args["search_term"]
    if len(search_term) > 0:
        posts_info = [p.basic_info(user)
                      for p in Post.search_posts(user, search_term)]
    else:
        posts_info = [p.basic_info(user) for p in Post.can_view_list(user)]

    return {"posts": posts_info}


@post.get("/view")
@uses_token
def view(user: User, *_) -> IPostFullInfo:
    user.permissions.assert_can(Permission.PostView)
    post_id = PostId(request.args["post_id"])
    post = Post(post_id)
    if not post.can_view(user):
        raise http_errors.Forbidden(
            "Do not have permissions to view this post"
        )
    return post.full_info(user)


@post.post("/create")
@uses_token
def create(user: User, *_) -> IPostId:
    user.permissions.assert_can(Permission.PostCreate)

    data = json.loads(request.data)
    heading: str = data["heading"]
    text: str = data["text"]
    tags = [Tag(i) for i in data["tags"]]
    private: bool = data["private"]
    anonymous: bool = data["anonymous"]

    if ExamMode.is_enabled() and not private:
        user.permissions.assert_can(Permission.PostOverrideExam)

    post_id = Post.create(user, heading, text, tags, private, anonymous).id

    return {"post_id": post_id}


@post.put("/edit")
@uses_token
def edit(user: User, *_) -> dict:
    user.permissions.assert_can(Permission.PostCreate)
    data = json.loads(request.data)
    post_id: PostId = data["post_id"]
    new_heading: str = data["heading"]
    new_text: str = data["text"]
    new_tags: list[TagId] = data["tags"]

    post = Post(post_id)

    if user != post.author:
        raise http_errors.Forbidden("Attempting to edit another user's post")

    if post.deleted:
        raise http_errors.BadRequest("Cannot edit a deleted post")

    post.heading = new_heading
    post.text = new_text
    post.tags = [Tag(t) for t in new_tags]

    # Send post back to main queue if it was previously closed
    if post.closed:
        if post.answered:
            post.queue = Queue.get_answered_queue()
        else:
            post.queue = Queue.get_main_queue()

    return {}


@post.delete("/delete")
@uses_token
def delete(user: User, *_) -> dict:
    user.permissions.assert_can(Permission.PostCreate)
    post = Post(PostId(request.args["post_id"]))

    if user != post.author:
        user.permissions.assert_can(Permission.DeletePosts)
        NotificationDeleted.create(
            post.author,
            post,
        )

    post.delete()
    return {}


@post.put("/react")
@uses_token
def react(user: User, *_) -> IUserReacted:
    user.permissions.assert_can(Permission.PostView)
    data = json.loads(request.data)
    post = Post(data["post_id"])
    post.react(user)

    if user != post.author:
        NotificationReacted.create(
            post.author,
            post,
        )

    return {"user_reacted": post.has_reacted(user)}


@post.put("/close")
@uses_token
def close_post(user: User, *_) -> IPostClosed:
    user.permissions.assert_can(Permission.ClosePosts)
    data = json.loads(request.data)
    post = Post(data["post_id"])
    post.closed_toggle()

    if user != post.author and post.closed:
        NotificationClosed.create(
            post.author,
            post,
        )

    return {"closed": post.closed}


@post.put("/report")
@uses_token
def report_post(user: User, *_):
    user.permissions.assert_can(Permission.ReportPosts)
    data = json.loads(request.data)
    post = Post(data["post_id"])
    post.queue = Queue.get_reported_queue()

    for u in User.all_where(
        lambda u: u.permissions.can(Permission.ViewReports)
    ):
        if u not in [user, post.author]:
            NotificationReported.create(u, post)

    return {}


@post.put("/unreport")
@uses_token
def unreport_post(user: User, *_):
    user.permissions.assert_can(Permission.ViewReports)
    data = json.loads(request.data)
    post = Post(data["post_id"])
    if post.answered is not None:
        post.queue = Queue.get_answered_queue()
    else:
        post.queue = Queue.get_main_queue()

    return {}
