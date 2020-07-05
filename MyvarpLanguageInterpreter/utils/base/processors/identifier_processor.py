import logging

from utils.base.processors.null_processor import NullProcessor
from utils.base.processors.grammar_processor import MyvarpGrammarProcessor

logging.basicConfig(format="%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s", level=logging.DEBUG)
# logging.disable(logging.DEBUG)
logger = logging.getLogger(__name__)


class IdentifierProcessor(MyvarpGrammarProcessor):
    def __init__(self, interpreter, word):
        super().__init__(interpreter, word)
        self.set_expected_types_for_left(['null', 'operator', 'expression.helper.,.@.?.$.{.[.('])
        self.set_expected_types_for_right(['operator', 'run', 'null', 'expression.helper.,.{.[.('])
        self.set_left_object(interpreter.get_last_word())
        self.set_result_type('identifier')
        logger.debug("IdentifierToken")