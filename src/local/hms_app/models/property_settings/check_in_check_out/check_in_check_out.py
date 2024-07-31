from odoo import api, exceptions, fields, models

from ...data import ALL_TIMES


class AllTimes(models.Model):
    _name = "all.times"
    _description = "All Times"
    _rec_name = "time"

    time = fields.Float(
        string="Time"
    )  # In Odoo, time fields are usually represented as Float


class CheckInCheckOutTime(models.Model):
    _name = "check.in.check.out.time"
    _description = "Check In Check Out Time"

    name = fields.Char(string="Name", compute="_compute_name")
    surcharge_for_late_check_out = fields.Selection(
        [
            ("free_of_charge", "Free of charge"),
            ("fixed_rate", "Fixed rate"),
            ("percent_of_the_day_rate", "Percent of the day rate"),
            ("hourly_fixed_rate", "Hourly fixed rate"),
            ("hourly_auto_calculated_price", "Hourly auto-calculated price"),
            ("no_early_check_in_late_check_out", "No early check-in/late check-out"),
        ],
        string="Surcharge For Late Check-Out",
    )
    select_the_availability = fields.Boolean(
        string="Select The Availability",
    )
    rate_price = fields.Integer(string="Rate Plan Price")
    rate_percent = fields.Integer(string="Rate Plan Percentage")
    rate_price_currency = fields.Selection(
        [("UZS", "UZS"), ("USD", "USD"), ("RUB", "RUB")],
        string="Rate Plan Price Currency",
        default="UZS",
    )
    availability_text = fields.Char(
        string="Select the availability",
        compute="_compute_availability",
    )
    display_value = fields.Char(
        string="Rate plan",
        compute="_compute_display_value",
    )
    half_hour_intervals = fields.Selection(ALL_TIMES, string="Half Hour Intervals")
    company_id = fields.Many2one("res.company", string="Company")

    # for front desk

    reason = fields.Text(string="Reason")

    @api.depends("select_the_availability")
    def _compute_availability(self):
        for record in self:
            record.availability_text = "Yes" if record.select_the_availability else "No"

    @api.depends(
        "surcharge_for_late_check_out",
        "rate_price",
        "rate_percent",
        "rate_price_currency",
    )
    def _compute_display_value(self):
        for record in self:
            if (
                record.surcharge_for_late_check_out == "fixed_rate"
                or record.surcharge_for_late_check_out == "hourly_fixed_rate"
            ):
                record.display_value = (
                    f"{record.rate_price} {record.rate_price_currency}"
                )
            elif record.surcharge_for_late_check_out == "percent_of_the_day_rate":
                record.display_value = f"{record.rate_percent} %"
            else:
                record.display_value = ""

    @api.onchange("half_hour_intervals", "rate_price", "rate_price_currency")
    def _compute_name(self):
        for record in self:
            if (
                record.half_hour_intervals
                and record.rate_price
                and record.rate_price_currency
            ):
                record.name = f"{record.half_hour_intervals} - {record.rate_price} {record.rate_price_currency}"
            else:
                record.name = record.half_hour_intervals


class CheckInCheckOutRoles(models.Model):
    _name = "check.in.check.out.roles"
    _description = "Check In Check Out Roles"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    check_in_time = fields.Float(string="Check In Time")
    from_main_settings = fields.Boolean(string="From Main Settings")
    check_in_time_data = fields.One2many("check.in.check.out.settings", "role_id")
    include_a_surcharge_for_early_check_in_in_the_prepayment = fields.Boolean(
        string="Include a Surcharge for Early Check-In in the Prepayment"
    )
    allow_guests_to_book_early_check_in_in_exely_booking_engine = fields.Boolean(
        string="Allow Guests to Book Early Check-In in Exely Booking Engine"
    )
    check_out_time = fields.Float(string="Check Out Time")
    from_main_settings_2 = fields.Boolean(string="From Main Settings 2")
    check_out_time_data = fields.One2many("check.out.settings", "role_id")
    include_a_surcharge_for_early_check_out_in_the_prepayment = fields.Boolean(
        string="Include a Surcharge for Early Check-Out in the Prepayment"
    )
    allow_guests_to_book_early_check_out_in_exely_booking_engine = fields.Boolean(
        string="Allow Guests to Book Early Check-Out in Exely Booking Engine"
    )

    @api.onchange("from_main_settings")
    def _onchange_from_main_settings(self):
        if self.from_main_settings:
            check_in_time_str = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("property_settings.check_in_times", default="14:00")
            )
            self.check_in_time = self._convert_time_to_float(check_in_time_str)

    @api.onchange("from_main_settings_2")
    def _onchange_from_main_settings_2(self):
        if self.from_main_settings_2:
            check_out_time_str = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("property_settings.check_out_times", default="12:00")
            )
            self.check_out_time = self._convert_time_to_float(check_out_time_str)

    def _convert_time_to_float(self, time_str):
        hours, minutes = map(int, time_str.split(":"))
        return hours + minutes / 60.0

    @api.model
    def create(self, vals):
        if vals.get("from_main_settings"):
            check_in_time_str = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("property_settings.check_in_times", default="14:00")
            )
            vals["check_in_time"] = self._convert_time_to_float(check_in_time_str)
        if vals.get("from_main_settings_2"):
            check_out_time_str = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("property_settings.check_out_times", default="12:00")
            )
            vals["check_out_time"] = self._convert_time_to_float(check_out_time_str)
        return super().create(vals)

    def write(self, vals):
        if vals.get("from_main_settings"):
            check_in_time_str = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("property_settings.check_in_times", default="14:00")
            )
            vals["check_in_time"] = self._convert_time_to_float(check_in_time_str)
        if vals.get("from_main_settings_2"):
            check_out_time_str = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("property_settings.check_out_times", default="12:00")
            )
            vals["check_out_time"] = self._convert_time_to_float(check_out_time_str)
        return super().write(vals)


