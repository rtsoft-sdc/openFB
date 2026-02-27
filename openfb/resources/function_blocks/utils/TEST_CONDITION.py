import logging
import threading


class TEST_CONDITION:
    executed_tests = 0
    failed_tests = 0
    final_report_printed = False
    final_report_lock = threading.Lock()

    def schedule(self, event_name, event_value, check):
        if event_name == 'REQ':
            TEST_CONDITION.executed_tests += 1

            if check:
                logging.info(
                    "------------------------------ [TEST_CONDITION_PASSED] %s passed",
                    self.get_instance_tag(),
                )
            else:
                TEST_CONDITION.failed_tests += 1
                logging.error(
                    "------------------------------ [TEST_CONDITION_FAILED] %s failed",
                    self.get_instance_tag(),
                )

            return event_value

    def get_instance_tag(self):
        return self.__class__.__name__

    def __del__(self):
        try:
            with TEST_CONDITION.final_report_lock:
                if TEST_CONDITION.final_report_printed:
                    return
                TEST_CONDITION.final_report_printed = True

                logging.info("\n------------------------------------------------------------------------------")
                logging.info(
                    " ------------------------ [TEST_CONDITION FINAL REPORT] -----------------------"
                )
                if TEST_CONDITION.failed_tests:
                    logging.error(
                        " ------------------------ %u tests executed, %u failed -----------------------",
                        TEST_CONDITION.executed_tests,
                        TEST_CONDITION.failed_tests,
                    )
                else:
                    logging.info(
                        " ------------------------ %u tests executed, %u failed -----------------------",
                        TEST_CONDITION.executed_tests,
                        TEST_CONDITION.failed_tests,
                    )
                logging.info("------------------------------------------------------------------------------\n")
        except Exception:
            pass
        
