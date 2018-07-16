from common.errors import *
from common.types import *
from common.text_block import TextBlock

ContainerComponent = namedtuple('ContainerComponent', ['c','row','col','rel_to','rel_how'])

class Container(TextBlock):
    def __init__(self,nrows=1,ncols=1,fixrows=False,fixcols=False,maxrows=1000,maxcols=1000,wrap=False):
        """
        See Container for details
        :param nrows:
        :param ncols:
        :param fixrows:
        :param fixcols:
        :param maxrows:
        :param maxcols:
        :param wrap:
        """
        self.components = []

        super(Container, self).__init__(nrows,ncols,fixrows,fixcols,maxrows,maxcols,wrap)


    def add_component(self, c, row, col, rel_to=None, rel_how='topleft'):
        """
        Add a component ``c`` to the container to pos ``x``,``y`` if ``rel_to == None``.
        If ``rel_to`` is a Component, ``x``,``y`` are used ase relative indices to one of
        ``rel_to``'s corners. Corner is selected using ``rel_how``
        :param c: component to be added
        :param row: absolute (relative to rel_to if rel_to != None) placement row of ``c``
        :param col: absolute (relative to rel_to if rel_to != None) placement col of ``c``
        :param rel_to: Component object or none
        :param rel_how: one of ``['topleft','topright','botleft','botright']``
        :return:
        """
        if not isinstance(c, Component):
            raise TypeError('argument c has to be instance of a class that inherits from Component')

        c.add_resize_listener_func(self.resize_performed)
        if isinstance(rel_to, Component):
            rel_to = rel_to.__cc
        cc = ContainerComponent(c, row, col, rel_to, rel_how)
        c.__cc = cc
        self.components.append(cc)
        self.recompute_component_bounds()
        return cc


    # def remove_component(self, ):


    def get_absolute_position(self, cc):
        """
        get the absolute position of a container component in the container text block
        :param cc: Component or ContainerComponent
        :return:
        """
        if isinstance(cc, Component):
            cc = cc.__cc

        if cc.rel_to is None:
            return cc.row, cc.col
        else:
            rrow, rcol = self.get_absolute_position(cc.rel_to)
            drow = {'topleft': 0, 'topright': 0, 'botleft': cc.rel_to.c.get_nrows()-1, 'botright': cc.rel_to.c.get_nrows()-1}
            dcol = {'topleft': 0, 'topright': cc.rel_to.c.get_ncols()-1, 'botleft': 0, 'botright': cc.rel_to.c.get_ncols()-1}
            return rrow + drow[cc.rel_how] + cc.row, rcol + dcol[cc.rel_how] + cc.col


    def get_bottom_rightmost(self, cc):
        """
        returns index of the bottomest rightmost point of a component
        :return:
        """
        if isinstance(cc, Component):
            cc = cc.__cc

        row, col = self.get_absolute_position(cc)
        return row + cc.c.get_nrows() - 1, col + cc.c.get_ncols() - 1


    def recompute_component_bounds(self):
        """
        compute absolute positions and sizes of components and try to resize
        the container if necessary
        :return:
        """
        for cc in self.components:
            maxrow, maxcol = self.get_bottom_rightmost(cc)
            self.resize_if_possible(maxrow, maxcol)


    def resize_performed(self, e):
        """
        Resize event received
        :param e:
        :return:
        """
        self.recompute_component_bounds()


    def _render_components(self):
        """
        Render all components in their current state into this container
        :return:
        """
        self[:, :] = ' '
        for cc in self.components:
            row, col = self.get_absolute_position(cc)
            self[row:row + cc.c.get_nrows(), col:col + cc.c.get_ncols()] = cc.c.get_lines()


    def _get_lines(self):
        self._render_components()
        return super(Container, self)._get_lines()

    def __getitem__(self, index):
        self._render_components()
        return super(Container, self).__getitem__(index)

    # def __setitem__(self, index, value):




if __name__ == '__main__':
    c = Container()
    b = TextBlock(1, 1, maxcols=3)
    c.add_component(b, 1, 1)

    b2 = TextBlock(1, 1, maxcols=3)
    c.add_component(b2, 1, 0, b, 'botleft')

    b.add_line(0, 'abcd')
    b2.add_line(0, 'efgh')
    print c
    # assert c[:, :] == ['    ', ' ab-', ' cd ', ' ef-', ' gh ']

