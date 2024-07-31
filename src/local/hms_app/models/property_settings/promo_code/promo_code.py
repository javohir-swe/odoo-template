import random
import string

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PromoCodeValidDate(models.Model):
    _name = "property_settings.promo_code.valid_date"
    _description = "Promo Code Valid Date"
    _rec_name = "name_display"

    date_from = fields.Date(string="From", required=True)
    date_to = fields.Date(string="To", required=True)
    promocode_id = fields.Many2one("property_settings.promo_code", string="Company")
    name_display = fields.Char(string="Name Display", compute="_compute_name_display")

    @api.depends("date_from", "date_to", "promocode_id")
    def _compute_name_display(self):
        if self.promocode_id:
            self.name_display = self.promocode_id.name
        else:
            for record in self:
                record.name_display = f"{record.first_field} {record.second_field}"


class PromoCodeGroups(models.Model):
    _name = "promo_code.groups"
    _description = "Promo Code Groups"
    _rec_name = "group_name"

    group_name = fields.Char(string="Name", required=True)
    promo_code_ids = fields.Many2many(
        "property_settings.promo_code",
        "promo_code_group_rel",
        string="Number of Codes",
    )
    enabled = fields.Boolean(string="Enabled", default=True)
    view_rate_plans = fields.Boolean(string="View Rate Plans", default=True)
    number_of_codes = fields.Integer(
        string="Number of codes", compute="_compute_related_count"
    )

    @api.depends("promo_code_ids")
    def _compute_related_count(self):
        for record in self:
            record.number_of_codes = len(record.promo_code_ids)


class RatePlanSpecialOffers(models.Model):
    _name = "rate.plan.special.offers"
    _description = "Rate Plan Special Offers"
    _rec_name = "rate_plan_id"

    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")


class PromoCodes(models.Model):
    _name = "property_settings.promo_code"
    _description = "property_settings.promo_code"
    _rec_name = "promo_code"

    promo_code = fields.Char(string="Promo Code", required=True)
    status = fields.Boolean(string="Status", default=True)
    usage = fields.Selection(
        [
            ("not_limited", "Not Limited"),
            ("limited", "Limited within"),
        ],
        string="Usage",
        default="not_limited",
    )
    usage_limit = fields.Integer(string="Usage Limit", default=0)
    period_of_stay = fields.Selection(
        [
            ("valid_through", "Valid Through"),
            ("not_limited", "Not Limited"),
        ],
        string="Period of Stay",
        default="not_limited",
    )
    limited_dates = fields.One2many(
        "property_settings.promo_code.valid_date", "promocode_id"
    )
    used = fields.Integer(string="Used", default=0)
    group_ids = fields.Many2many(
        "promo_code.groups", "promo_code_group_rel", string="Groups"
    )
    category = fields.Char(string="Category", compute="_compute_related_groups")

    @api.depends("group_ids")
    def _compute_related_groups(self):
        for record in self:
            record.category = ", ".join(record.group_ids.mapped("group_name"))

    @api.model
    def create(self, vals):
        if vals.get("usage") == "not_limited":
            vals["usage_limit"] = 0
        if vals.get("period_of_stay") == "not_limited":
            vals["limited_dates"] = [(5, 0, 0)]  # Clear the one2many field
        return super().create(vals)

    def write(self, vals):
        if vals.get("usage") == "not_limited":
            vals["usage_limit"] = 0
        if vals.get("period_of_stay") == "not_limited":
            vals["limited_dates"] = [(5, 0, 0)]  # Clear the one2many field
        return super().write(vals)

    @api.constrains("usage_limit")
    def check_number(self):
        if self.usage_limit < 0:
            raise ValidationError("Number must be non-negative!")


class PromoCodeGenerateWizard(models.TransientModel):
    """
    Promo code generatsiya qilish uchun model
    bu yerdagi barcha ma'lumotlar generatsiya qilish uchun.
    """

    _name = "promo.code.generate.wizard"
    _description = "Promo Code Generate Wizard"

    quantity = fields.Selection(
        [
            ("50", "50"),
            ("100", "100"),
            ("250", "250"),
            ("500", "500"),
            ("1000", "1000"),
        ],
        string="Quantity",
        required=True,
    )
    prefix = fields.Char(string="Prefix", required=True)
    length = fields.Integer(string="Length", required=True)
    status = fields.Boolean(string="Enable all added promo codes", default=True)
    usage = fields.Selection(
        [
            ("not_limited", "Not Limited"),
            ("limited", "Limited within"),
        ],
        string="Usage",
        default="not_limited",
        required=True,
    )
    usage_limit = fields.Integer(string="Usage Limit", default=0)
    group_ids = fields.Many2many("promo_code.groups", string="Groups", required=True)
    digits = fields.Boolean(string="Use Digits", default=True)
    letters = fields.Boolean(string="Use Letters", default=False)

    def generate_promo_codes(self):
        PromoCode = self.env["property_settings.promo_code"]
        quantity = int(self.quantity)
        characters = ""
        if self.digits:
            characters += string.digits
        elif self.letters:
            characters += string.ascii_uppercase
        else:
            raise ValidationError("The promo codes structure isn't defined.")
        for _ in range(quantity):
            code = self.prefix + "".join(random.choices(characters, k=self.length))
            PromoCode.create(
                {
                    "promo_code": code,
                    "status": self.status,
                    "usage": self.usage,
                    "usage_limit": self.usage_limit,
                    "group_ids": [(6, 0, self.group_ids.ids)],
                }
            )
        return {"type": "ir.actions.act_window_close"}
