from utils.collections.enumerator import StringEnumerator


class ScriptReader(StringEnumerator):

    def __init__(self, script='', start=0, stop=0):
        super().__init__(script, enum_type='word', start=start, stop=stop)

    def is_next_equal_to(self, char):
        return self.peek_next() == char

    def is_next_identifier(self):
        return str(self.peek_next()).isidentifier()

    def is_next_data_object(self):
        return str(self.peek_next()).isnumeric() or \
               str(self.peek_next()).lower() in ['true', 'false', 'none'] or self.is_next_string()

    def is_next_string(self):
        return str(self.peek_next()) in ['`', "'", '"', '"""', "'''"]

    def is_next_comment(self):
        return str(self.peek_next()) in ['#', "###", '/*', '*/']

    def is_next_collection(self):
        if str(self.peek_next()) in ['[', "(", '{', '}', ')', ']']:
            return True
        # else:
        #     if self.peek_next() in [',']:
        #         return True

    def is_next_collection_opener(self, line=None):
        if self.peek_next() in ['(', '[', '{']:
            if line and line in ['(', '[', '{']:
                return self.peek_next() == line
            return True

    def is_next_collection_closer(self, line=None):
        if self.peek_next() in [')', ']', '}']:
            if line and line in [')', ']', '}']:
                return self.peek_next() == line
            return True

    def is_next_int(self):
        return str(self.peek_next()).isnumeric()

    def is_next_bool(self):
        return str(self.peek_next()).lower() in ['true', 'false']

    def is_next_float(self):
        try:
            float(self.peek_next())
            return True
        except ValueError:
            return False

    def is_next_byte(self):
        pass

    def is_next_operator(self):
        items = ['++', '--', '**', '//', '+=', '-=', '^',
                 '*=', '/=', '==', '>=', '<=', '!=', '&',
                 '**=', '//=', '%=', '%', '^', '~', '=',
                 '/', '*', '+', '-', '>', '<', '!', '.']
        return self.peek_next() in items

    def is_next_syntax_helper(self):
        items = [';', ':', '|', '$', '#', '\\', ',', '?', '@', '(',  ')', '[', ']', '{', '}']
        return self.peek_next() in items

    def is_next_dot_operator(self):
        return self.peek_next() in ['.'] and str(self.peek_next_not_in(" . \n\t\b\a")).isidentifier()

    def is_next_assignment(self):
        return self.peek_next() in ["=", 'as']

    def is_next_group(self):
        return self.peek_next() in ['`', '"', "'", '/*', '*/', '"""', "'''", '###']

    def is_next_new_line(self):
        return self.peek_next() in ['\n']

    def is_next_line_terminator(self):
        return self.peek_next() in [';', 'endif', 'endfor', 'endwith', 'endfunc',
                                    'endwhile',  'endswitch',  'endclass', 'endforeach']

    def get_next_not_space(self):
        index = self.peek_next_index(not_in=' \n\t\b\a')
        if index is not None and index > -1:
            if self.set_pointer(index):
                return self.get_items()[index]
