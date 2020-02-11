from utils.builtins.constants import BUILTINS


def get_builtin(line):
    if is_builtin(line):
        for x in ['keywords', 'operators', 'classes', 'functions']:
            if BUILTINS[f'{x}'].__contains__(line):
                return BUILTINS[f'{x}'][f'{line}']


def is_builtin(line, _type="all"):
    if _type == "all":
        for x in ['keywords', 'operators', 'classes', 'objects']:
            if BUILTINS[f'{x}'].__contains__(line):
                return True
    else:
        return BUILTINS[f'{_type}'].__contains__(line)


def is_operator(line):
    return is_builtin(line, _type='operators')


def is_keyword(line):
    return is_builtin(line, _type='keywords')


def is_builtin_type(line):
    return is_builtin(line, _type='classes')


def is_builtin_object(line):
    return is_builtin(line, _type='objects')


def is_comparator_operator(line):
    return line in ['==', '>', '<', '>=', '<=', '!=']


def is_assignment_operator(line):
    return line in ['=', '+=', '-=', '*=', '/=', '%=', '++', '--']


def is_numerical_operator(line):
    return line in ['+', '-', '*', '/', '%', '**', '^']


def is_expression_operator(line):
    return line in ['!', '.']


def is_type(line):
    return is_builtin(line, _type='types')


def is_function(line):
    return is_builtin(line, _type='functions')


def is_string(line):
    if isinstance(line, str) and not line.isspace() and line != '':
        if line[0] == '"' and line[-1] == '"':
            return True
        if line[0] == "'" and line[-1] == "'":
            return True


def de_string(line):
    return line[1:-1]
