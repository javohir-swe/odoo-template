from odoo import fields, models


class BookingReconciliation(models.Model):
    _name = "booking.reconciliation"
    _description = "Booking Reconciliation"

    booking_id = fields.Many2one("booking", string="Booking")
    status = fields.Boolean(string="Status")
    booking_number = fields.Char(string="Booking Number")
    guest_id = fields.Many2one("guest", string="Guest")
    check_in_date = fields.Date(
        string="Check-in Date",
        required=True,
    )
    check_out_date = fields.Date(
        string="Check-out Date",
        required=True,
    )
    check_in_time = fields.Many2one("check.in.check.out.time", string="Check In Time")
    checkout_time = fields.Many2one("check.in.check.out.time", string="Check Out Time")
    total = fields.Float(related="booking_id.total", string="Total")
    commission_amount = fields.Float(string="Commission Amount")
