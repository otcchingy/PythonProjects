from MyvarpLanguageInterpretor.utils.collections.stack import Stack


class Enumerator:
    _start: int
    _stop: int
    _line_count: int
    _pointer: int
    _end_pointer: int
    _e_items: list

    def __init__(self, list_source=None, **kwargs):

        """

        :param list_items: list of items to enumerate through
        :param kwargs:
                start : index of iteration to start from    :default = 0,
                stop : number of iteration to stop at       :default = last item index
        """

        self._e_items = [] if not list_source else list(list_source)
        self._line_count = 0

        try:
            self._start = int(kwargs['start'])
        except KeyError:
            self._start = 0
        try:
            self._stop = int(kwargs['stop'])
        except KeyError:
            self._stop = 0

        self._start = 0 if (not self._start) or (0 > self._start >= self.__len__()) else self._start
        self._pointer = self._start - 1
        self._stop = (self.__len__() - 1) if (not self._stop) or \
                                             (0 > self._stop >= self.__len__()) or \
                                             (self._start < self._stop) else self._stop
        self._end_pointer = self._stop

    def __len__(self):
        return self._e_items.__len__()

    def __getitem__(self, item):
        item = int(item)
        if -1 < item < self.__len__():
            return self._e_items[item]

    def __next__(self):
        return self.get_next()

    def __previous__(self):
        return self.get_next()

    def add_item(self, item):
        self._e_items.append(item)
        self._stop = self._e_items.__len__() - 1

    def add_all_items(self, items):
        self._e_items += list(items)
        self._stop = self._e_items.__len__() - 1

    def get_items(self):
        return self._e_items

    def get_start_index(self):
        return self._start

    def get_stop_index(self):
        return self._stop

    def set_pointer(self, index):
        if self._start <= index <= self._stop:
            self._pointer = index
            return True
        return False

    def has_next(self):
        return self._pointer + 1 <= self._stop

    def has_previous(self):
        return self._pointer - 1 >= self._start and self._pointer <= self._stop

    def get_next(self):
        if self.has_next():
            self._pointer += 1
            return self._e_items[self._pointer]

    def get_previous(self):
        if self.has_previous():
            self._pointer -= 1
            return self._e_items[self._pointer]

    def peek(self, index):
        if self._start <= index <= self._stop:
            return self._e_items[index]

    def peek_next(self):
        if self.has_next():
            return self._e_items[self._pointer + 1]

    def peek_previous(self):
        if self.has_previous():
            return self._e_items[self._pointer - 1]

    def get_current_item_number(self):
        return self._pointer


