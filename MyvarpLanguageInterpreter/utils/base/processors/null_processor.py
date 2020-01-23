import logging
from utils.base.processors.grammar_processor import MyvarpGrammarProcessor

logging.basicConfig(format="%(levelname)-8s [%(lineno)d] %(message)s", level=logging.DEBUG)
# logging.disable(logging.DEBUG)
logger = logging.getLogger(__name__)


class NullProcessor(MyvarpGrammarProcessor):
    def __init__(self, interpreter):
        super().__init__(interpreter, "")
        self.set_expected_types_for_left([None])
        self.set_expected_types_for_right(['null', 'keyword', 'identifier', 'data'])
        self.set_left_object(None)
        self.set_result_type('null')
        logger.debug("NullToken")

    def operate(self):
        if self.validate_left_object() and self.validate_right_object():
            right = self.get_right_object()
            self.get_interpreter().set_last_word(right)
