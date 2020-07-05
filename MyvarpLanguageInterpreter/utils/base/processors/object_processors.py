import logging
from utils.base.processors.grammar_processor import MyvarpGrammarProcessor

logging.basicConfig(format="%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s", level=logging.DEBUG)
# logging.disable(logging.DEBUG)
logger = logging.getLogger(__name__)


class ObjectProcessor(MyvarpGrammarProcessor):
    def __init__(self, interpreter, word):
        super().__init__(interpreter, word)
        self.set_expected_types_for_left([None])
        self.set_expected_types_for_right([None])
        self.set_result_type('object')
        logger.debug("ObjectToken: ")

    def operate(self):
        pass


class NumberProcessor(MyvarpGrammarProcessor):
    def __init__(self, word):
        super().__init__(word)
        self.set_expected_types_for_left([None, 'operator', 'expression.helper.@.?.$.{,[,,,('])
        self.set_expected_types_for_right([None, 'identifier', 'operator', 'run'])
        self.set_result_type('number')
        logger.debug(f'NumberToken: {word}')

    def operate(self):
        pass


class BoolProcessor(MyvarpGrammarProcessor):
    def __init__(self, interpreter, word):
        super().__init__(interpreter, word)
        self.set_expected_types_for_left([None])
        self.set_expected_types_for_right([None])
        self.set_result_type('bool')
        logger.debug("BoolToken")

    def operate(self):
        pass


class ByteProcessor(MyvarpGrammarProcessor):
    def __init__(self, interpreter, word):
        super().__init__(interpreter, word)
        self.set_expected_types_for_left([None])
        self.set_expected_types_for_right([None])
        self.set_result_type('byte')
        logger.debug("BoolToken")

    def operate(self):
        pass


class StringProcessor(MyvarpGrammarProcessor):
    def __init__(self, interpreter, word):
        super().__init__(interpreter, word)
        self.set_expected_types_for_left([None])
        self.set_expected_types_for_right([None])
        self.set_result_type('string')
        logger.debug("StringToken")

    def operate(self):
        pass
