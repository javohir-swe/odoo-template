from odoo import _, fields, models
from odoo.exceptions import UserError


class SendTestMail(models.TransientModel):
    _name = "send.test.mail"
    _description = "Send Test Email"

    email_to = fields.Char(string="To")

    def send_test_email(self):
        if not self.email_to:
            raise UserError(_("Please provide an email address."))

        active_model = self.env.context.get("active_model")
        active_id = self.env.context.get("active_id")
        if not active_model or not active_id:
            raise UserError(_("No record found."))

        mail_record = self.env[active_model].browse(active_id)
        email_body = mail_record.result

        # Fetch the outgoing mail server username
        mail_server = self.env["ir.mail_server"].search([], limit=1)
        if not mail_server:
            raise UserError(_("No outgoing mail server configured."))

        email_from = mail_server.smtp_user

        mail_values = {
            "subject": mail_record.subject if mail_record.subject else "Movo",
            "body_html": email_body,
            "email_to": self.email_to,
            "email_from": email_from,
        }

        mail = self.env["mail.mail"].create(mail_values)
        mail.send()
        return {"type": "ir.actions.act_window_close"}
