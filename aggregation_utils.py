import datetime

CHANGESET = 'CHANGESET'
RESET_STATE = 'RESET_STATE'

def create_changeset(key, value):
    changes = {}
    changes[key] = value
    return {"type": CHANGESET, "timestamp": datetime.datetime.now(), "changes": changes}

def create_reset(**state):
    return {"type": RESET_STATE, "timestamp": datetime.datetime.now(), "state": state}

def merge(a, b):
    """
    Given two dictionaries, perform a merge between them. A merge is defined as taking all keys in
    the second collection and adding then to the first collection such that any duplicate key in the
    second collection will override an already-set key in the first collection.

    >>> merge({"foo": "bar"}, {"hello": "world"})
    {"foo": "bar", "hello": "world"}
    >>> merge({"foo": "bar"}, {"foo": "something else"})
    {"foo": "something else"}
    """
    result = dict(a)

    for key, value in b.items():
        result[key] = value

    return result

def aggregate_current_state(entries):
    """
    Given a mixed list of CHANGESETs and RESET_STATEs, aggregate them to determine the current state
    of the system.
    """

    # Find the most recent "reset"
    most_recent_reset = None
    for potential_reset in entries[::-1]: # https://stackoverflow.com/a/3705676/4115328
        if potential_reset["type"] == RESET_STATE:
            most_recent_reset = potential_reset
            break

    if most_recent_reset is None:
        raise Exception(
            'No resets were found in the passed list of entries. '
            'At least one reset is required in order to perform an aggregation.'
        )

    # Set the initial state to the last reset value
    state = most_recent_reset["state"]

    # Aggregate all changesets after this reset in order to compute the current state.
    most_recent_reset_index = entries.index(most_recent_reset)
    all_changes_after_reset = entries[most_recent_reset_index+1:]

    # Perform the aggregation.
    for changeset in all_changes_after_reset:
        state = merge(state, changeset["changes"])

    return state
