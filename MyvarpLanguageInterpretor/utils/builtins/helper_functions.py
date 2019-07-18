from MyvarpLanguageInterpretor.utils.builtins.constants import DEFAULT_ENVIRON


def is_builtin(line, _type=''):
    if not type:
        builtins = ['keywords', 'types', 'functions', 'operators']
        for t in builtins:
            if line in list(DEFAULT_ENVIRON['builtins'][f'{t}'].keys()):
                return True
    else:
        if line in list((DEFAULT_ENVIRON['builtins'][f'{_type}'].keys())):
            return True


def is_keyword(line):
    return is_builtin(line, _type='keywords')


def is_operator(line):
    return is_builtin(line, _type='operators')


def is_comparator_operator(line):
    return line in ['==', '>', '<', '>=', '<=', '!=']


def is_assignment_operator(line):
    return line in ['=', '+=', '-=', '*=', '/=', '%=', '++', '--']


def is_numerical_operator(line):
    return line in ['+', '-', '*', '/', '%', '**']


def is_expression_operator(line):
    return line in ['!', '.']


def is_type(line):
    return is_builtin(line, _type='types')


def is_function(line):
    return is_builtin(line, _type='functions')


@staticmethod
def is_string(line):
    if isinstance(line, str) and not line.isspace() and line != '':
        if line[0] == '"' and line[-1] == '"':
            return True
        if line[0] == "'" and line[-1] == "'":
            return True


@staticmethod
def de_string(line):
    return line[1:-1]
