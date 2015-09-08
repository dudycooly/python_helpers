__author__ = 'jp'

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
