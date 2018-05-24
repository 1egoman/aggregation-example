import datetime

from aggregation_utils import aggregate_current_state, create_changeset, create_reset

def main():
    entries = [
        create_reset(foo='bar', hello='world'),
        create_changeset('foo', 'baz'),
    ]

    print(aggregate_current_state(entries))

if __name__ == '__main__':
    main()
