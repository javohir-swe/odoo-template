import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PointOfSale(models.Model):
    _name = "point.of.sale"
    _description = "Point of Sale"

    name = fields.Char(string="Name", required=True)


# Delete
class CancellationRule(models.Model):
    _name = "cancel.rule"
    _description = "Cancellation rule"

    name = fields.Char(string="Name", required=True)


class Currency(models.Model):
    _name = "currency"
    _description = "Currency"
    _rec_name = "currency"

    currency = fields.Char(string="Currency", required=True)


class Types(models.Model):
    _name = "types"
    _description = "Type"

    name = fields.Char(string="Name", required=True)


# Delete
class Check(models.Model):
    _name = "checkinout"
    _description = "Check in check out"

    name = fields.Char(string="Name", required=True)


# Delete
class RoundingPolicy(models.Model):
    _name = "rounding.policy"
    _description = "Rounding policy"

    name = fields.Char(string="Name", required=True)


class RatePlan(models.Model):
    """General Settings and Display on the website"""

    _name = "rate.plan"
    _description = "Rate Plan"
    _rec_name = "rate_plan_name"

    rate_plan_name = fields.Char(string="Rate Plan Name", required=True)
    type_id = fields.Many2one("types", string="Type")
    currency_id = fields.Many2one("currency", string="Currency")
    room_types = fields.Many2many(
        "triple",  # Target model
        "rate_plan_triple_rel",  # Relation table
        "rate_plan_id",  # Column for "Rate Plan" model
        "triple_id",  # Column for "Triple" model
        string="Room Types",
        default=lambda self: self._default_room_types(),
        required=True,
    )
    # payment_methods_for_guests_id = fields.Many2many(
    #     "payment.methods.for.guests",  # Target model
    #     "rate_plan_paymentmethodsforguests_rel",  # Relation table
    #     "rate_plan_id",  # Column for "Rate Plan" model
    #     "paymentmethodsforguests_id",
    #     string="Payment Methods for Guests",
    # )
    # points_of_sale_ids = fields.Many2many("point.of.sale", string="Points of Sale")
    at_checkin = fields.Boolean(string="At Check-in")
    bank_card = fields.Boolean(string="Bank card guarantee")
    bank_for_individuals = fields.Boolean(
        string="Bank transfer for individuals (invoice issued by hotel) [100%] [no less than 3 days]"
    )
    bank_for_legal = fields.Boolean(
        string="Bank transfer for legal entities (invoice issued by hotel) [First nights: 1] [no less than 3 days]  "
    )
    channel_manager = fields.Boolean(string="Channel Manager")
    front_desk_booking = fields.Boolean(string="Front Desk Booking")
    mobile_extranet = fields.Boolean(string="Mobile Extranet")
    official_site = fields.Boolean(string="Official Site")

    cancellation_rule = fields.Many2one(
        "cancellation.terms", string="Cancellation Rule"
    )
    early_check_in_and_late_checkout_rule = fields.Many2one(
        "check.in.check.out.roles", string="Early Check-In and Late Check-Out Rule"
    )
    rounding_rule = fields.Many2one("rounding.rule", string="Rounding Rule")
    active_rate_plan = fields.Boolean(string="Active Rate Plan", default=True)
    detailed_description = fields.Text("Detailed description")
    thumbnail = fields.Image("Thumbnail")
    promo_picture_for_landing = fields.Image("Promo picture for landing")
    discount_motivator = fields.Boolean(
        string="Discount motivator (price crossing)", default=False
    )
    date_to_be_displayed_1 = fields.Date("Dates when the rate plan is shown to guests")
    date_to_be_displayed_2 = fields.Date()
    limited = fields.Boolean(string="Not limited", default=False)
    mon = fields.Boolean(default=False, string="Mon")
    tue = fields.Boolean(default=False, string="Tue")
    wed = fields.Boolean(default=False, string="Wed")
    thu = fields.Boolean(default=False, string="Thu")
    fri = fields.Boolean(default=False, string="Fri")
    sat = fields.Boolean(default=False, string="Sat")
    sun = fields.Boolean(default=False, string="Sun")
    price_details_by_days = fields.Boolean(
        default=False, string="Price details by days"
    )

    extras_type_ids = fields.One2many("rate_plan.extras", "extra_id", string="Extra")
    scheduler = fields.Char()
    # ============= Filter ============= #
    filter_minlos = fields.One2many(
        "rate_plan.min_los", "rate_plan_id", string="MinLOS"
    )
    filter_maxlos = fields.One2many(
        "rate_plan.max_los", "rate_plan_id", string="MaxLOS"
    )
    filter_minlosarrival = fields.One2many(
        "rate_plan.min_los_arrival", "rate_plan_id", string="MinLOSArrival"
    )
    filter_maxlosarrival = fields.One2many(
        "rate_plan.max_los_arrival", "rate_plan_id", string="MaxLOSArrival"
    )
    filter_fullparentlos = fields.One2many(
        "rate_plan.full_parent_los", "rate_plan_id", string="FullParentLOS"
    )
    filter_maxadvbooking = fields.One2many(
        "rate_plan.max_adv_booking", "rate_plan_id", string="MaxAdvBooking"
    )
    filter_minadvbooking = fields.One2many(
        "rate_plan.min_adv_booking", "rate_plan_id", string="MinAdvBooking"
    )
    filter_cta = fields.One2many("rate_plan.cta", "rate_plan_id", string="CTA")
    filter_ctd = fields.One2many(
        "rate_plan.rate_plan_ctd", "rate_plan_id", string="CTD"
    )
    filter_checkincheckout = fields.One2many(
        "rate_plan.check_in.check_out", "rate_plan_id", string="CheckIn CheckOut"
    )
    filter_paymentmethods = fields.One2many(
        "rate_plan.payment_methods", "rate_plan_id", string="PaymentMethods"
    )
    filter_closed = fields.One2many("rate_plan.closed", "close_id", string="Closed")
    filter_price = fields.One2many("rate_plan.price", "rate_plan_id", string="Price")
    filter_stay_controls = fields.One2many(
        "rate_plan.stay_controls", "rate_plan_id", string="StayControls"
    )
    # ===================== Filters ==========================
    booking_per_rate_plan = fields.Selection(
        [("no_promo_code", "No promo code"), ("with_promo_code", "With promo code")],
        default="no_promo_code",
    )
    promo_code_groups = fields.Many2many(
        "promo_code.groups", string="Groups of promo codes"
    )
    promo_code_ids = fields.Many2many(
        "property_settings.promo_code", string="promo codes"
    )
    display_promo_code = fields.Selection(
        [("hide", "Hide"), ("show", "Show")],
        default="hide",
        string="Display the rate plan before entering a promo code",
    )

    @api.onchange("limited")
    def _onchange_period_limit(self):
        if self.limited:
            self.date_to_be_displayed_2 = False

    @api.onchange("booking_per_rate_plan")
    def _onchange_booking_per_rate_plan(self):
        if self.booking_per_rate_plan == "no_promo_code":
            self.promo_code_groups = [(5, 0, 0)]  # Clear all entries
            self.promo_code_ids = [(5, 0, 0)]  # Clear all entries
            self.display_promo_code = "hide"  # Reset to default value

    def create(self, values):
        if (
            "booking_per_rate_plan" in values
            and values["booking_per_rate_plan"] == "no_promo_code"
        ):
            values.update(
                {
                    "promo_code_groups": [(5, 0, 0)],  # Clear all entries
                    "promo_code_ids": [(5, 0, 0)],  # Clear all entries
                    "display_promo_code": "hide",  # Reset to default value
                }
            )

        return super().create(values)

    def write(self, values):
        # If 'limited' is being set to True, clear 'period_of_stay_to'
        if "limited" in values and values["limited"]:
            values["date_to_be_displayed_2"] = False

        if (
            "booking_per_rate_plan" in values
            and values["booking_per_rate_plan"] == "no_promo_code"
        ):
            values.update(
                {
                    "promo_code_groups": [(5, 0, 0)],  # Clear all entries
                    "promo_code_ids": [(5, 0, 0)],  # Clear all entries
                    "display_promo_code": "hide",  # Reset to default value
                }
            )

        return super().write(values)

    @api.model
    def _default_room_types(self):
        # formga kirilganda barcha room types avtomatik tanlangan bo'ladi
        # Retrieves all triple records and returns their ids
        return self.env["triple"].search([]).ids

    @api.model
    def get_all_fields(self, rate_plan_id):
        record = self.browse(rate_plan_id)
        result = record.read()[0]

        result["room_types"] = []
        for room_type in record.room_types:
            room_type_data = room_type.read(["id", "rooms"])[0]
            room_type_data["child_aged_from"] = room_type.child_aged_from.read(
                ["id", "name"]
            )
            room_type_data["guest_ids"] = room_type.guest_ids.read(["id", "name"])
            result["room_types"].append(room_type_data)
        result["filter_closed"] = record.filter_closed.read(
            ["id", "relevant_date", "room_type_id", "status"]
        )
        result["filter_minlos"] = record.filter_minlos.read(
            ["id", "relevant_date", "room_type_id", "number"]
        )
        result["filter_stay_controls"] = record.filter_stay_controls.read(
            [
                "id",
                "rate_plan_id",
                "room_type_id",
                "guest_id",
                "child_age_range",
                "filter_id",
                "relevant_date",
                "status",
            ]
        )
        result["filter_price"] = record.filter_price.read(
            [
                "id",
                "rate_plan_id",
                "room_type_id",
                "guest_id",
                "child_age_range",
                "relevant_date",
                "price",
            ]
        )
        result["filter_minlos"] = record.filter_minlos.read(
            [
                "id",
                "rate_plan_id",
                "room_type_id",
                "filter_id",
                "relevant_date",
                "number",
                "reset",
            ]
        )
        result["filter_maxlos"] = record.filter_maxlos.read(
            [
                "id",
                "rate_plan_id",
                "room_type_id",
                "filter_id",
                "relevant_date",
                "number",
                "reset",
            ]
        )
        result["filter_minlosarrival"] = record.filter_minlosarrival.read(
            [
                "id",
                "rate_plan_id",
                "room_type_id",
                "filter_id",
                "relevant_date",
                "number",
                "reset",
            ]
        )
        result["filter_maxlosarrival"] = record.filter_maxlosarrival.read(
            [
                "id",
                "rate_plan_id",
                "room_type_id",
                "filter_id",
                "relevant_date",
                "number",
                "reset",
            ]
        )
        result["filter_fullparentlos"] = []
        for parent_los in record.filter_fullparentlos:
            parent_los_data = parent_los.read(
                ["id", "rate_plan_id", "room_type_id", "filter_id", "relevant_date"]
            )[0]
            parent_los_data["long_of_stay"] = parent_los.long_of_stay.read(
                ["id", "name"]
            )
            result["filter_fullparentlos"].append(parent_los_data)

        result["filter_checkincheckout"] = []
        for parent_los in record.filter_checkincheckout:
            parent_los_data = parent_los.read(
                ["id", "rate_plan_id", "filter_id", "relevant_date", "checkin_checkout"]
            )[0]
            parent_los_data["checkin_checkout"] = parent_los.checkin_checkout.read(
                ["id", "name"]
            )
            result["filter_checkincheckout"].append(parent_los_data)

        result["filter_paymentmethods"] = []
        for payment_method in record.filter_paymentmethods:
            payment_method_data = payment_method.read(
                ["id", "rate_plan_id", "room_type_id", "filter_id", "relevant_date"]
            )[0]
            payment_method_data[
                "payment_methods"
            ] = payment_method.payment_methods.read(["id", "name"])
            result["filter_paymentmethods"].append(payment_method_data)

        result["filter_maxadvbooking"] = record.filter_maxadvbooking.read(
            [
                "id",
                "rate_plan_id",
                "room_type_id",
                "filter_id",
                "relevant_date",
                "number",
                "reset",
            ]
        )
        result["filter_minadvbooking"] = record.filter_minadvbooking.read(
            [
                "id",
                "rate_plan_id",
                "room_type_id",
                "filter_id",
                "relevant_date",
                "number",
                "reset",
            ]
        )
        result["filter_cta"] = record.filter_cta.read(
            [
                "id",
                "rate_plan_id",
                "room_type_id",
                "filter_id",
                "relevant_date",
                "status",
            ]
        )
        result["filter_ctd"] = record.filter_ctd.read(
            [
                "id",
                "rate_plan_id",
                "room_type_id",
                "filter_id",
                "relevant_date",
                "status",
            ]
        )
        return result
