from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CancelCheckin(models.Model):
    _name = "front_desk.cancel_checkin"
    _description = "Cancel Checkin"

    booking_id = fields.Many2one("booking", string="Booking")
    reason = fields.Char(string="Description")

    @api.model
    def create(self, vals):
        booking = self.env["booking"].search([("id", "=", vals["booking_id"])])
        if booking:
            if booking.is_check_in:
                booking.is_check_in = False
            else:
                raise ValidationError("This booking has not been previously checked-in")

            change_history = self.env["booking.change.history"].create(
                {
                    "booking_id": booking.id,  # booking obyektining ID'sini berish
                    "room_number": booking.room_number.id,
                    "user_id": self.env.uid,
                    "field_name": "Cancel check-in",
                    "old_value": " ",
                    "new_value": vals.get("reason"),
                }
            )
        return super().create(vals)


class CancelCheckout(models.Model):
    _name = "front_desk.cancel_checkout"
    _description = "Cancel Checkout"

    booking_id = fields.Many2one("booking", string="Booking")
    reason = fields.Char(string="Description")

    @api.model
    def create(self, vals):
        booking = self.env["booking"].search([("id", "=", vals["booking_id"])])
        if booking:
            if booking.is_check_out:
                booking.is_check_out = False
            else:
                raise ValidationError(
                    "This booking has not been previously checked-out"
                )
            change_history = self.env["booking.change.history"].create(
                {
                    "booking_id": booking.id,  # booking obyektining ID'sini berish
                    "room_number": booking.room_number.id,
                    "user_id": self.env.uid,
                    "field_name": "Cancel check-out",
                    "old_value": " ",
                    "new_value": vals.get("reason"),
                }
            )
        return super().create(vals)
