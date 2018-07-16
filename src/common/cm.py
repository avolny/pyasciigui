class CharacterMatrix(object):
    def __init__(self, nrows=10, ncols=10, maxcols=15, fixnrows=False, fixncols=False, wrap=False, wrap_index=-1):
        self.nrows = nrows
        self.ncols = ncols
        self.maxcols = maxcols
        self.fixnrows = fixnrows
        self.fixncols = fixncols
        self.wrap = wrap
        self.wrap_index = wrap_index

        self.s = [' '*ncols for _ in range(nrows)]


    def _get_slice_indices(self, slice_, dim_size):
        if isinstance(slice_, int):
            if slice_ < 0:
                return [dim_size+slice_]
            else:
                return [slice_]
        step = 1 if slice_.step is None else slice_.step
        start = 0 if slice_.start is None else slice_.start
        stop = dim_size if slice_.stop is None else slice_.stop
        return list(range(start, stop, step))


    def transpose(self, inplace=False):
        if inplace:
            o = self
        else:
            o = self.copy()
        o.s = [''.join([o.s[i][j] for i in range(o.nrows)]) for j in range(o.ncols)]
        nr = o.nrows
        nc = o.ncols
        o.nrows = nc # switch
        o.ncols = nr
        return o


    def copy(self):
        o = CharacterMatrix(self.nrows, self.ncols, self.maxcols, self.fixnrows, self.fixncols, self.wrap, self.wrap_index)
        o.s = [self.s[i] for i in range(self.nrows)]
        return o


    def _expand_dimensions(self, nrows, ncols):
        if self.nrows < nrows:
            self.s += [' '*(self.ncols) for _ in range(nrows-self.nrows)]
            self.nrows = nrows
        if self.ncols < ncols:
            ncols = ncols if ncols < self.maxcols else self.maxcols
            self.s = [r + ' '*(ncols-self.ncols) for r in self.s]
            self.ncols = ncols


    def printxy(self, rowid, colid, text):
        """
        print into the matrix
        :param x: row
        :param y: col
        :param text: str or list of rows
        :return:
        """
        if isinstance(text, str):
            text = text.split('\n')
        for i,line in enumerate(text):
            print(line)
            self[rowid+i,colid:colid+len(line)] = line


    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.s[index]
        elif isinstance(index, tuple) or isinstance(index, int):
            index_ = list(index) if isinstance(index, tuple) else [index]
            n = len(index_)

            if n == 1:
                ret = self.s[index_[0]]
                return ret
            if n == 2:
                if isinstance(index_[0],slice):
                    ret = [self.s[i][index_[1]] for i in self._get_slice_indices(index_[0], self.nrows)]
                    return ret
                else:
                    ret = self.s[index_[0]][index_[1]]
                    return ret
            if n >= 3 or n < 1:
                raise IndexError('Index can have either one or two '
                                 'values. Used index: {}'.format(index_))


    def __setitem__(self, index, value):
        if isinstance(index, slice):
            self.s[index] = value
        elif isinstance(index, tuple) or isinstance(index, int):
            index_ = list(index) if isinstance(index, tuple) else [index]
            n = len(index_)

            if n == 1:
                if not self.fixnrows:
                    self._expand_dimensions(index_[0]+1, self.ncols)
                value = str(value)
                if not self.wrap:
                    self[index_[0],0:len(value)] = list(value)
                elif len(value) > self.ncols+self.wrap_index:
                    rows = []
                    while len(value) > self.ncols+self.wrap_index:
                        rows.append(list(value[:self.ncols+self.wrap_index]))
                        value = value[self.ncols + self.wrap_index:]
                    if value != '':
                        rows.append(value)

                    self[index_[0]:index_[0]+len(rows),0:self.ncols+self.wrap_index] = rows
            elif n == 2:
                # value = list(value)
                i_indices = self._get_slice_indices(index_[0], self.nrows)
                j_indices = self._get_slice_indices(index_[1], self.ncols)
                # if we would write emtpy string or list of rows, we write nothing
                if len(i_indices) == 0 or len(j_indices) == 0:
                    return
                self._expand_dimensions(i_indices[-1]+1 if not self.fixnrows else self.nrows,
                                        j_indices[-1]+1 if not self.fixncols else self.ncols)
                # check if the value is indeed an array of rows, if not put it into a 1-element list
                if not isinstance(value, list):
                    value = [str(value)]
                # check if the len is consistent
                if len(value) != len(i_indices) or \
                   True in [len(value[i]) != len(j_indices) for i in range(len(i_indices))]:
                    raise ValueError('Index-Value mismatch. The slice selected has dimensions {}, '\
                         'yet the supplied array has dimensions {}. \n"{}"'.format(
                        (len(i_indices),len(j_indices)),(len(value),len(value[0])), '"\n"'.join(value)))


                for i_iloc,i in enumerate(i_indices):
                    row = ''
                    j_iloc = 0
                    for j in range(self.ncols):
                        if j in j_indices:
                            row += value[i_iloc][j_iloc]
                            j_iloc += 1
                        else:
                            row += self.s[i][j]
                    self.s[i] = row
            elif n >= 3 or n < 1:
                raise IndexError('Index can have either one or two '
                                 'values. Used index: {}'.format(index_))


    def get_lines(self):
        return self.s


    def __str__(self):
        return '\n'.join([s + ' '*(self.ncols-len(s)) for s in self.s])
