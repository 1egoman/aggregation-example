from aggregation_utils import aggregate_current_state, create_changeset, create_reset

def deep_equal(a, b):
    assert a == b, "{} != {}".format(a, b)

deep_equal(
    aggregate_current_state([
        create_reset(foo='bar'),
        create_changeset('hello', 'world'),
    ]),
    {'foo': 'bar', 'hello': 'world'},
)

deep_equal(
    aggregate_current_state([
        create_reset(foo='bar', hello='world'),
        create_changeset('foo', 'baz'),
    ]),
    {'hello': 'world', 'foo': 'baz'},
)
