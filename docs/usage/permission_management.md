
# Permission management

We have created an extremely advanced system for managing user permissions,
which can be used to get fine-grained control over forum moderation. The
permissions are defined using groups, which can be granted or denied certain
permissions. Upon starting the server, permission groups are created for
admins, moderators and users, all with sensible defaults. However, the
permission management page can be used to modify the permissions of these
groups, excluding the admin group which will always be granted every
permission. If required, unneeded groups can be deleted, and new groups can be
created.

If even more fine-grained control over permissions is required, we also allow
for permissions to be overridden for individual users. By navigating to the
users section and selecting a user, you can see that they have permissions
that they inherit from their group. If required, an administrator can uncheck
the inherited option for a permission and then manually override those
permissions for that user.

We imagine that our default settings will be perfect for most course
administrators, but that taking advantage of the deep control our system gives
over permissions will be very simple to do if required. For example, if a
student is posting content that is inappropriate for a course forum, their
permission to create posts can be disabled without preventing them from
accessing the forum and viewing other content.

Note that when describing permissions in other sections, we consider
moderators to be a specialisation of users, and administrators to be a
specialisation of moderators. As such, unless specified otherwise, if we say
“users can do x”, this means that moderators and administrators can also do x;
and if we say “moderators can do y”, that means that administrators can also
do y. When we describe these permissions, we are also assuming that the
permission settings have been left in a default configuration. It is entirely
possible to grant access to any of the features listed to other permission
groups.
