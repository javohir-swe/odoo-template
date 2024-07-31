from odoo import api, fields, models

from ..data import ALL_TIMES


class Settings(models.Model):
    _name = "settings"
    _description = "Custom Settings"
    _rec_name = "name"

    name = fields.Char(default="Settings", required=True)
    housekeeping = fields.Boolean(
        default=False, help="Check-in only in rooms with status 'Cleaned' and 'Checked'"
    )
    guest_profiles = fields.Boolean(
        string="Guest Profiles",
        help="Automatically find the guest profiles with similar parameters for bookings from the website and the distribution channels",
    )
    auto_create = fields.Boolean(
        string="Auto Create",
        help="Automatically create standard invoice for bookings for several rooms",
    )
    paid_services = fields.Boolean(
        string="Paid Services",
        help="Do not show paid services included in the price in a separate line in the invoice",
    )
    accommodation = fields.Boolean(
        string="Accommodation", help="List the names of all guests in the invoice"
    )
    seal = fields.Binary(
        string="Seal",
        help="Max file size is 2 MB. Supported file formats are GIF, PNG and JPEG. Print image will automatically be changed to 250x250 pixels.",
    )
    administrator = fields.Boolean(
        string="Administrator",
        help="In the references tab 'Staff' the required fields Job title and Full name of the administrator fargonaazot@gmail.com are left empty",
    )
    fullname = fields.Char(string="Full Name")
    fullname_inlatin = fields.Char(
        string="Full Name in Latin", help="In Latin Characters"
    )
    job_title = fields.Char(string="Job Title")
    jobtitle_inlatin = fields.Char(
        string="Job Title in Latin", help="In Latin Characters"
    )
    signature = fields.Binary(
        string="Signature",
        help="Max file size is 2 MB. Supported image formats are GIF, PNG and JPEG. Signature image size will be automatically reduced to 250x250 points, with proportions preserved.",
    )
    show_accountant = fields.Boolean(
        string="Show Accountant",
        help="Show accountant signature on the invoice template",
    )
    new_booking = fields.Boolean(string="New Booking", help="New booking")
    booking_modifi = fields.Boolean(
        string="Booking Modification", help="Booking modification"
    )
    booking_cancel = fields.Boolean(
        string="Booking Cancellation", help="Booking cancellation"
    )
    enable_split = fields.Boolean(
        string="Enable Split",
        help="Split the Full board, Half board, and All-Inclusive meal service into breakfast, lunch, and dinner. Specify the rules for the meal report.",
    )
    checkin_time = fields.Float(
        string="Check-in Time",
        help="If check-in is early (or at the selected time), the report includes lunch and dinner; if check-in is late, only dinner is included",
    )
    checkout_time = fields.Float(
        string="Check-out Time",
        help="If check-out is early, the report includes breakfast only; if check-out is late (or at the selected time) - breakfast and lunch included",
    )
    checkin_times = fields.Selection(
        ALL_TIMES,
        default="16:00",
        string="Check-in Time",
        help="If check-in is early (or at the selected time), the report includes lunch and dinner; if check-in is late, only dinner is included",
    )
    checkout_times = fields.Selection(
        ALL_TIMES,
        default="12:00",
        string="Check-out Time",
        help="If check-out is early, the report includes breakfast only; if check-out is late (or at the selected time) - breakfast and lunch included",
    )

    references_ids = fields.One2many("references", "settings_id", "References")

    settings_pointofsale_id = fields.One2many(
        "settings.pointofsale", "settings_id", string="Point of Sale"
    )
    purpose_ofvisit_id = fields.One2many(
        "purpose.ofvisit", "settings_id", string="Purpose of Visit"
    )
    tag_id = fields.One2many("tag", "settings_id", string="Tag")
    payment_method_id = fields.One2many(
        "payment.method", "settings_id", string="Payment Method"
    )
    market_segment_id = fields.One2many(
        "market.segment", "settings_id", string="Market Segment"
    )
    staff_id = fields.One2many("staff", "settings_id", string="Staff")
    guest_status_id = fields.One2many(
        "guest.status", "settings_id", string="Guest Status"
    )
    new_template_id = fields.One2many(
        "new.template", "settings_id", string="New Template"
    )

    @api.model
    def create(self, vals):
        record = self.search([], limit=1)
        if record:
            record.write(vals)
            return record
        return super().create(vals)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        record = self.search([], limit=1)
        if record:
            res.update(
                {
                    "housekeeping": record.housekeeping,
                    "guest_profiles": record.guest_profiles,
                    "auto_create": record.auto_create,
                    "paid_services": record.paid_services,
                    "accommodation": record.accommodation,
                    "seal": record.seal,
                    "administrator": record.administrator,
                    "fullname": record.fullname,
                    "fullname_inlatin": record.fullname_inlatin,
                    "job_title": record.job_title,
                    "jobtitle_inlatin": record.jobtitle_inlatin,
                    "signature": record.signature,
                    "show_accountant": record.show_accountant,
                    "new_booking": record.new_booking,
                    "booking_modifi": record.booking_modifi,
                    "booking_cancel": record.booking_cancel,
                    "enable_split": record.enable_split,
                    "checkin_time": record.checkin_time,
                    "checkout_time": record.checkout_time,
                }
            )
        return res
