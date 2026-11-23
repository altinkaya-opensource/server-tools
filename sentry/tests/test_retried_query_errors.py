# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from psycopg2 import errors

from odoo.tests import TransactionCase, tagged

from ..hooks import before_send


@tagged("post_install", "-at_install")
class TestRetriedQueryErrors(TransactionCase):
    def send(self, logger_name, error):
        """Pass a "bad query" log record to before_send, as sql_db logs it."""
        record = logging.LogRecord(
            logger_name,
            logging.ERROR,
            __file__,
            0,
            "bad query: %s\nERROR: %s",
            ('UPDATE "bus_presence" SET "last_poll" = now() WHERE id IN (1)', error),
            None,
        )
        event = {"tags": {"include_context": False}, "level": "error"}
        return before_send(event, {"log_record": record})

    def test_retried_errors_are_dropped(self):
        for error in (
            errors.SerializationFailure("could not serialize access"),
            errors.LockNotAvailable("could not obtain lock"),
            errors.DeadlockDetected("deadlock detected"),
        ):
            with self.subTest(error=type(error).__name__):
                self.assertIsNone(self.send("odoo.sql_db", error))

    def test_other_query_errors_are_sent(self):
        error = errors.ForeignKeyViolation("violates foreign key constraint")
        self.assertIsNotNone(self.send("odoo.sql_db", error))

    def test_retried_error_from_another_logger_is_sent(self):
        error = errors.SerializationFailure("could not serialize access")
        self.assertIsNotNone(self.send("odoo.addons.some_module", error))
