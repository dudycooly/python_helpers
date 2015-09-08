__author__ = 'jp'

from nose.tools import (assert_equal, assert_items_equal,assert_dict_equal)
from datadiff import diff

def filter_list_of_dict_with_attr_value(list_of_dict, attribute, value):
    """Return matches for item with matching attribute value"""
    if list_of_dict:
        return [datadict for datadict in list_of_dict
                if attribute in datadict and datadict[attribute] == value]

def filter_list_of_dict_with_attr(list_of_dict, attribute):
    """Return matches for item with an attribute"""
    if list_of_dict:
        return [datadict for datadict in list_of_dict
                if attribute in datadict]

def sort_nested_list_in_place(list_of_lists):
    for sub_list in list_of_lists:
        sub_list.sort()
    list_of_lists.sort()

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
