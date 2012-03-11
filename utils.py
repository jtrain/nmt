import re
import sqlite3

def strip_tags(value):
    """Returns the given HTML with all tags stripped."""
    return re.sub(r'<[^>]*?>', '', value)

def make_namedtuple_factory(NamedTuple):
    def named_tuple_factory(cursor, row):
        try:
            return NamedTuple(*row)
        except TypeError:
            return row

    return named_tuple_factory
