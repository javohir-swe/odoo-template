from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AdditionAccountNumber(models.Model):
    _name = "addition.account.number"
    _description = "Additional Account Number"

    currency = fields.Selection(
        [("uzs", "UZS"), ("usd", "USD")], string="Account currency"
    )
    name_legal_entity = fields.Char(string="Legal entity name for bank account number")
    legal_name = fields.Char(string="Legal Name")
    bank_name = fields.Text(string="Bank name")
    SWIFT = fields.Text(string="SWIFT Code")
    account = fields.Integer(string="Account number")
    correspondent_name = fields.Text(string="Correspondent bank name")
    correspondent_swift = fields.Char(string="Correspondent bank SWIFT")
    correspondent_account = fields.Char(string="Correspondent account number")
    company_id = fields.Many2one("company", string="Companies")


class ResponsiblePerson(models.Model):
    _name = "responsible.person"
    _description = "Responsible Person"

    last_name = fields.Char(string="Last name")
    first_name = fields.Char(string="First Name")
    middle_name = fields.Char(string="Middle name")
    phone = fields.Char(string="Phone number")
    email = fields.Char(string="Email address")
    company_id = fields.Many2one("company", string="Companies")


class Company(models.Model):
    _name = "company"
    _description = "Company"
    _rec_name = "company_name"

    status = fields.Boolean(string="Status", default=True)
    company_type = fields.Selection(
        [
            ("customer_company", "Customer Company"),
            ("agent_company", "Agent Company"),
        ],
        string="Company type",
    )
    commission = fields.Integer(string="Commission amount")
    comment = fields.Text(
        string="Comments",
        help="Character left: 512\nOnly location tool staff can see.",
    )

    channel_agent = fields.Char(string="Change to agent company for channel")

    country_id = fields.Many2one("countries", string="Mamlakat")
    country = fields.Selection(
        [
            ("uzbekistan", "Uzbekistan"),
        ],
        string="Country",
        default="uzbekistan",
    )
    company_name = fields.Char(string="Company name")
    company_phone = fields.Char(string="Company phone number")
    company_email = fields.Char(string="Company email address")
    fax = fields.Char(string="Company fax")
    address = fields.Char(string="Legal address")
    zip_address = fields.Char(string="Zip address")
    account_number = fields.Selection(
        [("uzs", "UZS"), ("usd", "USD")], string="Account currency"
    )
    addition_account_number_id = fields.One2many(
        "addition.account.number",
        "company_id",
        string="Additional currency account numbers",
    )
    responsible_person_id = fields.One2many(
        "responsible.person",
        "company_id",
        string="Contact information of responsible persons",
    )
    guest_company_id = fields.Many2one("guest", string="Guest")

    swift_code = fields.Char(string="STIR", compute="_compute_swift_code", store=True)

    full_name = fields.Char(
        string="Contact information of responsible persons",
        compute="_compute_full_name",
        store=True,
    )
    # bank account
    currency = fields.Selection(
        [("uzs", "UZS"), ("usd", "USD"), ("rub", "RUB")],
        default="uzs",
        string="Currency",
    )
    bank_details = fields.Text(string="Bank details")

    registered_address = fields.One2many(
        "register.address", "company_id", string="Registered address"
    )
    not_the_same_registered_address = fields.Boolean(
        string="Not the same as the registered address"
    )
    postal_address = fields.One2many(
        "postal.address", "company_id", string="Postal address"
    )
    company_staff = fields.One2many("guest", "guest_company_id", string="Guest")

    @api.depends("addition_account_number_id.SWIFT")
    def _compute_swift_code(self):
        for company in self:
            swift_codes = company.addition_account_number_id.mapped("SWIFT")
            company.swift_code = ", ".join(swift_codes)

    @api.depends("responsible_person_id.first_name", "responsible_person_id.last_name")
    def _compute_full_name(self):
        for company in self:
            full_names = []
            for person in company.responsible_person_id:
                full_names.append(f"{person.first_name} {person.last_name}")
            company.full_name = ", ".join(full_names)

    @api.constrains("registered_address", "postal_address")
    def _check_single_address(self):
        for record in self:
            if len(record.registered_address) > 1:
                raise ValidationError("You can only set one registered address.")
            if len(record.postal_address) > 1:
                raise ValidationError("You can only set one postal address.")


class RegisteredAddress(models.Model):
    _name = "register.address"
    _description = "Register Address"

    company_id = fields.Many2one("company", string="Company")
    postal_code = fields.Char(string="Postal code")
    country = fields.Selection(
        [
            ("uzbekistan", "Uzbekistan"),
        ],
        default="uzbekistan",
        string="Country",
    )
    region = fields.Char(string="Region")
    district = fields.Char(string="District")
    city = fields.Char(string="City")
    location = fields.Char(string="Location")
    street = fields.Char(string="Street")
    house = fields.Char(string="House")
    building = fields.Char(string="Building")
    block = fields.Char(string="Block")
    apartment = fields.Char(string="Apartment")


class PostalAddress(models.Model):
    _name = "postal.address"
    _description = "Postal Address"

    company_id = fields.Many2one("company", string="Company")
    postal_code = fields.Char(string="Postal code")
    country = fields.Selection(
        [
            ("uzbekistan", "Uzbekistan"),
        ],
        default="uzbekistan",
        string="Country",
    )
    region = fields.Char(string="Region")
    district = fields.Char(string="District")
    city = fields.Char(string="City")
    location = fields.Char(string="Location")
    street = fields.Char(string="Street")
    house = fields.Char(string="House")
    building = fields.Char(string="Building")
    block = fields.Char(string="Block")
    apartment = fields.Char(string="Apartment")
