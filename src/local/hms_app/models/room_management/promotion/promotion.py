from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PromotionTypes(models.Model):
    _name = "promotion.types"
    _description = "Promotion Types"

    name = fields.Char(string="Type")


class Promotion(models.Model):
    _name = "promotion"
    _description = "Promotion"

    # title = fields.Char(compute="_compute_title")
    type = fields.Many2one("promotion.types", string="Type")
    name = fields.Char(string="Name")
    tree_amount = fields.Char(string="Amount", compute="_compute_tree_amount")
    amount = fields.Integer(string="Amount %")
    rounding_rule = fields.Many2one("rounding.rule", string="Rounding Rule")
    period_of_stay = fields.Char(
        string="Period of stay", compute="_compute_period_of_stay"
    )
    period_of_stay_from = fields.Date(string="Valid From")
    period_of_stay_to = fields.Date(string="Valid To", store=True)
    period_not_limit = fields.Boolean(string="No Period Limit", default=False)
    discount_is_displayed = fields.Char(
        string="Discount Display Period", compute="_compute_discount_is_displayed"
    )
    discount_is_displayed_from = fields.Date(string="Display From")
    discount_is_displayed_to = fields.Date(string="Display To", store=True)
    discount_not_limit = fields.Boolean(string="No Discount Limit", default=False)
    rate_plans = fields.Many2many(
        "rate.plan",
        string="Rate Plans",
        relation="promotion_rate_plan_rel",  # Optional: Odoo will create if not provided
        column1="promotion_id",  # Column referring to "promotion" in the relation table
        column2="rate_plan_id",  # Column referring to "rate.plan" in the relation table
    )

    room_types = fields.Many2many(
        "triple",
        string="Room Types",
        relation="promotion_room_type_rel",  # Optional: Odoo will create if not provided
        column1="promotion_id",  # Column referring to "promotion" in the relation table
        column2="room_type_id",  # Column referring to "room.type" in the relation table
    )
    room_types_count = fields.Integer(
        string="Room Types Count", compute="_compute_room_types_count"
    )
    rate_plans_count = fields.Integer(
        string="Rate Plans Count", compute="_compute_rate_plans_count"
    )

    @api.constrains("period_of_stay_from", "period_of_stay_to")
    def _check_period_of_stay(self):
        for record in self:
            if record.period_of_stay_from and record.period_of_stay_to:
                if record.period_of_stay_from > record.period_of_stay_to:
                    raise ValidationError(
                        "The start of the period of stay cannot be later than the end of the period."
                    )

    @api.constrains("discount_is_displayed_from", "discount_is_displayed_to")
    def _check_discount_display_period(self):
        for record in self:
            if record.discount_is_displayed_from and record.discount_is_displayed_to:
                if record.discount_is_displayed_from > record.discount_is_displayed_to:
                    raise ValidationError(
                        "The start of the discount display period cannot be later than the end of the display period."
                    )

    @api.depends("discount_is_displayed_from", "discount_is_displayed_to")
    def _compute_discount_is_displayed(self):
        for record in self:
            if record.discount_is_displayed_from and record.discount_is_displayed_to:
                record.discount_is_displayed = f"{record.discount_is_displayed_from} — {record.discount_is_displayed_to}"
            elif record.discount_is_displayed_from:
                record.discount_is_displayed = (
                    f"{record.discount_is_displayed_from} — not limited"
                )
            elif record.discount_is_displayed_to:
                record.discount_is_displayed = (
                    f"not included — {record.discount_is_displayed_to}"
                )
            else:
                record.discount_is_displayed = "not included — not limited"

    @api.depends("period_of_stay_from", "period_of_stay_to")
    def _compute_period_of_stay(self):
        for record in self:
            if record.period_of_stay_from and record.period_of_stay_to:
                record.period_of_stay = (
                    f"{record.period_of_stay_from} — {record.period_of_stay_to}"
                )
            elif record.period_of_stay_from:
                record.period_of_stay = f"{record.period_of_stay_from} — not limited"
            elif record.period_of_stay_to:
                record.period_of_stay = f"not included — {record.period_of_stay_to}"
            else:
                record.period_of_stay = "not included — not limited"

    @api.depends("amount")
    def _compute_tree_amount(self):
        for record in self:
            # Bu yerda amount maydonini tekshirib, tree_amount ga qiymat yoziladi
            record.tree_amount = "{}%".format(record.amount) if record.amount else ""

    @api.depends("rate_plans")
    def _compute_rate_plans_count(self):
        for record in self:
            record.rate_plans_count = int(len(record.rate_plans))

    @api.depends("room_types")
    def _compute_room_types_count(self):
        for record in self:
            record.room_types_count = int(len(record.room_types))

    @api.onchange("discount_not_limit")
    def _onchange_discount_limit(self):
        if self.discount_not_limit:
            self.discount_is_displayed_to = False

    @api.onchange("period_not_limit")
    def _onchange_period_limit(self):
        if self.period_not_limit:
            self.period_of_stay_to = False

    def write(self, values):
        # If 'period_not_limit' is being set to True, clear 'period_of_stay_to'
        if "period_not_limit" in values and values["period_not_limit"]:
            values["period_of_stay_to"] = False

        # If 'discount_not_limit' is being set to True, clear 'discount_is_displayed_to'
        if "discount_not_limit" in values and values["discount_not_limit"]:
            values["discount_is_displayed_to"] = False

        return super(Promotion, self).write(values)
