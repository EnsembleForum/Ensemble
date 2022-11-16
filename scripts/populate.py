"""
# Scripts / Populate

Clears the server. then populates it with default data, which will be helpful
when showing off the project.
"""
import _helpers
import ensemble_request as ensemble
del _helpers

print("📝 Populating data - this will take a few seconds...")

# Initialise forum
############################################################

ensemble.debug.clear()
ada = ensemble.admin.init(
    address="http://localhost:5812/login",
    request_type="get",
    username_param="username",
    password_param="password",
    success_regex="true",
    username="admin1",
    password="admin1",
    email="admin1@example.com",
    # Wrote the first computer program
    name_first="Ada",
    name_last="Lovelace",
)

permissions = ensemble.admin.permissions.groups_list(
    ada["token"])["groups"]

admin_perm = permissions[0]["group_id"]
mod_perm = permissions[1]["group_id"]
user_perm = permissions[2]["group_id"]


# Register other users
############################################################

ensemble.admin.users.register(
    ada["token"],
    [
        {
            # Inventor of Python
            "name_first": "Guido",
            "name_last": "van Rossum",
            "username": "admin2",
            "email": "guido@example.com",
        },
        {
            # Inventor of C
            "name_first": "Dennis",
            "name_last": "Ritchie",
            "username": "admin3",
            "email": "dennis@example.com",
        },
    ],
    admin_perm,
)
guido = ensemble.auth.login("admin2", "admin2")
dennis = ensemble.auth.login("admin3", "admin3")

ensemble.admin.users.register(
    ada["token"],
    [
        {
            # Inventor of first computer
            "name_first": "Charles",
            "name_last": "Babbage",
            "username": "mod1",
            "email": "charles@example.com",
        },
        {
            # Turing machine
            "name_first": "Alan",
            "name_last": "Turing",
            "username": "mod2",
            "email": "alan@example.com",
        },
        {
            # Wrote the code that got astronauts to the moon
            "name_first": "Margaret",
            "name_last": "Hamilton",
            "username": "mod3",
            "email": "margaret@example.com",
        },
    ],
    mod_perm,
)
charles = ensemble.auth.login("mod1", "mod1")
alan = ensemble.auth.login("mod2", "mod2")
margaret = ensemble.auth.login("mod3", "mod3")

ensemble.admin.users.register(
    ada["token"],
    [
        {
            # Creator of Unix
            "name_first": "Brian",
            "name_last": "Kernighan",
            "username": "user1",
            "email": "brian@example.com",
        },
        {
            # Creator of Linux
            "name_first": "Linus",
            "name_last": "Torvalds",
            "username": "user2",
            "email": "linus@example.com",
        },
        {
            # Creator of the first compiler
            # Also did lots of debugging
            "name_first": "Grace",
            "name_last": "Hopper",
            "username": "user3",
            "email": "grace@example.com",
        },
        {
            # Creator of the world wide web
            "name_first": "Tim",
            "name_last": "Berners-Lee",
            "username": "user4",
            "email": "tim@example.com",
        },
        {
            # Founder of the GNU project
            "name_first": "Richard",
            "name_last": "Stallman",
            "username": "user5",
            "email": "richard@example.com",
        },
    ],
    user_perm,
)
brian = ensemble.auth.login("user1", "user1")
linus = ensemble.auth.login("user2", "user2")
grace = ensemble.auth.login("user3", "user3")
tim = ensemble.auth.login("user4", "user4")
richard = ensemble.auth.login("user5", "user5")


# Set up queues
############################################################

teamwork_queue = ensemble.taskboard.queue_create(
    ada["token"],
    "Teamwork issues",
)["queue_id"]
compiler_queue = ensemble.taskboard.queue_create(
    ada["token"],
    "Compiler issues",
)["queue_id"]
spec_queue = ensemble.taskboard.queue_create(
    ada["token"],
    "Spec clarifications",
)["queue_id"]


# Create a bunch of content
############################################################

seg_fault = ensemble.browse.post.create(
    brian["token"],
    "What does this error mean?",
    "Whenever I try to run my code I get a segmentation fault. Why is this "
    "programming language so difficult :(",
    [],
)
ensemble.browse.comment.create(
    linus["token"],
    seg_fault["post_id"],
    "Skill issue.",
)
seg_fault_practice = ensemble.browse.comment.create(
    dennis["token"],
    seg_fault["post_id"],
    "It's just a practice thing. I'm sure you'll figure it out eventually!",
)
ensemble.browse.reply.create(
    brian["token"],
    seg_fault_practice["comment_id"],
    "Thanks for the advice, I'll keep working on it"
)
ensemble.browse.comment.react(
    brian["token"],
    seg_fault_practice["comment_id"],
)

