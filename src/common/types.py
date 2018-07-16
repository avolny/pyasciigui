from abc import abstractmethod, ABCMeta
from collections import namedtuple
from common.errors import *

ResizeEvent = namedtuple('ResizeEvent',['o','old_size','new_size'])



class Component(object):
    """
    Component abstract base class. The only abstract method is ``get_lines()``.
    This is the most basic building block of the whole framework from which every printable class inherits.
    Its purpose is to represent a rectangular ascii character matrix.
    """

    # __metaclass__ = ABCMeta

    def __init__(self, nrows, ncols):
        """
        Initialize base class, set initial number of rows and cols
        :param nrows:
        :param ncols:
        """
        self._resize_listeners = []
        self._nrows = nrows
        self._ncols = ncols
        pass


    def get_nrows(self):
        """
        Method that returns the true printed number of lines,
        can be overridden
        :return:
        """
        return self._nrows


    def get_ncols(self):
        """
        Method that returns the true printed number of lines,
        can be overridden
        :return:
        """
        return self._ncols

    def size(self):
        return (self._nrows, self._ncols)


    def add_resize_listener_func(self, func):
        """
        add resize event listener function it gets called as func(e) where e is ResizeEvent
        :param func:
        :return:
        """
        self._resize_listeners.append(func)


    def remove_resize_listener(self, func=None, index=None):
        """
        Removes a resize event listener, either by object reference or by index
        :param func:
        :param index:
        :return:
        """
        if func is not None:
            self._resize_listeners.remove(func)
        elif index is not None:
            self._resize_listeners.remove(self._resize_listeners[index])
        else:
            raise ValueError('Either the listener object reference or the index must not be None.')


    def resize(self, nrows, ncols):
        """
        Resize the Component. This method `cannot` be overridden for proper functionality.
        :param nrows: new number of rows
        :param ncols: new number of columns
        :return:
        """
        nrows, ncols = self._resize(nrows, ncols)
        if nrows != self._nrows or ncols != self._ncols:
            e = ResizeEvent(self, self.size(), (nrows,ncols))
            self._nrows = nrows
            self._ncols = ncols
            self._invoke_resize_performed(e)


    def _invoke_resize_performed(self, e):
        """
        invoke all listener functions
        :param e:
        :return:
        """
        for func in self._resize_listeners:
            func(e)
        pass


    def __str__(self):
        return '\n'.join(self.get_lines())


    def get_lines(self):
        """
        Returns a list of string rows. This method `cannot` be overridden.
        Implements size validation before returning
        :return:list of string rows, consistent size with nrows,ncols
        """
        lines = self._get_lines()
        eq_or_raise(len(lines), self.get_nrows(), '_get_lines() returned {} rows yet component has nrows={}')
        for line in lines:
            eq_or_raise(len(line), self.get_ncols(), '_get_lines() returned a row with {} cols yet component has ncols={}')
        return lines


    @abstractmethod
    def _resize(self, nrows, ncols):
        """
        Override this method in a child class, do all processing necessary to resize the component.
        Returns new rows and cols w.r.t. constraints of the subclass
        :return: tuple: (rows, cols)
        """
        pass


    @abstractmethod
    def _get_lines(self):
        """
        Override this method in a child class, this is the method that returns the actual text to be printed.
        :return: list of string rows, same length
        """
        pass




