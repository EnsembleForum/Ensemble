
# Miguel Guthridge

## Week 1

### Thursday

In week 1, we got into teams. Andrew and Neel were away, so they couldn't
participate in the discussion. I proposed that we do a course forum as a custom
project as I believe that is something I will be able to find motivation and
inspiration for. We drafted an initial project proposal with a few ideas.

* Exam mode
* Triage queue system

Although I came up with the initial idea for the triage queue, it was
developed, refined and transformed by the group to the point where I consider
it to be the work of the group.

## Week 2

### Monday

Our initial proposal was rejected as it wasn't clear that it was a big enough
workload. Sesi, Yuk and I worked to refine the system and give far more detail
on the complexities of our systems, however I fear we may have overcompensated
and become stuck with a highly complex project - we may need to reconsider our
goals if we realise they are unrealistic down the track. Our proposal this time
was accepted thankfully.

### Thursday

We also got access to the GitLab. I created an initial project structure
containing starter code as well as some dependencies we deemed essential. I
also helped to decide the tech stack we're using, particularly for the back-end
tooling. Hopefully I'll be able to use my experience with CI/CD to help
optimise our testing and deployment of the project.

## Week 3

### Monday

I made some initial progress on the project proposal. As of today, I've
completed a first draft of the background, but am still yet to do work on the
backend part of our tech stack. So far nobody else has started. Hopefully
they'll start soon so I can stop stressing.

I'll also do some work on getting a basic server running and sort out a folder
structure for the backend later.

### Tuesday

Added some starter code for the backend server, as well as documentation for
getting it to start. Build out a basic structure to contain all of the server
code.

### Thursday

Another team meeting - sorted out our interface design. Did lots of compromises
but I think we made the best decisions overall.

### Saturday

Team meeting online. Sesi, Yuk and I wrote tons and tons of user stories

### Sunday

Tested out MongoDB and found a bug that utterly breaks type-safety. Decided not
to use it as a result. Tried and failed to set up PostgreSQL - it's too painful
:(. Found a library (Piccolo) that looks really nice for interacting with it
though, so I wish we could use it.

## Week 4

### Monday

Wrote acceptance criteria. I had already written my sections earlier so I
didn't have much else to do. Sesi stayed up super late doing interface design,
and I feel kinda bad, but also I'm trash at interfaces so I don't think I'd be
much help.

### Tuesday

Spent hours fighting with databases. Turns out that Piccolo supports SQLite too
which is great, since it's super easy to set up (literally a `pip install`
away). Wrote a bit of a type system that wraps around it to hide database
queries from us when we're implementing the routes (since otherwise my brain
will collapse in a sobbing mess).

### Wednesday

Improved my type system some more and managed to get it working with a super
basic couple of routes, meaning we have the full framework in-place to be able
to write our server. I hope everyone else makes the same nice wrappers I am for
the rest of our database when we make it.

### Thursday

Another team meeting - we came up with all the routes for the entire server
and wrote input/output details for a few of the most important sprint 1 routes.
I found out how easy (and somewhat dodgy) it is to do zID authentication, so
we'll definitely implement that, although we'll need to mock it so we don't get
angry emails from CSE admins. I also went and wrote some test scripts which
will be helpful for testing the code. I plan to make a mock app for our login
info soon.

### Saturday

Wrote interface for sprint one routes in a team meeting. Implemented a mock
login server, which is based around the system that UNSW uses for
authentication. Also set up the system for registering users. Created a few
scripts for running the server and the tests at the same time.

### Sunday

Implemented system for registering users and logging in, including JWTs.

## Week 5

### Monday

Implemented a nice system for effectively checking tokens. Implement code for
checking user profiles.

### Tuesday

Implemented logout route.

### Wednesday

Miscellaneous improvements to auth code.

### Thursday

Project demonstration. Since the frontend code wasn't working correctly, things
were somewhat broken, which was a shame. I feel like a lot of my hard work went
unrecognised.

## Week 6

### Monday

Worked on permission management system.

### Tuesday

Completed the permission management system. Spent >4 hours trying to debug a
deadlock in the test script.

### Wednesday

Deadlock fixed, god it was painful to debug.

### Friday

Implement a system so that detailed error information is given as JSON,
including backtraces. This means that better debugging can be done for failing
tests, and more detailed error information can be given by the frontend.

### Saturday

Did quality of life improvements to the tests:

* The name of each test echoes at the start of the test, which makes it easier
  to track down failures in test output.

* Test outputs are uploaded as artifacts

## Week 7

I was super busy for the majority of this week with another assignment so I
didn't get a huge amount done.

### Thursday

Spent roughly 2.5 hours helping Andrew improve queue code - we finally got it
merged, although it was unfortunately over 2 weeks later than it should have
been.

### Friday

General maintenance of project.

## Week 8

Was super busy again, this time with CSE Revue. Didn't get much done again.

### Friday

Minor improvements for some return types to make things easier for the
frontend.

### Sunday

Added a few more routes to make it easier for the frontend dynamically hide
content which users don't have permission to access.

## Week 9

### Monday

Started work on notification support. Implemented an advanced model to
represent all kinds of notifications. Currently doesn't work, but I will debug
it tomorrow.

### Friday

Been super busy dealing with COMP1531 marking, so didn't get much done before
today. I fixed tons of bugs with notifications. Some kinds of notifications
require more code to be implemented, so I'll need to mark their tests as xfail
until the required routes are added.

### Saturday

Finished off notifications and got them merged. Andrew wasn't getting his work
on user profiles done in time, so I took over that and refactored the code that
needed improvement, as well as rewriting all the tests. The code should be much
more reliable and versatile now.

## Week 10

### Monday

Implemented queue following, and the notifications associated with that.
Because Yuk finished implementing deletions for comments and replies, I was
able add support for those notifications.

### Tuesday

Various bugs squashed. Added code coverage to the CI/CD pipeline. Helped Yuk
with finishing off the last bits of work. Worked on documentation, especially
for the report.

### Wednesday

A little more polishing up. More work on the final report.

### Thursday

Presentation day. Went pretty well overall I think!

### Friday

Final report submitted!
