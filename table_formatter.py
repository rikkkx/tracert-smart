
from enum import Enum


class Align(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2

    @staticmethod
    def center_just(word, length, s=" "):
        if length <= len(word):
            return word
        i = (length - len(word)) // 2
        word = (s * i) + word 
        return word.ljust(length, s)


class TablePrinter:
    def __init__(self, parametres, default_tail=True):
        self._info = []        
        self._width = 1
        for e in parametres.split('|'):
            name, width = e.split(':')
            column = {'name': name, 'width': max(int(width), len(name))}
            self._info.append(column)
            self._width += column['width'] + 1
        self._def_tail = default_tail
    
    @property
    def head(self):
        head = '.'
        for col in self._info:
            head += "".ljust(col['width'], '_') + '.'
        head += '\n'
        head += '|'
        for col in self._info:
            word = TablePrinter.fix_word(col['name'], col['width'], Align.CENTER)
            head += word + "|"
        head += '\n'
        head += "#" * self._width
        return head

    def body(self, iterable):
        cols = len(self._info)
        for line in iterable:
            body = '|'
            line = TablePrinter.fix_line(line, cols)
            for i in range(cols):
                word = TablePrinter.fix_word(line[i], self._info[i]['width'])
                body += word + '|'
            if self._def_tail:
                body += '\n'
                body += self.tail
            yield body
        if not self._def_tail:
            yield self.tail

    @property
    def tail(self):
        tail = '|'
        for col in self._info:
            tail += "".ljust(col['width'], '_') + '|'
        return tail

    @staticmethod
    def fix_line(line, length):
        res = []
        for i in range(length):
            res.append('*')
            if i < len(line):
                res[i] = line[i]
        return tuple(res)

    @staticmethod
    def fix_word(word, length, align=Align.LEFT):
        if word is None:
            return '*'.rjust(length, " ")
        word = str(word)
        if len(word) <= length:
            if align == Align.LEFT:
                return word.ljust(length, " ")
            elif align == Align.RIGHT:
                return word.rjust(length, " ")
            else:
                return Align.center_just(word, length, " ")
        res = ""
        for i in range(length - 1):
            res += word[i]
        return res + '*'

