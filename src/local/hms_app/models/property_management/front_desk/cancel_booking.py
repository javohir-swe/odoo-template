from odoo import api, fields, models


class CancelBooking(models.Model):
    _name = "front_desk.cancel_booking"
    _description = "Cancel Booking"

    name = fields.Char(string="Name", compute="_compute_name")
    booking_id = fields.Many2one("booking")
    reason = fields.Selection(
        [
            ("no_show", "No show"),
            ("no_show_charged", "No Show charged"),
            ("booking_cancellation", "Booking cancellation"),
            ("other", "Other"),
        ],
        string="Reason for cancellation",
        default="no_show",
    )
    comment = fields.Text(string="Comment")

    @api.depends("booking_id")
    def _compute_name(self):
        for record in self:
            if record.booking_id:
                record.name = str(record.booking_id.unique_id)
            else:
                record.name = "Cancel booking"

    @api.model
    def create(self, vals):
        booking = self.env["booking"].search([("id", "=", vals["booking_id"])])
        if booking:
            if vals.get("comment"):
                booking.status = "cancel"
        return super().create(vals)

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if record.comment and record.booking_id:
                record.booking_id.status = "cancel"
        return res
