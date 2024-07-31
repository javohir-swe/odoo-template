from odoo import api, fields, models


class AdvancedAvailabilitySettings(models.Model):
    _name = "availability_settings"
    _description = "Advanced Availability Settings"

    date = fields.Date(string="Date")
    role_sales = fields.Many2one("availability.online_sales_role", string="Role sales")

    @api.model
    def create(self, vals):
        existing_record = self.search([("date", "=", vals.get("date"))], limit=1)
        if existing_record:
            existing_record.write(vals)
            return existing_record
        return super().create(vals)

    def write(self, vals):
        if "date" in vals:
            for record in self:
                existing_record = self.search(
                    [("date", "=", vals.get("date")), ("id", "!=", record.id)], limit=1
                )
                if existing_record:
                    existing_record.write(vals)
                    self.unlink()
                    return existing_record
        return super().write(vals)