class StringEnumerator(Enumerator):
    _line_count: int
    _enum_type = None
    _e_script = None

    def __init__(self, script: str = None, **kwargs):

        """
        :param script: string lines
        :param kwargs:
                enum_type :
                        'line' - enumerate file by lines,
                        'char' - enumerate file by characters,
                        'word' - enumerate file by words,
                start : index of iteration to start from    :default = 0,
                stop : number of iteration to stop at       :default = last item index
        """

        try:
            self._enum_type = str(kwargs['enum_type'])
            if not self._enum_type:
                self._enum_type = 'word'
        except KeyError:
            self._enum_type = 'word'

        if not script:
            script = []

        self._line_count = 0

        if (not self._enum_type) or self._enum_type == 'line':
            script = list(enumerate(script))
        elif self._enum_type == 'char':
            script = list(script)
        elif self._enum_type == 'word':
            self._e_script = DefaultWalker(script)

        super().__init__(script)

    def set_pointer(self, index):
        if self._enum_type == 'word':
            return self._e_script.set_pointer(index)
        return self.set_pointer(index)

    def add_item(self, item):
        if self._enum_type == 'word':
            return self._e_script.add_item(item)
        return super().add_item(item)

    def add_all_items(self, items):
        if self._enum_type == 'word':
            return self._e_script.add_all_items(items)
        return super().add_all_items(items)

    def get_current_line_number(self):
        return self._line_count

    def get_items(self):
        if self._enum_type == 'word':
            return self._e_script.get_items()
        return super().get_items()

    def get_stop_index(self):
        if self._enum_type == 'word':
            return self._e_script.get_stop_index()
        return super().get_stop_index()

    def get_start_index(self):
        if self._enum_type == 'word':
            return self._e_script.get_start_index()
        return super().get_start_index()

    def get_current_item_number(self):
        if self._enum_type == 'word':
            return self._e_script.get_current_item_number()
        return super().get_current_item_number()

    def peek_next_index(self, not_in=''):
        if self._enum_type == 'word':
            c_index = self._e_script.get_current_item_number() + 1
            if not_in != '':
                while str(self._e_script.peek(c_index)) in not_in and c_index <= self._e_script.get_stop_index():
                    c_index += 1

            if c_index <= self._e_script.get_stop_index():
                return c_index
            return -1
        else:
            c_index = self.get_current_item_number() + 1
            if not_in != '':
                while str(self.peek(c_index)) in not_in and c_index <= self.get_stop_index():
                    c_index += 1

            if c_index <= self.get_stop_index():
                return c_index
            return -1

    def peek_next_not_in(self, line: str):
        index = self.peek_next_index(not_in=line)
        if index > -1:
            if self._enum_type == 'word':
                return self._e_script.peek(index)
            return self.peek(index)

    def peek(self, index):
        if self._enum_type == 'word':
            return self._e_script.peek(index)
        return super().peek(index)

    def peek_next(self):
        if self._enum_type == 'word':
            return self._e_script.peek_next()
        return super().peek_next()

    def peek_previous(self):
        if self._enum_type == 'word':
            return self._e_script.peek_previous()
        return super().peek_previous()

    def peek_next_not_space(self):
        index = self.peek_next_index(not_in=' \n\t\b\a')
        if index > -1:
            if self._enum_type == 'word':
                return self._e_script.peek(index)
            return self.peek(index)

    def has_next(self):
        if self._enum_type == 'word':
            return self._e_script.has_next()
        return super().has_next()

    def has_next_not_space(self):
        return self.peek_next_not_space()

    def has_next_not_in(self, line):
        return self.peek_next_not_in(line)

    def move_to_next_not_space(self):
        index = self.peek_next_index(not_in=' \n\t\b\a')
        if index > -1:
            self.set_pointer(index - 1)

    def move_to_next_not_in(self, line):
        index = self.peek_next_index(not_in=line)
        if index > -1:
            self.set_pointer(index - 1)

    def has_previous(self):
        if self._enum_type == 'word':
            return self._e_script.has_previous()
        else:
            return super().has_previous()

    def get_next(self):
        if self.has_next():

            item = None

            if self._enum_type == 'word':
                item = self._e_script.get_next()
            else:
                item = super().get_next()

            if self._enum_type == 'line':
                self._line_count += 1
            elif self._enum_type in 'word|char':
                if item == '\n':
                    self._line_count += 1

            return item

    def get_previous(self):
        if self.has_previous():
            item: str

            if self._enum_type == 'word':
                item = self._e_script.get_next()
            else:
                item = super().get_previous()

            if self._enum_type == 'line':
                self._line_count -= 1
            elif self._enum_type in 'word|char':
                if item == '\n':
                    self._line_count -= 1

            return item


