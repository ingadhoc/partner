##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

import re

from odoo.tests.common import TransactionCase


class TestPartnerStateTracking(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.StateField = cls.env["res.partner.state_field"]
        cls.StateField.search([]).unlink()
        cls.env.company.partner_state_enable = True
        cls.partner = cls.env["res.partner"].create({"name": "Tracking Partner", "email": "old@example.com"})
        # records created in the same transaction are not tracked until creation is finalized
        cls._flush_tracking(cls.env)

    @staticmethod
    def _flush_tracking(env):
        env.flush_all()
        env.cr.precommit.run()

    def _tracked_fields(self, vals):
        """Write vals on the partner and return the field names logged in the chatter."""
        self.partner.message_ids.unlink()
        self.partner.write(vals)
        self._flush_tracking(self.env)
        messages = self.partner.message_ids
        if "tracking_value_ids" in messages._fields:
            return set(messages.tracking_value_ids.field_id.mapped("name"))
        # without mail_tracking, Odoo renders the tracking only in the body: "old → <b>new</b> <i>(Label)</i>"
        labels = set(re.findall(r"<i>\((.*?)\)</i>", "".join(messages.mapped("body"))))
        return {name for name in self.partner._track_get_fields() if self.partner._fields[name].string in labels}

    def _add_line(self, field_name, changes):
        return self.StateField.create(
            {
                "field_id": self.env["ir.model.fields"]._get("res.partner", field_name).id,
                "changes": changes,
                "track": False,
                "approval": False,
                "block_edition": False,
            }
        )

    def test_chatter_tracking_by_state_fields(self):
        """ "Changes?" only adds fields to the chatter, it never removes standard ones.

        - Without lines, the standard tracked fields are logged.
        - A line with "Changes?" logs a field that is not tracked by default, and an
          approved partner does not go back to potential.
        - A line without "Changes?" does not stop logging a standard tracked field.
        """
        with self.subTest("without lines, a standard tracked field is logged"):
            self.assertEqual(self._tracked_fields({"email": "new@example.com"}), {"email"})

        with self.subTest("a line with changes logs a field not tracked by default and keeps the partner approved"):
            self._add_line("ref", changes=True)
            self.partner.partner_state_approved()
            self.assertEqual(self._tracked_fields({"ref": "REF-1", "email": "other@example.com"}), {"ref", "email"})
            self.assertEqual(self.partner.partner_state, "approved")

        with self.subTest("a line without changes keeps logging a standard tracked field"):
            self._add_line("email", changes=False)
            self.assertEqual(
                self._tracked_fields({"ref": "REF-2", "email": "last@example.com"}),
                {"ref", "email"},
            )

    def test_changes_column_for_standard_fields(self):
        """The "Changes?" column is checked and fixed for fields already tracked by Odoo."""
        email_line = self._add_line("email", changes=False)
        ref_line = self._add_line("ref", changes=False)

        with self.subTest("a standard field shows changes checked even if the line has it unchecked"):
            self.assertTrue(email_line.native_tracking)
            self.assertTrue(email_line.chatter_tracking)

        with self.subTest("another field shows and writes the stored changes value"):
            self.assertFalse(ref_line.native_tracking)
            self.assertFalse(ref_line.chatter_tracking)
            ref_line.chatter_tracking = True
            self.assertTrue(ref_line.changes)
