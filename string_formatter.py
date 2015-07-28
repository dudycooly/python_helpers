__author__ = 'jp'

def format_dict_values(data, interesting_field,separator):
    return '{1}{0}{1}'.format(separator.join([data[field]
                                              for field in interesting_field]),separator)

