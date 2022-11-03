"""
# Backend / Routes / Browse / Comment View

Comment View routes
"""
import json
from flask import Blueprint, request
from backend.models.permissions import Permission
from backend.models.reply import Reply
from backend.models.comment import Comment
from backend.models.user import User
from backend.types.identifiers import CommentId
from backend.types.comment import ICommentFullInfo
from backend.types.react import IUserReacted
from backend.types.reply import IReplyId
from backend.util.tokens import uses_token

comment_view = Blueprint("comment_view", "comment_view")


@comment_view.get("")
@uses_token
def get_comment(user: User, *_) -> ICommentFullInfo:
    user.permissions.assert_can(Permission.PostView)
    comment = Comment(CommentId(request.args["comment_id"]))
    return comment.full_info(user)


@comment_view.post("/reply")
@uses_token
def reply(user: User, *_) -> IReplyId:
    user.permissions.assert_can(Permission.PostComment)
    data = json.loads(request.data)
    text: str = data["text"]
    comment = Comment(data["comment_id"])

    reply_id = Reply.create(user, comment, text).id

    return {"reply_id": reply_id}


@comment_view.put("/react")
@uses_token
def react(user: User, *_) -> IUserReacted:
    user.permissions.assert_can(Permission.PostView)
    data = json.loads(request.data)
    comment = Comment(data["comment_id"])
    comment.react(user)

    return {"user_reacted": comment.has_reacted(user)}
