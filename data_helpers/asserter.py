__author__ = 'jp'

from nose.tools import (assert_equal, assert_items_equal,assert_dict_equal)
from datadiff import diff

def check_items_equal(actual_value, expected_value, msg=""):
    """
    :param actual_value:
    :param expected_value:
    :param msg:
    :return:

    """
    if isinstance(actual_value, (list, dict, tuple)):
        msg = "\n" + msg + "\n\nDiffering items :\nFirst Argument(Usually Actual) marked with (-)," \
                           "Second Argument(Usually Expected) marked with (+)"
    else:
        msg = "\n" + msg + "\nFirst Argument(Usually Actual), Second Argument(Usually Expected)"

    if not actual_value or not expected_value:
        assert_equal(actual_value, expected_value, u"{}\n{} != {}".format(msg, actual_value, expected_value))

    elif isinstance(actual_value, (list, tuple)):
        assert_items_equal(sorted(actual_value), sorted(expected_value),
                           u"{}\n{}".format(msg, unicode(diff(sorted(actual_value),
                                                          sorted(expected_value)))))
    elif isinstance(actual_value, dict):
        assert_dict_equal(actual_value, expected_value,
                     u"{}\n{}".format(msg, unicode(diff(actual_value, dict(expected_value)))))
    elif isinstance(actual_value, (str, bool)):
        assert_equal(actual_value, expected_value,
                     u"{}\n{} != {}".format(msg, unicode(actual_value), unicode(expected_value)))
    else:
        assert_equal(actual_value, expected_value,
                     u"{}\n{} != {}".format(msg, actual_value, expected_value))
