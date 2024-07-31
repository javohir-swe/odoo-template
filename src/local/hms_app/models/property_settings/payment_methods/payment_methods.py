from odoo import api, fields, models


class PaymentMethodsForGuests(models.Model):
    _name = "payment.methods.for.guests"
    _description = "Payment method"

    # Name and logo
    sequence = fields.Integer("Sequence", help="Determines the order of items")
    name = fields.Char(required=True, string="Payment method name")
    color = fields.Integer(string="Color Index", default=0)
    allow_cancel = fields.Boolean(string="Allow guest to cancel booking", default=True)
    privacy_policy_date = fields.Selection(
        [
            ("no_less", "no less"),
            ("no_more", "no more"),
            ("always", "always"),
        ]
    )
    payment_method_is_available_num = fields.Integer(
        string="Payment method is available number"
    )
    payment_method_is_available = fields.Selection(
        [
            ("hours", "hours"),
            ("days", "days"),
        ]
    )
    rate_plan_ids = fields.Many2many(
        "rate.plan",
        "rate_plan_payment_method_rel",
        "payment_method_id",
        "rate_plan_id",
        string="Rate Plans",
        required=True,
    )

    related_count = fields.Integer(
        string="Related Count", compute="_compute_related_count"
    )
    combined_field = fields.Char(
        string="Exely Booking Engine availability", compute="_compute_combined_field"
    )
    status_tag = fields.Char(compute="_compute_status_tag", store=False)

    # rate planlar sonini aniqlash
    @api.depends("rate_plan_ids")
    def _compute_related_count(self):
        for record in self:
            record.related_count = len(record.rate_plan_ids)

    # privacy_policy_date valuesi always bo'lganda pastdagi fieldlarni tozalash
    @api.onchange("privacy_policy_date")
    def _onchange_privacy_policy_date(self):
        if self.privacy_policy_date == "always":
            self.payment_method_is_available_num = 0
            self.payment_method_is_available = ""

    # Define a dictionary to map selection values to their labels
    def _get_label_from_value(self, selection, value):
        return dict(selection).get(value, value)

    @api.depends(
        "privacy_policy_date",
        "payment_method_is_available",
        "payment_method_is_available_num",
    )
    def _compute_combined_field(self):
        for record in self:
            privacy_policy_date_label = self._get_label_from_value(
                self._fields["privacy_policy_date"].selection,
                record.privacy_policy_date,
            )
            payment_method_is_available_label = self._get_label_from_value(
                self._fields["payment_method_is_available"].selection,
                record.payment_method_is_available,
            )
            record.combined_field = f"{privacy_policy_date_label or ''} {record.payment_method_is_available_num or ''} {payment_method_is_available_label or ''}".strip()

    @api.depends("allow_cancel")
    def _compute_status_tag(self):
        for record in self:
            record.status_tag = "Allowed" if record.allow_cancel else "Not Allowed"

    @api.model
    def create(self, values):
        if values.get("privacy_policy_date") == "always":
            values["payment_method_is_available_num"] = 0
            values["payment_method_is_available"] = ""
        return super().create(values)

    def write(self, values):
        if values.get("privacy_policy_date") == "always":
            values["payment_method_is_available_num"] = 0
            values["payment_method_is_available"] = ""
        return super().write(values)
