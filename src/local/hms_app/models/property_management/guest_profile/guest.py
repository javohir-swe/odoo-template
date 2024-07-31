import re

from odoo import api, exceptions, fields, models

from ...data import CITIZENSHIP


class LegalRepresentative(models.Model):
    _name = "legal.representative"
    _description = "Legal Representative"

    last_name = fields.Char(string="Last name")
    first_name = fields.Char(string="First Name")
    middle_name = fields.Char(string="Middle name")
    sex = fields.Selection([("male", "Male"), ("female", "Female")], string="Sex")
    birthday = fields.Datetime(string="Date of birth")
    birthday_country = fields.Many2one("countries", string="Country of birth")
    birthday_city = fields.Char(string="City")
    citizenship = fields.Char(string="Citizenship")
    degree_of_kinship = fields.Char(string="Degree of kinship")
    passport = fields.Selection(
        [("id", "ID"), ("passport", "Passport")], string="Document"
    )
    series = fields.Char(string="Series")
    series_num = fields.Char(string="Serial number")
    date_of_issue = fields.Datetime(string="Date of issue")
    end_of_issue = fields.Datetime(string="Validity period")
    given_by = fields.Text(string="Given by whom")
    guest_id = fields.Many2one("guest", string="Guest")


class EmailContact(models.Model):
    _name = "email.contact"
    _description = "Email Contact"

    guest_id = fields.Many2one("guest", string="Guest")
    email = fields.Char(string="Email address")

    @api.constrains("email")
    def _check_email(self):
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        for record in self:
            if record.email and not re.match(email_regex, record.email):
                raise exceptions.ValidationError("Please enter a valid email address.")


class PhoneContact(models.Model):
    _name = "phone.contact"
    _description = "Phone Contact"

    guest_id = fields.Many2one("guest", string="Guest")
    phone = fields.Char(string="Phone number")

    @api.constrains("phone")
    def _check_phone(self):
        phone_regex = r"^\+?\d{7,15}$"
        for record in self:
            if record.phone and not re.match(phone_regex, record.phone):
                raise exceptions.ValidationError("Please enter a valid phone number.")


