
# Routes

## Overview

* debug
    * **echo** (echo to console)
    * **clear** (clear database)
    * **shutdown** (shutdown server)

* auth
    * **login**
    * **register** (register if allowed)
    * **logout**
    * **password_reset**

* admin
    * **is_first_run** (returns whether the server is empty)
    * users
        * **register** (bulk user registration)
        * **all** (list of all users (perhaps paged))
    * permissions
        * **list_permissions** (list of available permissions)
        * **get_permissions** (get permissions of a user)
        * **set_permissions** (set permissions of a user)
        * **set_group** (change the group of a user)
        * groups
            * **make** (make a permission group)
            * **list** (list available permission groups)
            * **edit** (edit a permission group)
            * **remove** (remove an empty permission group)
    * auth
        * **get_config** (return config for auth system)
        * **set_config** (edit config for auth system)

* browse
    * **post_list** (get list of posts, incl. basic details of all)
        * **filter** (filter posts & search)
    * **create** (make a post or comment)
    * **post_view** (view a single post or comment)
        * **edit** (edit a post, incl reopening old posts)
        * **self_delete** (delete your own post)
        * **comment** (post a comment)
        * **react** (add a reaction - me too)
        * **report** (report a post)
        * **close** (close a post)
        * **mod_delete** (mod deletes post)
    * **comment_view**
        * **edit** (edit a comment)
        * **self_delete** (delete your own comment)
        * **comment** (reply to this comment)
        * **react** (add a reaction - me too)
        * **report** (report a post)
        * **close** (close a post)
        * **mod_delete** (mod deletes post)
        * **accept** (OP accepts as answer)

* taskboard
    * **queue_list** (list of queue IDs and names)
        * **create**
        * **delete**
    * queue
        * **post_list** (list of posts in the queue)
        * **post_add** (add post to queue, removing from others)

* notifications
    * **list**

## Starting state

When the server is started with an empty datastore:

* If no users registered, `/admin/is_first_run` returns
  `{"value": true}`
* When this happens, `/admin/auth/set_config` is accessible
  without authentication.
* Frontend user can then specify a configuration for the
  authentication system.
* They also specify their username and password, which are
  validated (allowing the configuration to be tested and changed
  if required)
* When the authentication is passed, their user is created as an
  admin and it is no-longer in first-run.