performance = ensemble.browse.post.create(
    guido["token"],
    "Why is my program so slow?",
    "It was really easy to write, but my assignment is taking ages to run.\n\n"
    "Is there anything I can do to speed it up?",
    [],
)
ensemble.browse.comment.create(
    grace["token"],
    performance["post_id"],
    "I created tools to avoid these issues years ago - the issue is that you "
    "chose a programming language that doesn't use them."
)
performance_ok = ensemble.browse.comment.create(
    charles["token"],
    performance["post_id"],
    "Don't worry, we don't have any requirements for performance in this "
    "course. As long as it gets there eventually it'll be fine!"
)
ensemble.browse.comment.accept(
    charles["token"],
    performance_ok["comment_id"],
)

teammates = ensemble.browse.post.create(
    margaret["token"],
    "My teammates aren't helping.",
    "The assignment is due in a few days, but I've had to write so much code "
    "myself. Is there anything I can do to get them working? I don't want it "
    "to crash and burn.\n\n"
    "This probably isn't historically accurate, but I need to fill the forum "
    "with something, so you'll just have to deal with it.",
    [],
    private=True,
)
ensemble.taskboard.queue_post_add(
    guido["token"],
    teamwork_queue,
    teammates["post_id"]
)
ensemble.browse.comment.create(
    guido["token"],
    teammates["post_id"],
    "Sorry to hear that. I've moved this to the teamwork queue, so we'll be "
    "able to keep track of things when it comes time to mark it. Feel free to "
    "keep editing your post with any updated info if the situation develops."
)

oss_assignment = ensemble.browse.post.create(
    richard["token"],
    "Are we allowed to share our assignments?",
    "I was thinking it'd be really cool if we could all share our assignments "
    "and work together on it! Are we allowed to do that?",
    []
)
ensemble.browse.comment.create(
    tim["token"],
    oss_assignment["post_id"],
    "Cool idea - I'll happily make a way we can share the work between our "
    "computers even if we're on the other side of the world!"
)
ensemble.browse.post.react(
    linus["token"],
    oss_assignment["post_id"],
)
oss_assignment_no = ensemble.browse.comment.create(
    charles["token"],
    oss_assignment["post_id"],
    "No. That is academic misconduct.",
)
ensemble.browse.comment.accept(
    charles["token"],
    oss_assignment_no["comment_id"],
)
ensemble.browse.reply.create(
    linus["token"],
    oss_assignment_no["comment_id"],
    "That's annoying. Guess I'll just have to write a very similar project "
    "but make it technically different enough that you can't do anything "
    "about it"
)


unix_files = ensemble.browse.post.create(
    linus["token"],
    "Wait so is everything supposed to be a file?",
    "Like,,, literally everything?",
    []
)
ensemble.browse.post.react(
    grace["token"],
    unix_files["post_id"],
)
unix_files_yes = ensemble.browse.comment.create(
    brian["token"],
    unix_files["post_id"],
    "Yes. Literally everything."
)
ensemble.browse.comment.react(
    linus["token"],
    unix_files_yes["comment_id"],
)
ensemble.browse.comment.react(
    richard["token"],
    unix_files_yes["comment_id"],
)
ensemble.browse.reply.create(
    alan["token"],
    unix_files_yes["comment_id"],
    "No, everything is a turing machine"
)

undefined_behaviour = ensemble.browse.post.create(
    grace["token"],
    "Why is there so much undefined behaviour in the assignment?",
    "A lot of it seems simple enough to define. I'd love to see some "
    "clarifications on how we should handle the authentication system, since "
    "the spec doesn't go into very much detail",
    []
)
ensemble.browse.post.react(
    richard["token"],
    undefined_behaviour["post_id"],
)
ensemble.browse.post.react(
    tim["token"],
    undefined_behaviour["post_id"],
)

ensemble.browse.post.create(
    guido["token"],
    "Assignment due soon!",
    "Just a reminder that your final assignment is due this Friday at 10 PM. "
    "Make sure you don't miss the deadline!",
    []
)
