from MyvarpLanguageInterpretor.utils.builtins.funtions import Display

DEFAULT_ENVIRON = {
    'info': {
        'script_name': '',  # get_script_name from kwargs
        'script_path': '',  # get script path
        'start_line': 0,
        'stop_line': 0
    },

    'temp': {},

    'builtins': {
        'operators': {
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
            '!': ''
        },

        'keywords': {
            'if': '',
            'else': '',
            'else if': '',
            'func': '',
            'class': '',
            'return': '',
            'when': '',
            'with': '',
            'as': '',
            'loop': '',
            'from': '',
            'for': '',
            'do': '',
            'then': '',
            'foreach': '',
            'try': '',
            'except': '',
            'break': '',
            'continue': '',
        },

        'types': {
            'number':  '',
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
        },

        'functions': {
            'display': Display()
        }
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
