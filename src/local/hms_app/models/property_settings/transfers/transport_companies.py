import re

from odoo import api, exceptions, fields, models


class TransportCompanies(models.Model):
    _name = "transport.companies"
    _description = "Transport Companies"

    name = fields.Char(string="Name", required=True)
    email_for_notifications = fields.Char(string="Notification Email")
    usd = fields.Integer(string="Price in USD")
    uzs = fields.Integer(string="Price in UZS")
    rub = fields.Integer(string="Price in RUB")

    @api.constrains("email_for_notifications")
    def _check_email(self):
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        for record in self:
            if record.email_for_notifications and not re.match(
                email_regex, record.email_for_notifications
            ):
                raise exceptions.ValidationError("Please enter a valid email address.")
