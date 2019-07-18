from MyvarpLanguageInterpretor.utils.builtins.funtions import Display

OPERATORS = {
    '++': '',
    '--': '',
    '**': '',
    '//': '',
    '+=': '',
    '-=': '',
    '*=': '',
    '/=': '',
    '==': '',
    '>=': '',
    '<=': '',
    '!=': '',
    '=': '',
    '/': '',
    '*': '',
    '+': '',
    '-': '',
    '%': '',
    '>': '',
    '<': '',
    '!': '',
    '.': ''
}

KEYWORDS = {
    'if': '',
    'else': '',
    'elseif': '',
    'func': '',
    'endif': '',
    'endfunc': '',
    'class': '',
    'interface': '',
    'abstract': '',
    'return': '',
    'when': '',
    'with': '',
    'endwith': '',
    'as': '',
    'from': '',
    'import': '',
    'in': '',
    'for': '',
    'endfor': '',
    'do': '',
    'then': '',
    'foreach': '',
    'endforeach': '',
    'try': '',
    'public': '',
    'private': '',
    'protected': '',
    'static': '',
    'final': '',
    'const': '',
    'except': '',
    'break': '',
    'continue': '',
}

TYPES = {
    'number': '',
    'int': '',
    'float': '',
    'string': '',
    'list': '',
    'dict': '',
    'set': '',
    'tuple': '',
    'bool': '',
    'byte': '',
    'object': '',
    'true': True,
    'false': False,
    'none': None
}

FUNCTIONS = {
    'display': Display()
}

DEFAULT_ENVIRON = {
    'info': {
        'script_name': '',  # get_script_name from kwargs
        'script_path': '',  # get script path
        'start_line': 0,
        'stop_line': 0
    },

    'temp': {},

    'builtins': {
        'operators': OPERATORS,

        'keywords': KEYWORDS,

        'types': TYPES,

        'functions': FUNCTIONS
    },

    'classes': {},

    'functions': {},

    'variables': {}
}

EXPECT_AFTER_DATA = [
    'syntax.helper',
    'syntax.newline',
    'builtins.operator',
    'method.call',
    'builtins.if',
    'builtins.as',
    'builtins.comparator'
]

EXPRESSIONS = [
    'data.',
    'data.identifier',
    'data.|operator|data.',
    'data.identifier|operator.accessor|data.identifier|data.collection.tuple',
    'builtins.keyword|expression|helper|scope'
    'builtins.keyword|data.expression|helper|scope'
]
