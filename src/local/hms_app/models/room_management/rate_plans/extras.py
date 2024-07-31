from datetime import timedelta

from odoo import api, fields, models


class ExtrasService(models.Model):
    _name = "rate_plan.service"
    _description = "Extra Service"

    name = fields.Char("Service", required=True)


class Extras(models.Model):
    _name = "rate_plan.extras"
    _description = "Rate plan display on the website in Exely Booking Engine"
    _rec_name = "service_name"

    status = fields.Boolean("Status", default=True)
    service_name = fields.Many2one(
        "services.settings",
        string="Service",
        required=True,
        # domain=lambda self: self._get_available_services_domain(),
    )
    service_type = fields.Selection(
        related="service_name.service_type", string="Type", required=True
    )
    room_types_count = fields.Char("Room Type", compute="_compute_related_count")
    room_types = fields.Many2many(
        "triple",
        "extras_triple_rel",
        "extras_id",
        "triple_id",
        string="Room Types",
    )
    included_or_extra = fields.Selection(
        [
            ("for_extra_cost", "For extra cost"),
            ("included_in_the_rate_plan", "Included in the rate plan"),
        ],
        default="included_in_the_rate_plan",
        string="Included or Extra",
    )
    extra_id = fields.Many2one("rate.plan", string="Extra")
    status_tag = fields.Char(compute="_compute_status_tag", store=False)
    booking_id = fields.Many2one("booking", ondelete="set null")
    delivery_date = fields.Date(
        string="Delivery Date",
        default=lambda self: fields.Date.today() + timedelta(days=1),
    )
    price = fields.Float(
        related="service_name.service_price_usd", string="Price", default=0.0
    )
    quantity = fields.Integer(string="Quantity", default=1)
    amount = fields.Float(string="Amount", compute="_compute_amount", store=True)
    comment = fields.Text(string="Comment")

    @api.depends("price", "quantity")
    def _compute_amount(self):
        for record in self:
            record.amount = record.price * record.quantity

    @api.depends("status")
    def _compute_status_tag(self):
        for record in self:
            record.status_tag = "Active" if record.status else "Inactive"

    @api.depends("room_types")
    def _compute_related_count(self):
        for record in self:
            record.room_types_count = len(record.room_types)

    def _get_available_services_domain(self):
        # Get all the ids of services already selected in other Extras
        used_service_ids = (
            self.env["rate_plan.extras"]
            .search([("service_name", "!=", False)])
            .mapped("service_name.id")
        )
        # Create a domain to exclude these ids
        return [("id", "not in", used_service_ids)]
