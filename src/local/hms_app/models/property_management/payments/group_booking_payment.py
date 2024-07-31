from odoo import api, fields, models


class GroupBookingPayment(models.Model):
    _name = "group_booking.payment"
    _description = "Group Booking Payment"

    name = fields.Char(string="Name", required=True)
    booking_id = fields.Many2one("booking", string="Booking")
    manage_invoice = fields.Selection(
        [("total_booking", "Total booking"), ("rooms", "Rooms")],
        default="total_booking",
        string="Manage Invoice",
    )
    payment_date = fields.Datetime(string="Payment Date", default=fields.Datetime.now)
    payment_method = fields.Selection(
        [
            (
                "bank_transfer_legal",
                "Bank transfer for legal entities (invoice issued by hotel)",
            ),
            (
                "bank_transfer_individual",
                "Bank transfer for individuals (invoice issued by hotel)",
            ),
            ("cash_cashbox", "By cash via cashbox"),
            ("card_terminal", "By card via terminal"),
        ],
        default="cash_cashbox",
        required=True,
        string="Payment Method",
    )
    comment = fields.Text(string="Comment")
    booking_invoices = fields.Many2many("reception.invoice")
    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount")
    is_payed = fields.Boolean(string="Is Payed")

    @api.onchange("is_payed")
    def _onchange_is_payed(self):
        if self.is_payed:
            for invoice in self.booking_invoices:
                invoice.status = "paid"

    @api.onchange("booking_id")
    def _onchange_booking_id(self):
        if self.booking_id:
            # Get the group_unique_id from the selected booking

            if self.booking_id.group_unique_id:
                group_unique_id = self.booking_id.group_unique_id

                # Find all reception.invoices with the same group_unique_id
                invoices = self.env["reception.invoice"].search(
                    [("booking_id.group_unique_id", "=", group_unique_id)]
                )

                # Set the found invoices to booking_invoices
                self.booking_invoices = [(6, 0, invoices.ids)]

    @api.depends("booking_invoices")
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.booking_invoices.mapped("to_be_paid"))
