from odoo import api, fields, models


class CancellationTerms(models.Model):
    _name = "cancellation.terms"
    _description = "Cancellation Terms"
    _rec_name = "penalty"

    penalty = fields.Selection(
        [
            ("no_fine", "No fine"),
            ("first_day", "First day"),
            ("amount_prepayment", "The amount of the prepayment, %"),
            ("from_first_day", "From the first day, %"),
        ],
        string="Penalty",
        required=True,
        default="first_day",
    )
    percentage = fields.Integer(default=1)
    invisable_percentage = fields.Boolean(default=True)
    period_title = fields.Char(string="Period Title", compute="_compute_period_title")
    period_before_arrival = fields.Selection(
        [
            ("any", "Any"),
            ("more", "More"),
            ("less", "Less"),
            ("within_period", "Within a period"),
        ],
        string="Period Before Arrival",
        required=True,
        default="less",
    )
    invisable_periods = fields.Boolean(default=True)
    invisable_periods_till = fields.Boolean(default=True)
    number_of_days_hours = fields.Integer()
    number_of_days_hours_till = fields.Integer()
    days_hours = fields.Selection(
        [
            ("days", "days"),
            ("hours", "hours"),
        ],
        default="hours",
    )
    arrival_dates = fields.Char(
        string="Arrival dates", compute="_compute_arrival_dates"
    )
    arrival_dates_from = fields.Date(
        string="Arrival Dates From", default=fields.Date.context_today
    )
    arrival_dates_to = fields.Date(
        string="Arrival Dates To", default=fields.Date.context_today
    )
    not_limited = fields.Boolean(string="Not Limited")

    cancellation_policy = fields.Many2one("rule.name")

    @api.onchange("penalty")
    def _onchange_penalty(self):
        if self.penalty in ["no_fine", "first_day"]:
            self.percentage = 0
            self.invisable_percentage = True
        elif self.penalty in ["amount_prepayment", "from_first_day"]:
            self.percentage = 1
            self.invisable_percentage = False

    @api.onchange("period_before_arrival")
    def _onchange_period_before_arrival(self):
        if self.period_before_arrival in ["more", "less"]:
            self.invisable_periods = False
            self.invisable_periods_till = True
        elif self.period_before_arrival in ["any"]:
            self.invisable_periods_till = True
            self.invisable_periods = True
        elif self.period_before_arrival in ["within_period"]:
            self.invisable_periods = False
            self.invisable_periods_till = False

    @api.onchange("not_limited")
    def _onchange_not_limited(self):
        if self.not_limited:
            self.arrival_dates_to = False
        else:
            self.arrival_dates_to = fields.Date.context_today(self)

    @api.model
    def create(self, vals):
        if vals.get("not_limited"):
            vals["arrival_dates_to"] = False
        return super().create(vals)

    def write(self, vals):
        if "not_limited" in vals and vals["not_limited"]:
            vals["arrival_dates_to"] = False
        return super().write(vals)

    @api.depends(
        "period_before_arrival",
        "number_of_days_hours",
        "days_hours",
        "number_of_days_hours_till",
    )
    def _compute_period_title(self):
        for record in self:
            if record.period_before_arrival == "any":
                record.period_title = "Any"
            elif record.period_before_arrival in ["more", "less"]:
                record.period_title = f"{record.period_before_arrival.capitalize()} {record.number_of_days_hours} {record.days_hours}"
            elif record.period_before_arrival == "within_period":
                record.period_title = f"Within a period from {record.number_of_days_hours} till {record.number_of_days_hours_till} {record.days_hours}"
            else:
                record.period_title = ""

    @api.depends("arrival_dates_from", "arrival_dates_to")
    def _compute_arrival_dates(self):
        for record in self:
            if record.arrival_dates_from and not record.arrival_dates_to:
                record.arrival_dates = (
                    f"Unlimited from {record.arrival_dates_from.strftime('%d.%m.%Y')}"
                )
            elif record.arrival_dates_from and record.arrival_dates_to:
                record.arrival_dates = f"{record.arrival_dates_from.strftime('%d.%m.%Y')} - {record.arrival_dates_to.strftime('%d.%m.%Y')}"
            else:
                record.arrival_dates = ""