class EarlyCheckinSettings(models.Model):
    _name = "check.in.check.out.settings"
    _description = "Check In Check Out Settings"

    checkin_times = fields.Float(string="Check In Time")
    valid_from_ = fields.Float(string="Valid From")
    valid_till_ = fields.Float(string="Valid Till")
    charge_rule = fields.Selection(
        [
            ("free", "Free of charge"),
            ("fixed_rate", "Fixed rate"),
            ("percent", "Percent of the day rate"),
            ("hourly_fixed_rate", "Hourly fixed rate"),
            ("hourly_auto_calculated_price", "Hourly auto-calculated price"),
            ("no_early_checkin_late_check_out", "No Early Check-In/Late Check-Out"),
        ],
        string="Charge Rule",
        default="free",
        required=True,
    )
    percent = fields.Integer(string="Percent")
    value = fields.Float(string="Value")
    value_uzs = fields.Float(string="UZS")
    value_usd = fields.Float(string="USD")
    value_rub = fields.Float(string="RUB")
    invisible_price = fields.Boolean(
        string="Invisible Price", default=True, compute="_compute_invisible_price"
    )
    role_id = fields.Many2one("check.in.check.out.roles")

    @api.depends("charge_rule")
    def _compute_invisible_price(self):
        for record in self:
            if (
                record.charge_rule == "free"
                or record.charge_rule == "percent"
                or record.charge_rule == "no_early_checkin_late_check_out"
                or record.charge_rule == "hourly_auto_calculated_price"
            ):
                record.invisible_price = True
            else:
                record.invisible_price = False

    @api.constrains("checkin_times", "valid_from_", "valid_till_")
    def _check_time_validity(self):
        for record in self:
            self._validate_time(record.checkin_times, "Check In Time")
            self._validate_time(record.valid_from_, "Valid From Time")
            self._validate_time(record.valid_till_, "Valid Till Time")

    def _validate_time(self, time_value, field_name):
        hours = int(time_value)
        minutes = (time_value * 60) % 60
        if not (0 <= hours < 24):
            raise exceptions.ValidationError(
                f"{field_name} must have hours between 0 and 24."
            )
        if not (0 <= minutes < 60):
            raise exceptions.ValidationError(
                f"{field_name} must have minutes between 0 and 59."
            )


class LateCheckOutSettings(models.Model):
    _name = "check.out.settings"
    _description = "Out Settings"

    checkin_times = fields.Float(string="Check In Time")
    valid_from_ = fields.Float(string="Valid From")
    valid_till_ = fields.Float(string="Valid Till")
    charge_rule = fields.Selection(
        [
            ("free", "Free of charge"),
            ("fixed_rate", "Fixed rate"),
            ("percent", "Percent of the day rate"),
            ("hourly_fixed_rate", "Hourly fixed rate"),
            ("hourly_auto_calculated_price", "Hourly auto-calculated price"),
            ("no_early_checkin_late_check_out", "No Early Check-In/Late Check-Out"),
        ],
        string="Charge Rule",
        default="free",
        required=True,
    )
    value = fields.Float(string="Value")
    value_uzs = fields.Float(string="UZS")
    value_usd = fields.Float(string="USD")
    value_rub = fields.Float(string="RUB")
    invisible_price = fields.Boolean(
        string="Invisible Price", default=True, compute="_compute_invisible_price"
    )
    role_id = fields.Many2one("check.in.check.out.roles")

    @api.depends("charge_rule")
    def _compute_invisible_price(self):
        for record in self:
            if (
                record.charge_rule == "free"
                or record.charge_rule == "percent"
                or record.charge_rule == "no_early_checkin_late_check_out"
                or record.charge_rule == "hourly_auto_calculated_price"
            ):
                record.invisible_price = True
            else:
                record.invisible_price = False

    @api.constrains("checkin_times", "valid_from_", "valid_till_")
    def _check_time_validity(self):
        for record in self:
            self._validate_time(record.checkin_times, "Check In Time")
            self._validate_time(record.valid_from_, "Valid From Time")
            self._validate_time(record.valid_till_, "Valid Till Time")

    def _validate_time(self, time_value, field_name):
        hours = int(time_value)
        minutes = (time_value * 60) % 60
        if not (0 <= hours < 24):
            raise exceptions.ValidationError(
                f"{field_name} must have hours between 0 and 24."
            )
        if not (0 <= minutes < 60):
            raise exceptions.ValidationError(
                f"{field_name} must have minutes between 0 and 59."
            )
