import logging

from utils.base.processors.grammar_processor import MyvarpGrammarProcessor

logging.basicConfig(format="%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s", level=logging.DEBUG)
# logging.disable(logging.DEBUG)
logger = logging.getLogger(__name__)


class AssignmentProcessor(MyvarpGrammarProcessor):
    def __init__(self, interpreter):
        super().__init__(interpreter, "=")
        self.set_expected_types_for_left('identifier')
        self.set_expected_types_for_right(['identifier', 'data-expression', 'data'])
        self.set_left_object(interpreter.get_last_word())
        logger.debug("AssignmentToken")

    def operate(self):
        if self.validate_left_object():
            right = self.get_interpreter().wait_for_data()
            if right is not None:
                word = None  # DataWordProcessor(right)
                self.set_right_object(word)
                if self.validate_right_object():
                    pass
                    # self.get_interpreter().get_memory . do_assignment
                    # with self.get_right_object().get_word() self.get_right_object().get_result()
                    # set self result type
                    self.get_interpreter().set_last_word(self)
