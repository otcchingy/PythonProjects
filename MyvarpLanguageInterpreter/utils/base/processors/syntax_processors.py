import logging
from utils.base.processors.grammar_processor import MyvarpGrammarProcessor

logging.basicConfig(format="%(levelname)-8s [%(lineno)d] %(message)s", level=logging.DEBUG)
# logging.disable(logging.DEBUG)
logger = logging.getLogger(__name__)


class SyntaxHelperProcessor(MyvarpGrammarProcessor):
    def __init__(self, interpreter, i):
        super().__init__(interpreter, i)
        self.set_expected_types_for_left([None])
        self.set_expected_types_for_right(['null', 'keyword', 'identifier', 'data'])
        self.set_result_type('helper')
        logger.debug("HelperToken")

    def operate(self):
        if self.validate_left_object():
            right = self.get_right_object()
            self.get_interpreter().set_last_word(right)


class RunProcessor(MyvarpGrammarProcessor):
    def __init__(self, interpreter):
        super().__init__(interpreter, "")
        self.set_expected_types_for_left([None])
        self.set_expected_types_for_right([None])
        self.set_result_type('run')
        logger.debug("Run Expression")

    def operate(self):
        if self.validate_left_object():
            right = self.get_right_object()
            self.get_interpreter().set_last_word(right)


class CallProcessor(MyvarpGrammarProcessor):
    def __init__(self, interpreter):
        super().__init__(interpreter, "")
        self.set_expected_types_for_left(['identifier', 'object', 'class'])
        self.set_expected_types_for_right(['null', 'keyword', 'identifier', 'data', 'expression.helper.{.[.(.)'])
        self.set_left_object(None)
        self.set_result_type('call')
        logger.debug("Object Call")

    def operate(self):
        if self.validate_left_object():
            right = self.get_right_object()
            self.get_interpreter().set_last_word(right)
