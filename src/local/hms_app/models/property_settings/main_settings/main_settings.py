import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError

from ...data import ALL_TIMES


class EmailAddress(models.Model):
    _name = "email.address"
    _description = "Email Address"
    _rec_name = "email"

    email = fields.Char(string="Email", required=True)


class BaseTypes(models.Model):
    _name = "base.types"
    _description = "Base Types"

    name = fields.Char(string="Name", required=True)


class State(models.Model):
    _name = "state"
    _description = "State"
    _rec_name = "region"

    region = fields.Char(string="Region", required=True)


class City(models.Model):
    _name = "city"
    _description = "City"
    _rec_name = "city"

    city = fields.Char(string="City", required=True)
    region_id = fields.Many2one("state", string="Region", required=True)


class ResCompany(models.Model):
    _inherit = "res.company"

    logo = fields.Binary(string="Company Logo")
    file_data = fields.Binary(string="Upload File", attachment=True)
    child_ages = fields.One2many(
        "child.age.range", "company_id", string="Child Age Range"
    )
    get_directions = fields.Text(string="Get Directions")
    check_in_times = fields.One2many(
        "check.in.check.out.time", "company_id", string="Check In Time"
    )
    check_out_times = fields.One2many(
        "check.in.check.out.time", "company_id", string="Check Out Time"
    )
    check_in_time = fields.Selection(
        ALL_TIMES,
        string="Check In Time",
        store=True,
    )
    check_out_time = fields.Selection(
        ALL_TIMES,
        string="Check Out Time",
        store=True,
    )

    # get_directions = fields.Binary(string="Get Directions")


