from odoo import models, fields, api
import math


class RoundingRule(models.Model):
    _name = "rounding.rule"
    _description = "Rounding Rule for Room Prices"

    price_per_room = fields.Float(string="Price Per Room")
    round_rate = fields.Float(string="Rounded Rate", compute="_compute_rounded_rate")
    price_per_room_2 = fields.Float(string="Price Per Room 2")
    round_rate_2 = fields.Float(
        string="Rounded Rate 2", compute="_compute_rounded_rate"
    )
    rounding_size = fields.Selection(
        [
            ("0.01", "up to UZS 0.01"),
            ("0.05", "up to UZS 0.05"),
            ("0.10", "up to UZS 0.10"),
            ("0.50", "up to UZS 0.50"),
            ("1", "up to UZS 1"),
            ("5", "up to UZS 5"),
            ("10", "up to UZS 10"),
            ("100", "up to UZS 100"),
        ],
        string="Rounding Size",
        required=True,
        default="0.01",
    )
    rounding_rule = fields.Selection(
        [
            ("nearest", "Up to the Nearest Number"),
            ("up", "Up to the Larger Number"),
            ("down", "Down to the Nearest Number"),
        ],
        string="Rounding Rule",
        required=True,
        default="nearest",
    )
    name = fields.Char(
        compute="_compute_name", string="Rule Name", store=True, readonly=True
    )

    @api.depends("rounding_size", "rounding_rule")
    def _compute_name(self):
        for record in self:
            size_label = dict(self._fields["rounding_size"].selection).get(
                record.rounding_size
            )
            rule_label = dict(self._fields["rounding_rule"].selection).get(
                record.rounding_rule
            )
            record.name = "Round up to {}, {}".format(size_label, rule_label)

    @api.onchange(
        "price_per_room",
        "price_per_room_2",
        "rounding_size",
        "rounding_rule",
    )
    def _compute_rounded_rate(self):
        rounding_fields = [
            ("price_per_room", "round_rate"),
            ("price_per_room_2", "round_rate_2"),
        ]

        for price_field, rate_field in rounding_fields:
            price = getattr(self, price_field)
            if price:
                multiplier = 1 / float(self.rounding_size)
                if self.rounding_rule == "nearest":
                    rounded_price = round(price * multiplier) / multiplier
                elif self.rounding_rule == "up":
                    rounded_price = math.ceil(price * multiplier) / multiplier
                elif self.rounding_rule == "down":
                    rounded_price = math.floor(price * multiplier) / multiplier

                setattr(self, rate_field, rounded_price)
