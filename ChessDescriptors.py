

chess_colors = ('White', 'Black')
chess_vertical = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
chess_horizontal = tuple(map(str, (1, 2, 3, 4, 5, 6, 7, 8)))


class ChessDescriptor(object):

    def __init__(self, cls):
        self._cls = cls

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if isinstance(value, list) or isinstance(value, set):
            if not bool(value):
                instance.__dict__[self.name] = value
                return
            f = True
            for item in value:
                if not isinstance(item, self._cls) and not issubclass(item.__class__, self._cls):
                    f = False
                    break
            if f:
                instance.__dict__[self.name] = value
                return
            else:
                raise ValueError(f"{self.name} should be list/set of instances of class {self._cls} or it's subclass")
        elif isinstance(value, self._cls) or issubclass(value.__class__, self._cls) or value is None:
            instance.__dict__[self.name] = value
        else:
            raise ValueError(f'{self.name} should be in (inst of {self._cls}, inst of sub of {self._cls} None)')


class ColorDescriptor(object):

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value in chess_colors or value is None:
            instance.__dict__[self.name] = value
        else:
            raise ValueError(f'{self.name} should be in {chess_colors} or None')


class PositionDescriptor(object):

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if (value[0] in chess_vertical and value[1] in chess_horizontal) or value is None:
            instance.__dict__[self.name] = value
        else:
            raise ValueError(f'{self.name} should be chess-notation str or None')


class IntDescriptor(object):

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if isinstance(value, int):
            instance.__dict__[self.name] = value
        else:
            raise ValueError(f'{self.name} should be int type')


class BoolDescriptor(object):

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if isinstance(value, bool):
            instance.__dict__[self.name] = value
        else:
            raise ValueError(f'{self.name} should be bool type')


class SmthOrFalseDescriptor(object):

    def __init__(self, cls):
        self._cls = cls

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if str(value) == 'False' or issubclass(value.__class__, self._cls) or isinstance(value, self._cls):
            instance.__dict__[self.name] = value
        else:
            raise ValueError(f'{self.name} should be in (False, {self._cls}, subclass of {self._cls})')


class NonDataDescriptor(object):

    def __init__(self):
        self.instance_flag = False

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if self.instance_flag:
            raise ValueError(f'You cannot set the {self.name} value')
        else:
            instance.__dict__[self.name] = value
            self.instance_flag = True
