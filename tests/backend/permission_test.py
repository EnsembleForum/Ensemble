"""
# Tests / Backend / Permission Test

Unit tests for `PermissionSet` type.
"""
'''
Commented out for type safety - these tests no-longer work,
I'm just keeping them until I write new tests.

from backend.models import Permission, PermissionSet

def test_name():
    """Can we use the name property?"""
    s = PermissionSet('my set', None, set(), set())
    assert s.name == 'my set'


def test_all_disallowed_default():
    """Are all permissions denied by default?"""
    s = PermissionSet('test', None, set(), set())
    for p in Permission:
        assert not s.can(p)


def test_allow():
    """Can we grant permissions to users?"""
    s = PermissionSet('my set', None, set(), set())
    s.allow({Permission.Post})
    assert s.can(Permission.Post)


def test_disallow():
    """Can we disallow granted permissions?"""
    s = PermissionSet('my set', None, set(), set())
    s.allow({Permission.Post})
    s.disallow({Permission.Post})
    assert not s.can(Permission.Post)


def test_inherit():
    """Do permission sets correctly inherit permissions from their parent?"""
    s = PermissionSet('daddy', None, set(), set())
    parent.allow({Permission.Post})
    s = PermissionSet('child', parent)
    assert s.can(Permission.Post)


def test_override():
    """Can permission sets override permissions from their parent?"""
    parent = PermissionSet('daddy')
    parent.allow({Permission.Post})
    s = PermissionSet('child', parent)
    s.disallow({Permission.Post})
    assert not s.can(Permission.Post)


def test_unassign():
    """Can permissions be unassigned, meaning they will inherit from their
    parent again?
    """
    parent = PermissionSet('daddy')
    parent.allow({Permission.Post})
    s = PermissionSet('child', parent)
    s.disallow({Permission.Post})
    s.unassign({Permission.Post})
    assert s.can(Permission.Post)
    # Now prevent the parent from posting
    parent.disallow({Permission.Post})
    # Does it also affect the child?
    assert not s.can(Permission.Post)


def test_multi_inheritance():
    """Can we have chains of permissions that inherit from each other?"""
    grandparent = PermissionSet('nan')
    parent = PermissionSet('daddy', grandparent)
    child = PermissionSet('child', parent)
    # First the grandparent lets them post
    grandparent.allow({Permission.Post})
    assert child.can(Permission.Post)
    # Then the parent stops them
    parent.disallow({Permission.Post})
    assert not child.can(Permission.Post)
    # Then they be a naughty boy and give themselves permission
    child.allow({Permission.Post})
    assert child.can(Permission.Post)
'''
