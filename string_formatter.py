__author__ = 'jp'

def format_dict_values(data, interesting_field,separator):
    """
    :param data dictionary to be inspected:
    :param interesting_field list of fies to be filtered out:
    :param used to separate values in the output:
    :return: formatted string

    e.g.
     In[10]:format_dict_values({'a':"1",'b':"2",'h':'h','aa':'g'}, ['b','a'],'-')

    with pattern 1
    Out[10]:'2-1'

    with pattern 2
    Out[10]:'2-1-'

    """
    # pattern1
    return '{0}'.format(separator.join([data[field]
                                              for field in interesting_field]))
    # pattern2
    return '{0}{1}'.format(separator.join([data[field]
                                              for field in interesting_field]),separator)

