



class DimensionsError(Exception):
    """
    Basic Exception that's intended to use when 2D dimensions of two objects mismatch and shouldn't
    """
    pass

class ResizeError(Exception):
    """
    Exception that is thrown when resize() cannot be performed
    """
    pass


def eq_or_raise(v1,v2,msg,Error=DimensionsError):
    """
    if ``v1 != v2`` raise ``Error`` with message that gets formated as ``msg.format(v1,v2)``
    :param v1:
    :param v2:
    :param msg:
    :param Error:
    :return:
    """
    if v1 != v2:
        raise Error(msg.format(v1,v2))


def gt_or_raise(v1,v2,msg,Error=DimensionsError):
    """
    if ``v1 <= v2`` raise ``Error`` with message that gets formated as ``msg.format(v1,v2)``
    :param v1:
    :param v2:
    :param msg:
    :param Error:
    :return:
    """
    if v1 <= v2:
        raise Error(msg.format(v1,v2))


def gte_or_raise(v1,v2,msg,Error=DimensionsError):
    """
    if ``v1 < v2`` raise ``Error`` with message that gets formated as ``msg.format(v1,v2)``
    :param v1:
    :param v2:
    :param msg:
    :param Error:
    :return:
    """
    if v1 < v2:
        raise Error(msg.format(v1,v2))


def neq_or_raise(v1,v2,msg,Error=DimensionsError):
    """
    if ``v1 == v2`` raise ``Error`` with message that gets formated as ``msg.format(v1,v2)``
    :param v1:
    :param v2:
    :param msg:
    :param Error:
    :return:
    """
    if v1 == v2:
        raise Error(msg.format(v1,v2))