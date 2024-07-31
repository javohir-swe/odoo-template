from odoo import api, fields, models
from odoo.exceptions import ValidationError


class GroupServices(models.Model):
    _name = "group.services"
    _description = "Services Group"

    name = fields.Char(string="Name", required=True)
    service = fields.One2many(
        "services.settings", "group_of_services", string="Service"
    )
    description = fields.Text(string="Description")
    service_count = fields.Integer(
        string="Service Count", compute="_compute_service_count"
    )

    @api.depends("service")
    def _compute_service_count(self):
        for record in self:
            record.service_count = len(record.service)


class ServicePhoto(models.Model):
    _name = "service.photo"
    _description = "Service Photos"

    service_id = fields.Many2one(
        "services.settings", string="Service", ondelete="cascade"
    )
    photo = fields.Binary(string="Photo", required=True)


class MotivatorInExelyBookingEngine(models.Model):
    _name = "motivator.booking.engine"
    _description = "Motivator in Exely Booking Engine"

    name = fields.Char(string="Name")
    icon = fields.Binary(string="Icon")  # Using Binary field for images


# RatePlan ulassh kerak
class ServicesTypes(models.Model):
    _name = "services.types"
    _description = "Service Types"

    name = fields.Char(string="Name")


class Services(models.Model):
    _name = "services.settings"
    _description = "Services"
    _rec_name = "service_name"

    status = fields.Boolean(string="Status", default=True)
    service_type = fields.Selection(
        [("general", "General"), ("meal", "Meal")],
        string="Type",
        required=True,
        default="general",
    )
    service_name = fields.Selection(
        [
            ("breakfast", "Breakfast"),
            ("buffet_breakfast", "Buffet breakfast"),
            ("continental_breakfast", "Continental breakfast"),
            ("english_breakfast", "English breakfast"),
            ("american_breakfast", "American breakfast"),
            ("lunch", "Lunch"),
            ("dinner", "Dinner"),
            ("buffet_dinner", "Buffet dinner"),
            ("dinner_a_la_carte", "Dinner à la carte"),
            ("breakfast_and_lunch", "Breakfast & lunch"),
            ("breakfast_and_dinner", "Breakfast & dinner"),
            ("lunch_and_dinner", "Lunch & dinner"),
            ("full_board", "Full board"),
            ("full_board_buffet", "Full board buffet"),
            ("full_board_a_la_carte", "Full board à la carte"),
            ("all_inclusive", "All inclusive"),
            ("ultra_all_inclusive", "Ultra all inclusive"),
            ("other", "Other"),
        ],
        string="Name",
        default="breakfast",
        required=True,
    )
    invisible_name = fields.Boolean(compute="_compute_invisible_name")
    name = fields.Char(string="Name")
    service_charge_type = fields.Selection(
        [("per_guest_per_night", "Per guest per night")],
        string="Charge Type",
        default="per_guest_per_night",
        readonly=True,
    )

    title_price = fields.Char(string="Price", compute="_compute_title_price")
    service_price_usd = fields.Float(string="Price USD")
    service_price_uzs = fields.Float(string="Price UZS")
    service_price_rub = fields.Float(string="Price RUB")
    service_exely_booking_engin = fields.Boolean(
        string="Movo Booking Engine", default=True
    )
    service_front_desk = fields.Boolean(string="Movo PMS", default=True)
    dissplay_website_description = fields.Text(
        string="Description", default="from 07:00 to 10:00"
    )
    dissplay_website_name = fields.Text(string="dissplay_website_name")
    dissplay_website_photos = fields.One2many(
        "service.photo", "service_id", string="Photos"
    )
    service_motivator = fields.Selection(
        [
            ("no_motivator", "no motivator"),
            ("sale", "Sale"),
            ("bestseller", "Bestseller"),
            ("book_now", "Book now!"),
            ("families_with_children", "Families with children"),
            ("friends", "Friends"),
        ],
        default="no_motivator",
        string="Motivator in Exely Booking Engine",
    )

    point_of_sale = fields.Many2one("point.of.sale", string="Point of Sale")
    group_of_services = fields.Many2one("group.services", string="Group of Services")
    # Not need
    motivator_in_exely_booking_engine = fields.Many2one(
        "motivator.booking.engine", string="Motivator in Booking Engine"
    )
    sale_title = fields.Char(string="Sale Title", compute="_compute_sale_title")

    @api.depends("service_exely_booking_engin", "service_front_desk")
    def _compute_sale_title(self):
        for record in self:
            titles = []
            if record.service_exely_booking_engin:
                titles.append("(Exely Booking Engine)")
            if record.service_front_desk:
                titles.append("(Exely PMS)")
            record.sale_title = " & ".join(titles)

    @api.depends("service_price_usd", "service_price_uzs", "service_price_rub")
    def _compute_title_price(self):
        for record in self:
            prices = []
            if record.service_price_usd:
                prices.append(f"USD {record.service_price_usd:.2f}")
            if record.service_price_uzs:
                prices.append(f"UZS {record.service_price_uzs:.2f}")
            if record.service_price_rub:
                prices.append(f"RUB {record.service_price_rub:.2f}")
            record.title_price = " | ".join(prices)

    @api.constrains("service_exely_booking_engin", "service_front_desk")
    def _check_service_fields(self):
        for record in self:
            if not record.service_exely_booking_engin and not record.service_front_desk:
                raise ValidationError("Select at least one point of sale")

    @api.depends("service_name")
    def _compute_invisible_name(self):
        for record in self:
            record.invisible_name = record.service_name != "other"

    # type = fields.Many2one("services.types", string="Service Type")
    # name = fields.Char(string="Name")
    # charge_type = fields.Char(string="Charge Type")
    # price_usd = fields.Char(string="Price USD")
    # price_uzs = fields.Char(string="Price UZS")
    # price_rub = fields.Char(string="Price RUB")
    # description = fields.Text(string="Description")


#     photos = fields.Binary(string="Photos")  # Using Binary field for images
