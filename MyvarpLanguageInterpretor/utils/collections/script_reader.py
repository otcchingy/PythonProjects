from MyvarpLanguageInterpretor.utils.collections.enumerator import StringEnumerator


class ScriptReader(StringEnumerator):
    _expression: str
    _current_line: str
    _all_lines: str

    def __init__(self, script='', start=0, stop=0):
        self._current_line = ''
        self._all_lines = ''
        super().__init__(script, enum_type='word', start=start, stop=stop)

    def is_next_equal_to(self, char):
        return self.peek_next() == char

    def is_next_identifier(self):
        return str(self.peek_next_not_space()).isidentifier()

    def is_next_data_object(self):
        return str(self.peek_next_not_space()).isnumeric() or \
               str(self.peek_next_not_space()).lower() in ['true', 'false', 'none'] or self.is_next_string()

    def is_next_string(self):
        return str(self.peek_next_not_space()) in ['"', "'", '"""']

    def is_next_comment(self):
        return str(self.peek_next_not_space()) in ['#', "###", '/*', '*\\', '//']

    def is_next_collection(self):
        if str(self.peek_next_not_space()) in ['[', "(", '{']:
            return True
        else:
            if self.peek_next_not_space() in [',']:
                return True

    def is_next_int(self):
        return str(self.peek_next_not_space()).isnumeric()

    def is_next_bool(self):
        pass

    def is_next_float(self):
        try:
            float(self.peek_next_not_space())
            return True
        except ValueError:
            return False

    def is_next_byte(self):
        pass

    def is_next_operator(self):
        items = ['++', '--', '**', '//', '+=', '-=',
                 '*=', '/=', '==', '>=', '<=', '!=', '=',
                 '/', '*', '+', '-', '%', '>', '<', '!']
        return self.peek_next_not_space() in items

    def is_next_syntax_helper(self):
        items = [';', ':', '^', '&', '%', '|', '$',
                 '@', '!', '#', '\\', '.', '=', ',',
                 '?', '(', ')', '[', ']', '{', '}', '']
        return self.peek_next_not_space() in items

    def is_next_parenthesis(self):
        items = ['(', ')', '[', ']', '{', '}']
        return self.peek_next_not_space() in items

    def is_next_parenthesis_opener(self, line=None):
        items = ['(', '[', '{']
        return self.peek_next_not_space() in line if line and line in items else items

    def is_next_parenthesis_closer(self, line):
        items = [')', ']', '}', ]
        return self.peek_next_not_space() in line if line and line in items else items

    def is_next_function_call(self):
        return self.is_next_parenthesis_opener('(')

    def is_next_method_call(self):
        return self.peek_next_not_space() in ['.'] and str(self.peek_next_not_in(" . \n\t\b\a")).isidentifier()

    def is_next_assignment(self):
        return self.peek_next_not_space() in ["=", 'as']

    def is_next_scope_opener(self):
        return self.peek_next_not_space() in ['{', ':', 'then']

    def is_next_scope_closer(self):
        return self.peek_next_not_space() in ['}', 'endif', 'endfor', 'endwhile', 'endforeach', ';']

    def is_next_group(self):
        return self.is_next_collection()

    def is_next_group_item(self):
        pass

    def is_next_new_line(self):
        return self.peek_next() in ['\n']

    def get_next_not_space(self):
        index = self.peek_next_index(not_in=' \n\t\b\a')
        if index is not None and index > -1:
            if self.set_pointer(index):
                return self.get_items()[index]
