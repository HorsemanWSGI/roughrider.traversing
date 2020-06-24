from roughrider.traversing import DEFAULT, VIEW
from roughrider.traversing.parsing import parse_path, create_path


def test_parse():
    """Parse a path to a stack, default namespaces.
    """
    assert ([(DEFAULT, 'a'),
             (DEFAULT, 'b'),
             (DEFAULT, 'c')] ==
            list(parse_path('/a/b/c')))
    assert list(parse_path('/')) == []
    assert list(parse_path('')) == []


def test_multi_slash():
    assert parse_path('/a/b/c') == parse_path('/a///b//c')
    assert parse_path('/a/b/c') == parse_path('/a/b/c/')


def test_create():
    assert ('/a/b/c' ==
            create_path([
                (DEFAULT, 'a'),
                (DEFAULT, 'b'),
                (DEFAULT, 'c')]))


def test_parse_ns():
    """Parse a path to a stack with namespaces.
    """
    assert ([(DEFAULT, 'a'),
             (DEFAULT, 'b'),
             (VIEW, 'c')] ==
            list(parse_path('/a/b/++view++c')))


def test_create_ns():
    assert ('/a/b/++view++c' ==
            create_path([
                (DEFAULT, 'a'),
                (DEFAULT, 'b'),
                (VIEW, 'c')]))


def test_parse_ns_shortcut():
    assert ([(DEFAULT, 'a'),
             (DEFAULT, 'b'),
             (VIEW, 'c')] ==
            list(parse_path('/a/b/@@c', shortcuts={'@@': VIEW})))


def test_create_ns_shortcut():
    assert ('/a/b/@@c' ==
            create_path([
                (DEFAULT, 'a'),
                (DEFAULT, 'b'),
                (VIEW, 'c')], shortcuts={'@@': VIEW}))


def test_parse_ns_shortcut_not_at_beginning():
    # shortcuts should be at the beginning of a step to be recognized
    assert ([(DEFAULT, 'a'),
             (DEFAULT, 'b'),
             (DEFAULT, 'a@@c')] ==
            list(parse_path('/a/b/a@@c', shortcuts={'@@': VIEW})))


def test_create_ns_shortcut_not_at_beginning():
    assert ('/a/b/a@@c' ==
            create_path([
                (DEFAULT, 'a'),
                (DEFAULT, 'b'),
                (DEFAULT, 'a@@c')], shortcuts={'@@': VIEW}))


def test_create_ns_weird_no_close():
    # a namespace that opens but doesn't close
    assert ('/a/b/++c' ==
            create_path([
                (DEFAULT, 'a'),
                (DEFAULT, 'b'),
                (DEFAULT, '++c')]))


def test_parse_ns_weird_no_close():
    assert ([(DEFAULT, 'a'),
             (DEFAULT, 'b'),
             (DEFAULT, '++c')] ==
            list(parse_path('/a/b/++c')))


def test_parse_ns_weird_no_open():
    # a namespace that closes but doesn't open
    assert ([(DEFAULT, 'a'),
             (DEFAULT, 'b'),
             (DEFAULT, 'view++c')] ==
            list(parse_path('/a/b/view++c')))


def test_create_ns_weird_no_open():
    # a namespace that closes but doesn't open
    assert ('/a/b/view++c' ==
            create_path([
                (DEFAULT, 'a'),
                (DEFAULT, 'b'),
                (DEFAULT, 'view++c')]))