class Walker(Enumerator):
    _enumerator: Enumerator
    _matchers: dict
    _breakers: set
    _current_word: str
    _is_breaker_word_part: bool
    _is_grouper_word_part: bool
    _stack: Stack
    _expected: str
    _string_active: bool
    _multiple_line_string_active: int
    _pointer: int

    def __init__(self, groupers: dict = None, breakers: set = None):

        self._string_active = False
        self._multiple_line_string_active = 0
        self._is_breaker_word_part = True
        self._is_grouper_word_part = True
        self._stack = Stack()
        self._expected = ''
        self._current_word = ''
        self._groupers = {}
        self._breakers = set([])
        self._pointer = -1

        self._enumerator = Enumerator([])

        super().__init__()

        if groupers:
            self._groupers = groupers
        if breakers:
            self._breakers = breakers

    def set_enumerator(self, enumerator: Enumerator):
        self._enumerator = enumerator

    def add_all_items(self, items):
        self._enumerator.add_all_items(items)
        self.generate_words()

    def add_item(self, item):
        self._enumerator.add_all_items(item)
        self.generate_words()

    def set_breaker_as_word(self, choice: bool):
        self._is_breaker_word_part = bool(choice)

    def set_grouper_as_word_part(self, choice: bool):
        self._is_grouper_word_part = bool(choice)

    def reset_expected(self):
        self._expected = ''

    def get_expected(self):
        self.__process_expected()
        return self._expected

    def __process_expected(self):

        self._expected = ''

        if self.is_grouper(self._stack.top()):
            self._expected = self._groupers[self._stack.top()]
        elif self._current_word == '':
            self._expected = '|char|opener| |any'
        elif self.is_breaker(self._current_word):
            self._expected = '|char|opener| |'
        elif self.is_group_opener(self._current_word):
            self._expected = '|char|closer| |'
        elif self.is_group_closer(self._current_word):
            self._expected = '|char|opener|closer| |breaker|'
        elif self._current_word.__len__() >= 1:
            self._expected = '|char|opener| |breaker|'

    def is_current_word_group(self):
        return self._stack.top() in self.get_groupers().keys()

    def is_current_word_in_string(self):
        return self._string_active

    def set_breakers(self, breakers: set):
        self._breakers = breakers

    def add_breakers(self, breaker: str):
        self._breakers.add(breaker)

    def get_breakers(self):
        return self._breakers

    def set_groupers(self, groupers: dict):
        self._groupers = groupers

    def add_groupers(self, opener: str, closer: str):
        self._groupers[opener] = closer

    def get_groupers(self):
        return self._groupers

    def get_current_word(self):
        return self._current_word

    def make_word(self):
        if self._current_word != '':
            if (self.is_breaker(self._current_word)) and self._is_breaker_word_part:
                self.__add_word()
            elif (self.is_grouper(self._current_word)) and self._is_grouper_word_part:
                self.__add_word()
            else:
                self.__add_word()

    def __add_word(self):
        super().add_item(self._current_word)
        self._current_word = ''

    def is_word_has_groupers(self, line: str):
        return self.is_grouper(line[0])

    def is_breaker(self, breaker: str):
        return breaker in self._breakers

    def is_grouper(self, grouper: str):
        return self.is_group_opener(grouper) or self.is_group_closer(grouper)

    def is_group_opener(self, grouper: str):
        return list(self._groupers.keys()).__contains__(grouper)

    def is_group_closer(self, grouper: str):
        return list(self._groupers.values()).__contains__(grouper)

    def is_expecting(self, line):

        if self.is_breaker(line):
            line = 'breaker'
        elif self.is_grouper(line):
            return line == self.get_expected()
        else:
            line = 'char'

        return line in self.get_expected()

    def generate_words(self):
        while self._enumerator.has_next():
            data = self._enumerator.get_next()

            if self._multiple_line_string_active:

                if self.is_expecting(data):
                    if self._enumerator.peek(self._enumerator.get_current_item_number() + 1) == data and \
                            self._enumerator.peek(self._enumerator.get_current_item_number() + 2) == data:
                        self._multiple_line_string_active = 0
                        self.make_word()
                        if self._is_grouper_word_part:
                            self._current_word += self._enumerator.get_next()
                            self._stack.pop()
                            self._current_word += self._enumerator.get_next()
                            self._stack.pop()
                            self._current_word += data
                            self._stack.pop()
                            self.make_word()
                    else:
                        self._current_word += data

                else:
                    self._current_word += data

            elif self.is_current_word_in_string():

                if self.is_expecting(data):
                    self._string_active = False
                    self._stack.pop()
                    self.make_word()
                    if self._is_grouper_word_part:
                        self._current_word += data
                        self.make_word()

                else:
                    self._current_word += data

            elif self.is_breaker(data):

                self.make_word()
                if self._is_breaker_word_part:
                    self._current_word += data
                    self.make_word()

            elif self.is_grouper(data):

                if self.is_expecting(data):
                    if data == "'" or data == '"':
                        self._string_active = False
                    self._stack.pop()
                elif self._stack.isEmpty() or self._stack.top() != data:
                    if data == "'" or data == '"':

                        if self._enumerator.peek(self._enumerator.get_current_item_number() + 1) == data and \
                                self._enumerator.peek(self._enumerator.get_current_item_number() + 2) == data:
                            self._multiple_line_string_active = 3
                        else:
                            self._string_active = True
                    if self.is_group_opener(data):
                        self._stack.push(data)
                    if self._multiple_line_string_active:
                        self._stack.push(self._enumerator.get_next())
                        self._stack.push(self._enumerator.get_next())

                self.make_word()
                if self._is_grouper_word_part:
                    self._current_word += data
                    if self._multiple_line_string_active:
                        self._current_word += data
                        self._current_word += data
                    self.make_word()
            else:
                self._current_word += data

        if self._current_word != '':
            self.make_word()


class DefaultWalker(Walker):

    def __init__(self, lines):
        breakers = {
            ' ', ',', ';', ':', '.', '=', '+',
            '-', '*', '/', '@', '\n', '\t',
            '\b', '\a', '^', '!', '<', '>', '#'}

        groupers = {
            '{': '}',
            '[': ']',
            '(': ')',
            '"': '"',
            "'": "'",
            '/*': '*/',
            '"""': '"""',
            "'''": "'''",
            '###': '###'
        }

        super().__init__(groupers, breakers)
        super().add_all_items(lines)


# s = DefaultWalker("""
# '''
#     sdasdafa
#     My name is a  man 'i am him "lets gp" '
#     afdafadfaj jhjhb
# '''
# """)
#
# while (s.has_next()):
#     print(s.get_next())
