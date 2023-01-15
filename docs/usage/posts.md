
# Posting on the forum

Note that to quickly test the following features, we have added a script to
quickly generate some content to fill the forum. If you start the server then
run the script `python scripts/populate.py`, the server will be set up and
populated with data. You can login as ***admin1***, ***mod1***, or ***user1***
(with the passwords matching the usernames) to see the forum from the various
perspectives that the default roles offer.

At the core of Ensemble is posts. They act as a way for users to ask questions
on the forum. To create a post, the “New Post” button in the bottom right
should be used. When a user has written their post, they can submit it, and it
will appear in the browse section where other users can answer it.

There are various systems for interacting with posts, which are used to foster
engagement in the forum.

## Comments and replies

If a user wishes to answer a question, they can create a comment on it by
clicking the reply button. Users can also reply to comments to create nested
discussions.

## Accepting comments

If a comment adequately addresses a user’s question, that user can accept the
comment, which marks the post as answered, as well as highlighting the comment
that was accepted. Moderators can accept comments on any post, which can be
used to ensure that time isn’t wasted browsing through questions which have
already been addressed. When a post is answered, it will appear green in the
post list to differentiate it.

## Reacting to posts, comments and replies

On each post, there is a “me too” button which can be pressed by any user to
indicate that they have the same question. On comments and replies, there is a
“thanks” button which can be pressed by any user to thank the author for their
help. Comments on a post are sorted by the amount of thanks they have
received, which ensures that the most helpful comments rise to the top.
Replies are always shown in chronological order to maintain the flow of the
conversation.