class MainSettings(models.TransientModel):
    # _name = "main.settings"
    _description = "Main Settings"
    _inherit = "res.config.settings"

    # Name and logo
    type_id = fields.Many2one(
        "base.types",
        string="Type",
        config_parameter="property_settings.type_id",
        required=True,
    )
    name = fields.Char(
        string="Name", config_parameter="property_settings.name", required=True
    )
    name_in_english = fields.Char(
        string="Name in English",
        config_parameter="property_settings.name_in_english",
        required=True,
    )
    # company_logo = fields.Binary(
    #     string="Company Logo", related="env.company.logo", readonly=False
    # )
    # Privacy policy
    privacy_policy_date = fields.Selection(
        [
            ("unlimited", "Unlimited"),
            ("3_years", "3 Years"),
            ("1_year", "1 Year"),
            ("6_months", "6 Months"),
            ("1_month", "1 Month"),
        ],
        string="Data retention expiry period from the check-out date",
        default="unlimited",
        config_parameter="property_settings.privacy_policy_date",
    )

    # Check-in and check-out
    # check_in = fields.Float(
    #     string="Check-In Time",
    #     default=0.0,
    #     config_parameter="property_settings.check_in",
    # )
    # check_out = fields.Float(
    #     string="Check-Out Time",
    #     default=0.0,
    #     config_parameter="property_settings.check_out",
    # )
    # check_in = fields.Many2one("check.in.check.out.time", string="Check Out Time")
    # check_out = fields.Many2one("check.in.check.out.time", string="Check Out Time")
    check_in_times = fields.Many2one(
        "check.in.check.out.time",
        string="Check In Time",
        config_parameter="property_settings.check_in_time",
        # required=True,
    )
    check_out_times = fields.Many2one(
        "check.in.check.out.time",
        string="Check Out Time",
        config_parameter="property_settings.check_out_time",
        #         required=True,
    )
    check_in_time = fields.Selection(
        ALL_TIMES,
        string="Check In Time",
        config_parameter="property_settings.check_in_times",
        default="14:00",
        required=True,
        readonly=False,
        store=True,
    )
    check_out_time = fields.Selection(
        ALL_TIMES,
        string="Check Out Time",
        config_parameter="property_settings.check_out_times",
        default="12:00",
        required=True,
        readonly=False,
        store=True,
    )

    # Weekend days
    monday = fields.Boolean(
        string="Monday",
        config_parameter="property_settings.monday",
        required=True,
        default=False,
    )
    tuesday = fields.Boolean(
        string="Tuesday",
        config_parameter="property_settings.tuesday",
        required=True,
        default=False,
    )
    wednesday = fields.Boolean(
        string="Wednesday",
        config_parameter="property_settings.wednesday",
        required=True,
        default=False,
    )
    thursday = fields.Boolean(
        string="Thursday",
        config_parameter="property_settings.thursday",
        required=True,
        default=False,
    )
    friday = fields.Boolean(
        string="Friday",
        config_parameter="property_settings.friday",
        required=True,
        default=False,
    )
    weekend = fields.Boolean(
        string="Weekend",
        config_parameter="property_settings.weekend",
        required=True,
        default=False,
    )
    saturday = fields.Boolean(
        string="Saturday",
        config_parameter="property_settings.saturday",
        required=True,
        default=True,
    )
    sunday = fields.Boolean(
        string="Sunday",
        config_parameter="property_settings.sunday",
        required=True,
        default=True,
    )

    # Child age
    child_age_start = fields.Integer(string="Child Age Start")
    child_age_end = fields.Integer(string="Child Age End")

    child_age_ids = fields.One2many(
        "child.age.range",
        related="company_id.child_ages",
        string="Child Age Range",
        readonly=False,
        required=True,
    )

    # Address
    postal_code = fields.Integer(
        string="Postal Code",
        config_parameter="property_settings.postal_code",
        required=True,
    )
    state_id = fields.Many2one(
        "state",
        string="State",
        config_parameter="property_settings.state_id",
        required=True,
    )
    district = fields.Char(
        string="District", config_parameter="property_settings.district", required=True
    )
    city_id = fields.Many2one(
        "city", string="City", config_parameter="property_settings.city_id"
    )
    street = fields.Char(string="Street", config_parameter="property_settings.street")
    house_number = fields.Integer(
        string="House Number", config_parameter="property_settings.house_number"
    )
    littera = fields.Char(
        string="Littera", config_parameter="property_settings.littera"
    )
    building = fields.Char(
        string="Building", config_parameter="property_settings.building"
    )
    construction = fields.Char(
        string="Construction", config_parameter="property_settings.construction"
    )

    # data for location
    latitude = fields.Float(
        string="Latitude", config_parameter="property_settings.latitude"
    )
    longitude = fields.Float(
        string="Longitude", config_parameter="property_settings.longitude"
    )
    get_directions = fields.Text(
        string="Get Directions",
        related="company_id.get_directions",
        readonly=False,
        help="Route description to your accommodation property will be displayed in booking confirmations and will help a guest to easily find your location.",
    )

    # Phone
    # Main phone number
    main_phone = fields.Char(
        string="Main phone",
        config_parameter="property_settings.main_phone",
        required=True,
    )
    main_comment = fields.Char(
        string="Main comment", config_parameter="property_settings.main_comment"
    )

    # Additional phone 1
    phone_1 = fields.Char(
        string="Secondary phone", config_parameter="property_settings.phone_1"
    )
    comment_1 = fields.Char(
        string="Secondary comment", config_parameter="property_settings.comment_1"
    )

    # Additional phone 2
    phone_2 = fields.Char(
        string="Tertiary phone", config_parameter="property_settings.phone_2"
    )
    comment_2 = fields.Char(
        string="Tertiary comment", config_parameter="property_settings.comment_2"
    )

    # Additional phone 3
    phone_3 = fields.Char(
        string="Fourth phone", config_parameter="property_settings.phone_3"
    )
    comment_3 = fields.Char(
        string="Fourth comment", config_parameter="property_settings.comment_3"
    )

    # Email
    email_for_guests = fields.Char(
        string="Email for Guests",
        config_parameter="property_settings.email_for_guests",
        required=True,
    )
    email_for_notifications = fields.Char(
        string="Email for Notifications",
        config_parameter="property_settings.email_for_notifications",
    )
    additional_email = fields.Char(
        string="Additional Email", config_parameter="property_settings.additional_email"
    )

    # Guest confirmation settings
    file_data = fields.Binary(
        string="Upload File", related="company_id.file_data", readonly=False
    )
    file_name = fields.Char(
        string="File Name", config_parameter="property_settings.file_name"
    )

    # ishlaydigan telefon raqam validatsiya
    @api.constrains("main_phone")
    def check_phone(self):
        pattern = re.compile(
            r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
        )  # regex pattern for international phone format with optional extension
        for record in self:
            if record.main_phone and not pattern.match(record.main_phone):
                raise ValidationError("Main phone number is not in the correct format.")

    # ishlaydigan email validatsiya
    @api.model
    def create(self, vals):
        if "email_for_guests" in vals and vals["email_for_guests"] is not False:
            self._validate_email(vals["email_for_guests"])
        # Repeat for other email fields
        return super().create(vals)

    def write(self, vals):
        if "email_for_guests" in vals and vals["email_for_guests"] is not False:
            self._validate_email(vals["email_for_guests"])
        # Repeat for other email fields
        return super().write(vals)

    def _validate_email(self, email):
        if email and not isinstance(email, str):
            raise ValidationError("Email value must be a string.")
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Invalid email format: %s" % email)
