from collections import namedtuple, defaultdict

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

def generic_namedtuple_factory(cursor, row):
    """
    Usage:
    con.row_factory = namedtuple_factory
    """
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)