class Guest(models.Model):
    _name = "guest"
    _description = "Guest"
    _rec_name = "full_name"

    js_field = fields.Char(string="JS field")
    citizenship = fields.Char(string="Citizenship")

    citizenships = fields.Selection(CITIZENSHIP, string="Citizenship")
    last_name = fields.Char(string="Last name", required=True)
    first_name = fields.Char(string="First Name", required=True)
    middle_name = fields.Char(string="Middle name")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    email_ids = fields.One2many("email.contact", "guest_id", string="Emails")
    phone_ids = fields.One2many("phone.contact", "guest_id", string="Phones")
    sex = fields.Selection([("male", "Male"), ("female", "Female")], string="Sex")
    birthday = fields.Date(string="Date of birth")
    guest_company_id = fields.Many2one("company", string="Company")
    country_id = fields.Many2one("countries", string="Country")
    document = fields.Selection(
        [
            ("not_specified", "Not specified"),
            ("passport", "Passport"),
            ("other_identity_document", "Other identity document"),
        ],
        default="not_specified",
        string="Document",
    )
    # =============================== #
    invisable_passport = fields.Boolean(string="Invisable Passport", default=True)
    invisable_title = fields.Boolean(string="Invisable Title", default=True)
    document_title = fields.Char(string="Document Title")
    series = fields.Char(string="Series")
    number = fields.Char(string="No.")
    issue_date = fields.Date(string="Issue date")
    expiry_date = fields.Date(string="Expiry date")
    issuing_authority = fields.Text(string="Issuing authority")
    country_of_birth = fields.Selection(CITIZENSHIP, string="Country of birth")
    passport_city = fields.Char(string="City")
    document_copy = fields.Binary(string="Document copy")
    document_copy_filename = fields.Char(string="Document copy filename")
    # ================================== #
    birthday_country = fields.Many2one("countries", string="Country of birth")
    legal_representative_id = fields.One2many(
        "legal.representative",
        "guest_id",
        string="Information about the legal representative",
    )
    # ================================= #
    representative_last_name = fields.Char(string="Last name")
    representative_first_name = fields.Char(string="First Name")
    representative_middle_name = fields.Char(string="Middle name")
    representative_sex = fields.Selection(
        [("male", "Male"), ("female", "Female")], string="Gender"
    )
    representative_birthday = fields.Date(string="Date of birth")
    representative_birthday_country = fields.Selection(
        CITIZENSHIP, string="Country of birth"
    )
    representative_birthday_city = fields.Char(string="City of birth")
    representative_citizenship = fields.Selection(CITIZENSHIP, string="Citizenship")
    representative_relationship_to_cardholder = fields.Selection(
        [
            ("mother", "Mother"),
            ("father", "Father"),
            ("other_relationship", "Other relationship"),
            ("guardian", "Guardian"),
            ("caregiver", "Caregiver"),
        ],
        default="father",
        string="Relationship to cardholder",
    )
    representative_passport = fields.Selection(
        [
            ("not_specified", "Not specified"),
            ("passport", "Passport"),
            ("other_identity_document", "Other identity document"),
        ],
        defalt="not_specified",
        string="Document",
    )
    # =============================== #
    representative_invisable_passport = fields.Boolean(
        string="Invisable Passport", default=True
    )
    representative_invisable_title = fields.Boolean(
        string="Invisable Title", default=True
    )
    representative_document_title = fields.Char(string="Document Title")
    representative_series = fields.Char(string="Series")
    representative_number = fields.Char(string="No.")
    representative_issue_date = fields.Date(string="Issue date")
    representative_expiry_date = fields.Date(string="Expiry date")
    representative_issuing_authority = fields.Text(string="Issuing authority")
    # ================================== #
    # ================================= #
    guest_status = fields.Selection(
        [
            ("not_selected", "Not Selected"),
            ("vip", "VIP"),
            ("blacklist", "Blacklist"),
            ("regular_customer", "Regular Customer"),
            ("corporate_client", "Corporate Client"),
        ],
        default="not_selected",
        string="Guest Status",
    )
    comment_for_guest = fields.Text(string="Comments")
    countries = fields.Selection(CITIZENSHIP, string="Countries")
    zip_code = fields.Integer(string="Postal code")
    region = fields.Char(string="Region")
    district = fields.Char(string="District")
    city = fields.Char(string="City")
    location = fields.Char(string="Location")
    settlement = fields.Char(string="Accommodation")
    street = fields.Char(string="Street")
    home = fields.Char(string="House")
    building = fields.Char(string="Building")
    apartment = fields.Char(string="Apartment")
    # ====================================== #
    total_bookings = fields.Integer(
        string="Total Bookings", compute="_compute_total_bookings", store=True
    )
    total_amount = fields.Float(
        string="Total Amount", compute="_compute_total_bookings", store=True
    )
    booking_info = fields.Char(
        string="Booking Info", compute="_compute_booking_info", store=True
    )
    booking_ids = fields.Many2many("booking", string="Bookings")
    # ====================================== #
    full_name = fields.Char(
        string="Guest's full name", compute="_compute_full_name", store=True
    )
    # ====================================== #
    deposit = fields.Float(string="Deposit", compute="_compute_deposit", store=True)
    deposit_data = fields.One2many("deposit.data", "guest_id", string="Deposit Data")
    # ====================================== #

    @api.depends("deposit_data.amount", "deposit_data.action_type")
    def _compute_deposit(self):
        for guest in self:
            deposit_total = 0
            for data in guest.deposit_data:
                if data.action_type == "payment":
                    deposit_total += data.amount
                else:
                    deposit_total -= data.amount
            guest.deposit = deposit_total

    @api.depends("booking_ids")
    def _compute_total_bookings(self):
        for guest in self:
            guest.total_bookings = len(guest.booking_ids)
            guest.total_amount = sum(booking.total for booking in guest.booking_ids)

    @api.depends("total_bookings", "total_amount")
    def _compute_booking_info(self):
        for guest in self:
            guest.booking_info = f"Total bookings: {guest.total_bookings}. Total amount: {guest.total_amount} UZS."

    @api.depends("first_name", "last_name", "middle_name")
    def _compute_full_name(self):
        for guest in self:
            guest.full_name = f"{guest.first_name} {guest.last_name}"

    @api.onchange("document")
    def _onchange_document(self):
        print("passport")
        if self.document == "passport":
            self.invisable_passport = False
            self.invisable_title = True
        elif self.document == "other_identity_document":
            self.invisable_passport = False
            self.invisable_title = False
        else:
            self.invisable_passport = True
            self.invisable_title = True

    @api.onchange("representative_passport")
    def _onchange_representative_passport(self):
        print("representative")
        if self.representative_passport == "passport":
            self.representative_invisable_passport = False
            self.representative_invisable_title = True
        elif self.representative_passport == "other_identity_document":
            self.representative_invisable_passport = False
            self.representative_invisable_title = False
        else:
            self.representative_invisable_passport = True
            self.representative_invisable_title = True
