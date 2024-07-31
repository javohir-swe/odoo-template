from odoo import api, fields, models
from odoo.exceptions import ValidationError


class GuestDepositData(models.Model):
    _name = "deposit.data"
    _description = "Guest Deposit Data"
    _order = "created_at desc"

    guest_id = fields.Many2one("guest", string="Guest", required=True)
    booking_id = fields.Many2one("booking", string="Booking")
    deposit_data = fields.Many2one("guest")
    created_at = fields.Datetime(
        string="Date and time", default=fields.Datetime.now, readonly=True
    )
    amount = fields.Float(string="Amount", default=0)
    action_type = fields.Selection(
        [
            ("withdrawal", "Withdrawal"),
            ("penalty", "Penalty"),
            ("refund", "Refund"),
            ("payment", "Payment"),
        ],
        string="Action Type",
        default="payment",
    )


class Deposit(models.Model):
    _name = "reception.deposit"
    _description = "Hotel Deposit"

    invoice_id = fields.Many2one("reception.invoice", string="Invoice")
    booking_id = fields.Many2one("booking", string="Booking")
    guest_id = fields.Many2one(
        related="booking_id.guest_id", string="Guest", readonly=False
    )
    bill_to = fields.Many2one(related="booking_id.guest_id", string="Bill To")
    amount = fields.Float(string="Amount", default=0)
    total_deposit = fields.Float(
        string="Total Deposit", default=0, compute="_compute_total_deposit"
    )  # guest_id ichidagi deposit ga amount ni qo'shib yig'indini chiqarish kerak
    payment_date = fields.Datetime(string="Payment Date", default=fields.Datetime.now)
    comment = fields.Text(string="Payment Comment")
    action_type = fields.Selection(
        [
            ("withdrawal", "Withdrawal"),
            ("penalty", "Penalty"),
            ("refund", "Refund"),
            ("payment", "Payment"),
        ],
        string="Action Type",
        default="payment",
    )

    @api.constrains("amount")
    def _check_amount(self):
        for record in self:
            if record.amount < 0:
                raise ValidationError("Amount cannot be negative.")

    @api.depends("amount", "guest_id.deposit", "action_type")
    def _compute_total_deposit(self):
        for record in self:
            if record.guest_id:
                if record.action_type == "payment":
                    record.total_deposit = record.amount + record.guest_id.deposit
                else:
                    record.total_deposit = record.guest_id.deposit - record.amount
            else:
                record.total_deposit = record.amount

    # @api.model
    # def create(self, vals):
    #     deposit = super().create(vals)
    #     if deposit.guest_id:
    #         self.env["deposit.data"].create(
    #             {
    #                 "booking_id": deposit.booking_id.id,
    #                 "amount": deposit.amount,
    #                 "guest_id": deposit.guest_id.id,
    #                 "action_type": deposit.action_type,
    #             }
    #         )
    #     return deposit

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if (
                "amount" in vals
                or "booking_id" in vals
                or "guest_id" in vals
                or "action_type" in vals
            ):
                self.env["deposit.data"].create(
                    {
                        "booking_id": record.booking_id.id,
                        "amount": vals.get("amount", record.amount),
                        "guest_id": vals.get("guest_id", record.guest_id.id),
                        "action_type": vals.get("action_type", record.action_type),
                    }
                )
        return res
