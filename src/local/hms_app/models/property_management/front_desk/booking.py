import logging
import uuid
from datetime import date, datetime, timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError

from ...data import ALL_TIMES, CITIZENSHIP, LANGUAGES

_logger = logging.getLogger(__name__)


class Accommodation(models.Model):
    _name = "accommodation"
    _description = "Accommodation"

    name = fields.Char("Name", compute="_compute_name", readonly=True, store=True)
    check_in_date = fields.Date(string="Check-in Date")
    check_out_date = fields.Date(string="Check-out Date")
    rate_plan = fields.Many2one("rate.plan", string="Rate Plan")
    room_type = fields.Many2one("triple", string="Room Type")
    adults = fields.Integer(string="Adults", store=True)
    price = fields.Float(string="Price", compute="_compute_price", store=True)
    vacant = fields.Integer(string="Vacant", compute="_compute_vacant", store=True)
    booking_unique = fields.Char("Booking")

    @api.model
    def get_accommodation_data(self):
        accommodations = self.search([])

        def format_accommodation_data(accommodation):
            return {
                "name": accommodation.name,
                "check_in_date": accommodation.check_in_date,
                "check_out_date": accommodation.check_out_date,
                "rate_plan": accommodation.rate_plan.rate_plan_name,
                "room_type": accommodation.room_type.rooms
                if accommodation.room_type
                else "",
                "adults": accommodation.adults,
                "price": accommodation.price,
                "vacant": accommodation.vacant,
                "booking_unique": accommodation.booking_unique,
            }

        data = [
            format_accommodation_data(accommodation) for accommodation in accommodations
        ]

        return data

    @api.depends("room_type", "adults", "price", "vacant")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.room_type.rooms} ({record.adults} adult(s))(UZS {record.price}) - ({record.vacant} vacant)"

    @api.depends("check_in_date", "room_type")
    def _compute_vacant(self):
        for record in self:
            if record.check_in_date and record.room_type:
                main_availability_records = self.env["main.availability"].search(
                    [
                        ("date", "=", record.check_in_date),
                        ("room_type", "=", record.room_type.id),
                    ]
                )
                if main_availability_records:
                    min_front_desk_availability = min(
                        avail.front_desk for avail in main_availability_records
                    )
                    record.vacant = min_front_desk_availability
                else:
                    record.vacant = 0
            else:
                record.vacant = 0

    @api.depends("check_in_date", "check_out_date", "room_type", "adults", "rate_plan")
    def _compute_price(self):
        for record in self:
            if (
                record.check_in_date
                and record.check_out_date
                and record.room_type
                and record.adults
                and record.rate_plan
            ):
                price_records = self.env["rate_plan.price"].search(
                    [
                        ("relevant_date", ">=", record.check_in_date),
                        ("relevant_date", "<=", record.check_out_date),
                        ("room_type_id", "=", record.room_type.id),
                        ("guest_id.guest_number", "=", record.adults),
                        ("rate_plan_id", "=", record.rate_plan.id),
                    ],
                    order="relevant_date desc",
                    limit=1,
                )
                if price_records:
                    record.price = price_records.price
                else:
                    record.price = 0
            else:
                record.price = 0

    @api.model
    def create(self, vals):
        record = super().create(vals)
        return record

    def write(self, vals):
        result = super().write(vals)
        return result


class Booking(models.Model):
    _name = "booking"
    _description = "Booking"

    name = fields.Char(string="Name", compute="_compute_name")
    js_field = fields.Char(string="JS")
    check_in_date = fields.Date(
        string="Check-in Date", required=True, default=fields.Date.today
    )
    check_out_date = fields.Date(
        string="Check-out Date",
        required=True,
        default=lambda self: fields.Date.today() + timedelta(days=1),
    )
    nights = fields.Integer(compute="_compute_nights", store=True, string="Nights")
    adults = fields.Selection(
        [(str(i), str(i)) for i in range(11)], string="Adults", default="1"
    )
    children = fields.Selection(
        [(str(i), str(i)) for i in range(11)], string="Children", default="0"
    )
    customer_company_id = fields.Many2one("company", string="Customer Company")
    agent_company_id = fields.Many2one("company", string="Agent Company")
    rate_plan = fields.Many2one(
        "rate.plan", string="Rate Plan", domain=[("front_desk_booking", "=", True)]
    )
    room_type_id = fields.Many2one("triple", string="Room Type")
    accommodation = fields.Many2one("accommodation", string="Accommodation")
    # room_number to'g'ri ishlashi uchun accommodation tanlanganidan keyin update qilish kerak.
    room_number = fields.Many2one("room.inventory", string="Room Number")
    available_room_ids = fields.Many2many(
        "room.inventory", compute="_compute_available_rooms", string="Available Rooms"
    )
    dont_move = fields.Boolean(string="Do not allow room move")
    check_in_time = fields.Many2one("check.in.check.out.time", string="Check In Time")
    checkout_time = fields.Many2one("check.in.check.out.time", string="Check Out Time")

    check_in_times = fields.Selection(
        ALL_TIMES,
        string="Check-in Times",
        default=lambda self: self._get_default_check_in_time(),
    )
    check_in_price = fields.Float(string="Check-in Price")

    check_out_times = fields.Selection(
        ALL_TIMES,
        string="Check-out Times",
        default=lambda self: self._get_default_check_out_time(),
    )
    check_out_price = fields.Float(string="Check-out Price")

    price_detail_ids = fields.One2many(
        "booking.price.detail", "booking_id", string="Price Details"
    )
    # Not need
    room_service_id = fields.One2many(
        "room.service", "booking_id", string="Room Service"
    )
    room_service_ids = fields.Many2many("rate_plan.extras", string="Room Service")
    total_services = fields.Char("Total Services", compute="_compute_total_services")
    total_services_front_desk = fields.Char(
        string="Total Services", compute="_compute_total_services"
    )
    guest_id = fields.Many2one("guest", string="Guest")
    first_name = fields.Char(
        related="guest_id.first_name", string="First Name", readonly=False
    )
    last_name = fields.Char(
        related="guest_id.last_name", string="Last Name", readonly=False
    )
    middle_name = fields.Char(
        related="guest_id.middle_name", string="Middle Name", readonly=False
    )
    email = fields.Char(related="guest_id.email", string="Email", readonly=False)
    phone = fields.Char(related="guest_id.phone", string="Phone", readonly=False)
    gender = fields.Selection(related="guest_id.sex", string="Gender", readonly=False)
    send_email = fields.Boolean(string="Send email notifications", readonly=False)
    # Selection field for countries
    citizenship = fields.Selection(CITIZENSHIP, string="Citizenship")

    # citizenship = fields.Selection([
    #     ('key', 'value')
    # ], string='Citizenship')

    deposit = fields.Float(string="Deposit")
    guarantee_method = fields.Selection(
        [
            ("external_payment", "External payment system"),
            ("bank_transfer_individuals", "Bank transfer for individuals"),
            ("bank_transfer_legal", "Bank transfer for legal entities"),
            ("cash_cashbox", "Cash via cashbox"),
            ("cash_terminal", "Cash via terminal"),
            ("deposit", "Deposit"),
        ],
        string="Guarantee Method",
    )

    service_and_accommodation = fields.Float(string="Service and Accommodation")
    total = fields.Float(string="Total")
    payment_due = fields.Float(string="Payment Due")
    is_paid = fields.Boolean("Paid", default=False)
    amount_paid = fields.Float("Amount Paid")
    must_pay = fields.Float("Must Pay", compute="_compute_must_pay")
    reception_id = fields.Many2one("reception", string="Reception")
    residual = fields.Float(string="Residual")

    @api.depends("total", "amount_paid")
    def _compute_must_pay(self):
        for record in self:
            if record.amount_paid >= record.total:
                record.must_pay = 0.0
                record.residual = record.amount_paid - record.total
            else:
                record.must_pay = record.total - record.amount_paid
                record.residual = 0.0

    unique_id = fields.Char(
        string="Unique ID",
        readonly=True,
        copy=False,
        default=lambda self: self._generate_unique_uuid(),
    )
    regenerate_accommodations = fields.Boolean(default=False)
    group_unique_id = fields.Char("group_unique_id")
    total_summary = fields.Text("Booking Summary", compute="_compute_booking_summary")
    price_detail_total = fields.Float(
        "Total Price Detail", compute="_compute_total_price_detail"
    )
    average_daily_rate = fields.Float(
        "Average Daily Rate", compute="_compute_average_daily_rate"
    )
    cost_of_stay = fields.Float("Cost of Stay", compute="_compute_cost_of_stay")
    point_of_sale = fields.Many2one("settings.pointofsale")
    purpose_of_visit = fields.Many2one("purpose.ofvisit")
    tag = fields.Many2one("tag")
    payment_method = fields.Many2one("payment.method")
    new_payment_method = fields.Many2one(
        "payment.methods.for.guests", string="Payment Method"
    )
    market_segment = fields.Many2one("market.segment")
    staff = fields.Many2one("staff")
    guest_status = fields.Many2one("guest.status")

    customer_language = fields.Selection(LANGUAGES)
    guest_comment = fields.Text("Guest comment")

    status = fields.Selection(
        [
            ("created", "Created"),
            ("cancel", "Cancel"),
            ("done", "Done"),
        ],
        string="status",
        default="created",
    )

    # for reception
    arrival_status = fields.Selection(
        [
            ("arrival", "Arrival"),
            ("waiting", "Waiting"),
            ("same_day_bookings", "Same-day bookings"),
            ("overdue", "Overdue"),
        ],
        string="Arrival Status",
        default="same_day_bookings",
        # compute="_compute_arrival_status",
    )

    departure_status = fields.Selection(
        [("waiting", "Waiting"), ("checked_out", "Checked Out")],
        default="waiting",
        string="Departure Status",
    )

    # for reception form
    date_of_stay_and_guests = fields.Char(
        "Date of Stay and number and Guests", compute="_compute_date_of_stay_and_guests"
    )
    tags = fields.Selection(
        [
            ("not_selected", "Not Selected"),
            ("promo_event", "Promo event"),
            ("business_forum", "Business forum"),
        ],
        default="not_selected",
        String="Tags",
    )

    change_history_ids = fields.One2many(
        "booking.change.history", "booking_id", string="Change History"
    )
    is_check_in = fields.Boolean("Is In Check-In", default=False)
    is_check_out = fields.Boolean("Is In Check-Out", default=False)
    is_market_segment = fields.Selection(
        [
            ("individual", "Individual"),
            ("corporate_individual", "Corporate individual"),
            ("corporate_group", "Corporate group"),
            ("travel_agency_individual", "Travel agency individual"),
            ("travel_agency_group", "Travel agency group"),
            ("online", "Online"),
            ("free_of_charge", "Free of charge"),
            ("service", "Service"),
        ],
        string="Market Segment",
    )

    is_front_desk_booking = fields.Selection(
        [
            ("front_desk", "Front Desk"),
            ("booking_engine", "Booking Engine"),
            ("via_phone", "via phone"),
            ("via_distribution_channel", "via distribution channel"),
            ("website", "Website"),
            ("fax", "Fax"),
            ("email", "Email"),
            ("mobile_version_of_site", "Mobile version of site"),
            ("facebook", "Facebook"),
            ("tripadvisor", "TripAdvisor"),
            ("extranet_booking", "Extranet booking"),
            ("mobile_extranet", "Mobile extranet"),
        ],
        string="Point of Sale",
    )

    is_purpose_of_visit = fields.Selection(
        [
            ("service", "Service"),
            ("business", "Business"),
            ("tourism", "Tourism"),
            ("education", "Education"),
            ("medical_care", "Medical care"),
            ("work", "Work"),
            ("private", "Private"),
            ("transit", "Transit"),
            ("humanitarian", "Humanitarian"),
            ("other", "Other"),
        ],
        string="Purpose of Visit",
    )

    booking_status = fields.Selection(
        [
            ("do_not_come", "Do not come"),
            ("new_booking", "New Booking"),
            ("checked_in", "Checked In"),
            ("moved", "Moved"),
            ("departured", "Departured"),
            ("booking_from_channels", "Booking from Channels"),
            ("book_without_room", "Book without room"),
            ("group_booking", "Group Booking"),
        ],
        compute="_compute_booking_status",
        store=True,
    )

    # group_booking_status = fields.Selection(
    #     [
    #         ("group_do_not_come", "Do not come"),
    #         ("group_new_booking", "New Booking"),
    #         ("group_checked_in", "Checked In"),
    #         ("group_moved", "Moved"),
    #         ("group_departured", "Departured"),
    #         ("group_booking_from_channels", "Booking from Channels"),
    #         ("group_book_without_room", "Book without room"),
    #         ("group_booking", "Group Booking"),
    #     ],
    #     store=True,
    # )

    arrival_date = fields.Date(string="Arrival Date")
    arrival_time = fields.Float(string="Arrival Time")

    # color_status = fields.Selection([
    #     ("late_color", "Late Color"),
    #     ("new_booking_color", "New Booking Color"),
    #     ("checked_in_color", "Checked In Color"),
    #     ("moved_color", "Moved Color"),
    #     ("departured_color", "Departured Color"),
    #     ("booking_from_channels_color", "Booking_from Channels Color"),
    #     ("book_without_room_color", ""),
    #     ("", ""),
    # ])

    booking_condition = fields.Selection(
        [
            ("new_booking", "New Booking"),
            ("without_room", "Without Room"),
            ("checked_in", "Checked In"),
            ("checked_out", "Checked Out"),
            ("did_not_go", "Did Not Go"),
            ("checkout_expired", "Checkout Expired"),
            ("late", "late"),
        ],
        default="new_booking",
        string="Booking Condition",
        compute="_compute_booking_condition",
    )

    is_moved_room = fields.Boolean("Moved Room", default=False)
    is_group_booking = fields.Boolean(
        "Group Booking", default=False, compute="_compute_is_group_booking"
    )

    """
    checkin qilsa bo'ladimi yoki yo'qmi shuni tekshiradigan field (nomi hazil uchun nomlangan)
    C-SPACE Coworking 23.07.2024 22:10 'uchqun_swe'
    """
    checkinable = fields.Boolean(
        "Checkinable", default=False, compute="_compute_checkinable"
    )

    @api.depends("check_in_times", "check_out_times", "room_number")
    def _compute_checkinable(self):
        for record in self:
            # Default value for checkinable
            record.checkinable = False

            if (
                not record.room_number
                or not record.check_in_times
                or not record.check_out_times
                or not record.id
            ):
                continue

            # Get all bookings for the same room number
            domain = [
                ("room_number", "=", record.room_number.id),
                ("id", "!=", record.id),  # Exclude the current booking
                ("check_out_date", ">=", fields.Date.today()),
                # Consider only future bookings or those not checked out yet
            ]
            other_bookings = self.search(domain)

            checkinable = True
            for other_booking in other_bookings:
                if not other_booking.is_check_out:
                    if other_booking.check_out_date > record.check_in_date or (
                        other_booking.check_out_date == record.check_in_date
                        and other_booking.check_out_times > record.check_in_times
                    ):
                        checkinable = False
                        break

            record.checkinable = checkinable

    @api.depends(
        "status",
        "is_paid",
        "room_number",
        "is_check_in",
        "is_check_out",
        "is_moved_room",
        "check_in_times",
        "check_out_times",
    )
    def _compute_booking_condition(self):
        for record in self:
            try:
                if record.status == "done" and not record.room_number:
                    record.booking_condition = "without_room"
                else:
                    record.booking_condition = "new_booking"

                if (
                    record.status == "done"
                    and record.is_check_in
                    and record.check_out_date > date.today()
                ):
                    record.booking_condition = "checked_in"
                elif record.status == "done" and not record.room_number:
                    record.booking_condition = "without_room"
                elif record.status == "done" and record.room_number:
                    record.booking_condition = "new_booking"

                if record.is_check_in and record.is_check_out:
                    if record.room_number:
                        if record.is_paid:
                            record.booking_condition = "checked_out"
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

                if (
                    record.check_out_date <= date.today()
                    and not record.is_check_out
                    and not record.is_check_in
                ):
                    record.booking_condition = "checkout_expired"
                elif (
                    record.check_out_date <= date.today()
                    and record.is_check_in
                    and not record.is_check_out
                ):
                    record.booking_condition = "did_not_go"
                elif record.check_in_date <= date.today() and not record.is_check_in:
                    record.booking_condition = "late"

                if not record.room_number:
                    record.booking_condition = "without_room"

            except Exception:
                raise ValueError(
                    f"Compute method failed to assign booking_condition for booking {record.id}"
                )

    # @api.depends(
    #     "check_in_times",
    #     "check_out_times",
    #     "is_check_in",
    #     "is_check_out",
    #     "is_moved_room",
    # )
    # def _compute_booking_condition(self):
    #     current_time = datetime.now().strftime("%H:%M")
    #     current_date = fields.Date.today()
    #     for record in self:
    #         if record.check_in_date and record.check_in_times:
    #             check_in_time = record.check_in_times
    #             if (
    #                 record.check_in_date <= current_date
    #                 and check_in_time < current_time
    #                 and not record.is_check_in
    #                 and record.check_out_date >= current_date
    #             ):
    #                 record.booking_condition = "late"
    #                 continue
    #
    #         if record.check_out_date and record.check_out_times:
    #             check_out_time = record.check_out_times
    #             if (
    #                 record.check_out_date <= current_date
    #                 and check_out_time < current_time
    #                 and not record.is_check_out
    #                 and record.is_check_in
    #             ):
    #                 record.booking_condition = "did_not_go"
    #                 continue
    #
    #         if record.check_in_times and record.check_out_times:
    #             if (
    #                 record.check_out_date <= current_date
    #                 and record.check_out_times < current_time
    #             ):
    #                 record.booking_condition = "checkout_expired"
    #                 continue
    #
    #         if not record.room_number:
    #             record.booking_condition = "without_room"
    #         else:
    #             record.booking_condition = "new_booking"
    #
    #         if record.is_check_in and not record.is_check_out:
    #             record.booking_condition = "checked_in"
    #         else:
    #             record.booking_condition = "new_booking"
    #
    #         if record.is_check_out and record.is_check_in:
    #             record.booking_condition = "checked_out"
    #         else:
    #             pass

    # Default value if none of the conditions are met
    # record.booking_condition = "late"

    @api.model
    def _get_default_check_in_time(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("property_settings.check_in_times", default="14:00")
        )

    @api.model
    def _get_default_check_out_time(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("property_settings.check_out_times", default="12:00")
        )

    @api.depends("group_unique_id")
    def _compute_is_group_booking(self):
        for record in self:
            if record.group_unique_id:
                record.is_group_booking = True

    # Need to delete
    @api.depends(
        "check_in_date",
        "check_out_date",
        "check_in_time",
        "checkout_time",
        "is_check_in",
        "is_check_out",
        "arrival_status",
        "is_moved_room",
        "departure_status",
        "group_unique_id",
    )
    def _compute_booking_status(self):
        current_date = fields.Date.today()
        for record in self:
            if (
                record.check_in_date <= current_date <= record.check_out_date
                and not record.is_moved_room
            ):
                if (
                    not record.is_check_in
                    and not record.is_check_out
                    and not record.group_unique_id
                ):
                    record.booking_status = "do_not_come"

            elif (
                record.is_check_in
                and record.arrival_status == "arrival"
                and not record.is_moved_room
            ):
                record.booking_status = "checked_in"

            elif record.is_moved_room:
                record.booking_status = "moved"

            elif (
                record.is_check_out
                and record.departure_status == "checked_out"
                and not record.is_moved_room
            ):
                record.booking_status = "departured"

            elif record.group_unique_id and not record.is_moved_room:
                record.booking_status = "group_booking"

            else:
                record.booking_status = "new_booking"

    @api.onchange("rate_plan", "room_type_id")
    def _onchange_rate_plan_room_type(self):
        if self.rate_plan and self.room_type_id:
            extras = self.env["rate_plan.extras"].search(
                [
                    ("extra_id", "=", self.rate_plan.id),
                    ("room_types", "=", self.room_type_id.id),
                    ("included_or_extra", "=", "included_in_the_rate_plan"),
                ]
            )
            self.room_service_ids = [(6, 0, extras.ids)]

    @api.model
    def _get_country_selection(self):
        countries = self.env["res.country"].search([])
        return [(country.code, country.name) for country in countries]

    @api.depends("check_in_date", "check_out_date", "nights", "adults", "children")
    def _compute_date_of_stay_and_guests(self):
        for record in self:
            record.date_of_stay_and_guests = f"{self.check_in_date}-{self.check_out_date} (nights {self.nights}) adults:{self.adults} children:{self.children}"

    @api.depends("room_service_ids")
    def _compute_total_services(self):
        for record in self:
            total_services = len(record.room_service_ids)
            cost_of_services = sum(service.price for service in record.room_service_ids)
            record.total_services_front_desk = cost_of_services
            record.total_services = f"{total_services} | {cost_of_services:.2f}"

    @api.depends("price_detail_ids")
    def _compute_booking_summary(self):
        for record in self:
            total_nights = record.nights
            average_daily_rate = record.average_daily_rate
            cost_of_stay = record.cost_of_stay
            self.total = cost_of_stay
            record.total_summary = (
                f"{total_nights} | {average_daily_rate:.2f} | {cost_of_stay:.2f}"
            )

    @api.depends("price_detail_ids")
    def _compute_total_price_detail(self):
        for record in self:
            total_price = sum(detail.price for detail in record.price_detail_ids)
            record.price_detail_total = total_price

    @api.depends("nights", "price_detail_total")
    def _compute_average_daily_rate(self):
        for record in self:
            if record.nights:
                record.average_daily_rate = record.price_detail_total / record.nights
            else:
                record.average_daily_rate = 0

    @api.depends("price_detail_total")
    def _compute_cost_of_stay(self):
        for record in self:
            record.cost_of_stay = record.price_detail_total

    @api.depends("check_in_date", "check_out_date")
    def _compute_nights(self):
        for record in self:
            if record.check_in_date and record.check_out_date:
                delta = record.check_out_date - record.check_in_date
                record.nights = delta.days

    def _generate_unique_uuid(self):
        current_date = datetime.now().strftime("%d%m%Y")

        while True:
            # Generate a UUID4 and take the first 6 characters
            unique_id = f"{current_date}-{str(uuid.uuid4())[:8]}"
            # Check if it already exists
            if not self.search([("unique_id", "=", unique_id)]):
                return unique_id

    @api.model
    def _update_main_availability_bookings(
        self, check_in_date, check_out_date, room_type_id, increment=True
    ):
        availability_records = self.env["main.availability"].search(
            [
                ("date", ">=", check_in_date),
                ("date", "<=", check_out_date),
                ("room_type", "=", room_type_id),
            ]
        )
        for record in availability_records:
            if increment:
                record.bookings += 1
                # record.front_desk -= 1
                # record.default -= 1
            else:
                record.bookings -= 1
            #     record.front_desk += 1
            #     record.default += 1
            # _logger.info(f"Updated bookings for {record.date}: Bookings={record.bookings}, Front Desk={record.front_desk}, Default={record.default}")

    @api.model
    def _update_main_availability_cancellations(
        self, check_in_date, check_out_date, room_type_id, increment=True
    ):
        availability_records = self.env["main.availability"].search(
            [
                ("date", ">=", check_in_date),
                ("date", "<=", check_out_date),
                ("room_type", "=", room_type_id),
            ]
        )
        for record in availability_records:
            if increment:
                record.cancellations += 1
                # record.front_desk += 1
                # record.default += 1
            else:
                record.cancellations -= 1
            #     record.front_desk -= 1
            #     record.default -= 1
            # _logger.info(f"Updated cancellations for {record.date}: Cancellations={record.cancellations}, Front Desk={record.front_desk}, Default={record.default}")

    @api.model
    def create(self, vals):
        if not vals.get("unique_id"):
            vals["unique_id"] = self._generate_unique_uuid()
        record = super().create(vals)

        if vals.get("status") == "done":
            self.env["reception"].create(
                {
                    "booking_id": record.id,
                }
            )

        # Ensure adults count does not exceed room type limit before generating accommodations
        record.set_regenerate_accommodations_flag()
        if not record._validate_adults_vs_room_type():
            raise ValidationError(
                f"The number of adults ({record.adults}) exceeds the maximum allowed guests for the selected room type."
            )
        record._generate_accommodations()

        if record.accommodation:
            record._generate_price_details()
        record.with_context(skip_write=True).write({"regenerate_accommodations": False})

        if record.room_number:
            record._update_room_inventory_dates()

        return record

    def _validate_adults_vs_room_type(self):
        for record in self:
            room_type = record.room_type_id
            if room_type:
                max_guests = int(room_type.number_of_guests)
                if int(record.adults) <= 0 or int(record.adults) > max_guests:
                    return False
        return True

    def _generate_accommodations(self):
        for booking in self:
            accommodations = self.env["accommodation"].search(
                [("booking_unique", "=", booking.unique_id)]
            )
            accommodations.unlink()
            room_types = self.env["triple"].search([])

            for room_type in room_types:
                # Validate adults vs room type before creating accommodations
                if (
                    int(booking.adults) > int(room_type.number_of_guests)
                    or int(booking.adults) <= 0
                ):
                    continue

                self.env["accommodation"].create(
                    {
                        "check_in_date": booking.check_in_date,
                        "check_out_date": booking.check_out_date,
                        "rate_plan": booking.rate_plan.id,
                        "room_type": room_type.id,
                        "adults": booking.adults,  # Pass the correct number of adults
                        "booking_unique": booking.unique_id,
                    }
                )

    def write(self, vals):
        for record in self:
            changes = []
            old_status = record.status
            new_status = vals.get("status", old_status)
            room_type_id = record.room_type_id.id
            check_in_date = record.check_in_date
            check_out_date = record.check_out_date
            if "is_paid" in vals or "is_check_out" in vals:
                is_paid = vals.get("is_paid", record.is_paid)
                is_check_out = vals.get("is_check_out", record.is_check_out)

                if not is_paid and is_check_out:
                    vals["is_check_out"] = False

            if old_status == "done" and new_status == "done":
                for field, new_value in vals.items():
                    old_value = record[field]

                    if type(old_value) != type(new_value):
                        continue

                    if old_value != new_value:
                        changes.append(
                            {
                                "booking_id": record.id,
                                "room_number": record.room_number.id,
                                "user_id": self.env.uid,
                                "field_name": field,
                                "old_value": str(old_value),
                                "new_value": str(new_value),
                            }
                        )

            if changes:
                self.env["booking.change.history"].create(changes)

            if old_status != new_status:
                if old_status == "done":
                    self._update_main_availability_bookings(
                        check_in_date, check_out_date, room_type_id, increment=False
                    )
                elif old_status == "cancel":
                    self._update_main_availability_cancellations(
                        check_in_date, check_out_date, room_type_id, increment=False
                    )

                if new_status == "done":
                    self._update_main_availability_bookings(
                        check_in_date, check_out_date, room_type_id, increment=True
                    )
                    self._create_or_update_booking_reconciliation(record)
                    self._create_or_update_accounting_calendar(record)

                reception_exists = (
                    self.env["reception"].search_count([("booking_id", "=", record.id)])
                    > 0
                )
                if not reception_exists:
                    self.env["reception"].create(
                        {
                            "booking_id": record.id,
                            "check_in_date": record.check_in_date,
                        }
                    )
                elif new_status == "cancel":
                    self._update_main_availability_cancellations(
                        check_in_date, check_out_date, room_type_id, increment=True
                    )

        for record in self:
            if "room_number" in vals:
                old_room_number = record.room_number
                if old_room_number:
                    old_room_number.write(
                        {
                            "dates_of_stay_from": False,
                            "dates_of_stay_to": False,
                        }
                    )

        result = super().write(vals)

        for record in self:
            if (
                "check_in_date" in vals
                or "check_out_date" in vals
                or "rate_plan" in vals
                or "adults" in vals
            ):
                record.set_regenerate_accommodations_flag()
                if not record._validate_adults_vs_room_type():
                    raise ValidationError(
                        f"The number of adults ({record.adults}) exceeds the maximum allowed guests for the selected room type."
                    )
                record._generate_accommodations()
            if record.accommodation:
                record._generate_price_details()
            if not self.env.context.get("skip_write"):
                self.with_context(skip_write=True).write(
                    {"regenerate_accommodations": False}
                )

        for record in self:
            if (
                "room_number" in vals
                or "check_in_date" in vals
                or "check_out_date" in vals
            ):
                record._update_room_inventory_dates()

        if old_status == "done" and new_status == "done":
            self._create_or_update_booking_reconciliation(record)

        if old_status != new_status and new_status == "done":
            self.env["sales.and.occupancy"].create(
                {
                    "booking_id": record.id,
                }
            )
            if not record.group_unique_id and not self.env["report.bookings"].search(
                [("unique_id", "=", record.unique_id)]
            ):
                self.env["report.bookings"].create(
                    {
                        "booking_id": record.id,
                    }
                )
            self.env["occupancy.rate"].create(
                {
                    "booking_id": record.id,
                }
            )
            self.env["booking.window"].create(
                {
                    "booking_id": record.id,
                }
            )
            self.env["booking.cancellations"].search(
                [("booking_id", "=", record.id)]
            ).unlink()

            if record.guest_id:
                record.guest_id.write({"booking_ids": [(4, record.id)]})

        if old_status != new_status and new_status == "cancel":
            self.env["sales.and.occupancy"].search(
                [("booking_id", "=", record.id)]
            ).unlink()
            self.env["occupancy.rate"].search([("booking_id", "=", record.id)]).unlink()
            self.env["booking.window"].search([("booking_id", "=", record.id)]).unlink()
            self.env["booking.cancellations"].create(
                {
                    "booking_id": record.id,
                }
            )

            # Remove booking from guest's booking_ids
            if record.guest_id:
                record.guest_id.write({"booking_ids": [(3, record.id)]})

        return result

    def unlink(self):
        for booking in self:
            # booking.reconciliation yozuvlarini o'chirish
            reconciliation_records = self.env["booking.reconciliation"].search(
                [("booking_id", "=", booking.id)]
            )
            reconciliation_records.unlink()
            reconciliation_records = self.env["accounting.calendar"].search(
                [("booking_id", "=", booking.id)]
            )
            reconciliation_records.unlink()

            # Eski room_number ni bo'shatish
            if booking.room_number:
                booking.room_number.write(
                    {
                        "dates_of_stay_from": False,
                        "dates_of_stay_to": False,
                    }
                )
            # Reception yozuvlarini o'chirish
            reception_records = self.env["reception"].search(
                [("unique_id", "in", self.mapped("unique_id"))]
            )
            reception_records.unlink()

            # booking o'chirilganda `sales.and.occupancy` ham o'chirilishi kerak
            sales_occupancy_records = self.env["sales.and.occupancy"].search(
                [("booking_id", "=", booking.id)]
            )
            sales_occupancy_records.unlink()

            # booking o'chirilganda `occupancy.rate` ham o'chirilishi kerak
            occupancy_rate_records = self.env["occupancy.rate"].search(
                [("booking_id", "=", booking.id)]
            )
            occupancy_rate_records.unlink()

            # booking o'chirilganda `occupancy.rate` ham o'chirilishi kerak
            booking_cancellations_records = self.env["booking.cancellations"].search(
                [("booking_id", "=", booking.id)]
            )

            # booking o'chirilganda `occupancy.rate` ham o'chirilishi kerak
            report_bookings_records = self.env["report.bookings"].search(
                [("booking_id", "=", booking.id)]
            )
            report_bookings_records.unlink()

            # booking o'chirilganda price detail ham o'chirilishi kerak
            price_details_records = self.env["booking.price.detail"].search(
                [("booking_id", "=", booking.id)]
            )

        return super().unlink()

    def _create_or_update_booking_reconciliation(self, record):
        reconciliation_record = self.env["booking.reconciliation"].search(
            [("booking_id", "=", record.id)], limit=1
        )
        if reconciliation_record:
            reconciliation_record.write(
                {
                    "status": True,
                    "booking_number": record.unique_id,
                    "guest_id": record.guest_id.id,
                    "check_in_date": record.check_in_date,
                    "check_out_date": record.check_out_date,
                    "check_in_time": record.check_in_time.id,
                    "checkout_time": record.checkout_time.id,
                    "total": record.total,
                    "commission_amount": 0.0,  # Example, you may calculate commission amount as per your requirement
                }
            )
        else:
            self.env["booking.reconciliation"].create(
                {
                    "booking_id": record.id,
                    "status": True,
                    "booking_number": record.unique_id,
                    "guest_id": record.guest_id.id,
                    "check_in_date": record.check_in_date,
                    "check_out_date": record.check_out_date,
                    "check_in_time": record.check_in_time.id,
                    "checkout_time": record.checkout_time.id,
                    # "total": record.total,
                    "commission_amount": 0.0,  # Example, you may calculate commission amount as per your requirement
                }
            )

    def _create_or_update_accounting_calendar(self, record):
        accounting_calendar_record = self.env["accounting.calendar"].search(
            [("booking_id", "=", record.id)], limit=1
        )
        if accounting_calendar_record:
            accounting_calendar_record.write(
                {
                    "status": True,
                    "booking_number": record.unique_id,
                    "guest_id": record.guest_id.id,
                    "check_in_date": record.check_in_date,
                    "check_out_date": record.check_out_date,
                    "check_in_time": record.check_in_time.id,
                    "checkout_time": record.checkout_time.id,
                    # "total": record.total,
                    "commission_amount": 0.0,  # Example, you may calculate commission amount as per your requirement
                }
            )
        else:
            self.env["accounting.calendar"].create(
                {
                    "booking_id": record.id,
                    "status": True,
                    "booking_number": record.unique_id,
                    "guest_id": record.guest_id.id,
                    "check_in_date": record.check_in_date,
                    "check_out_date": record.check_out_date,
                    "check_in_time": record.check_in_time.id,
                    "checkout_time": record.checkout_time.id,
                    "total": record.total,
                    "commission_amount": 0.0,  # Example, you may calculate commission amount as per your requirement
                }
            )

    def _update_room_inventory_dates(self):
        for record in self:
            if record.room_number:
                room_inventory = record.room_number
                room_inventory.write(
                    {
                        "dates_of_stay_from": record.check_in_date,
                        "dates_of_stay_to": record.check_out_date,
                    }
                )

    def set_regenerate_accommodations_flag(self):
        for record in self:
            record.with_context(skip_write=True).regenerate_accommodations = True

    # def _generate_accommodations(self):
    #     for booking in self:
    #         accommodations = self.env["accommodation"].search(
    #             [("booking_unique", "=", booking.unique_id)]
    #         )
    #         accommodations.unlink()
    #         room_types = self.env["triple"].search([])
    #         for room_type in room_types:
    #             self.env["accommodation"].create(
    #                 {
    #                     "check_in_date": booking.check_in_date,
    #                     "check_out_date": booking.check_out_date,
    #                     "rate_plan": booking.rate_plan.id,
    #                     "room_type": room_type.id,
    #                     # "booking_id": booking.id,
    #                     "booking_unique": booking.unique_id,
    #                 }
    #             )

    def _generate_price_details(self):
        for booking in self:
            existing_price_details = self.env["booking.price.detail"].search(
                [
                    ("booking_id", "=", booking.id),
                ]
            )
            existing_price_details.write({"active": False})

            if booking.nights > 0:
                for i in range(booking.nights):
                    date = booking.check_in_date + timedelta(days=i)
                    existing_price_detail = existing_price_details.filtered(
                        lambda p: p.date == date
                    )
                    if existing_price_detail:
                        existing_price_detail.write(
                            {
                                "price": booking.accommodation.price,
                                "active": True,
                            }
                        )
                    else:
                        new_detail = self.env["booking.price.detail"].create(
                            {
                                "booking_id": booking.id,
                                "date": date,
                                "rate_plan_id": booking.rate_plan.id,
                                "price": booking.accommodation.price,
                            }
                        )
                        existing_price_details += new_detail

    @api.onchange("accommodation")
    def _compute_available_rooms(self):
        for record in self:
            if not record.check_in_date or not record.check_out_date:
                record.available_room_ids = self.env["room.inventory"].search([]).ids
                continue

            # Check if the record has a temporary ID
            if not record.id or str(record.id).startswith("NewId_"):
                # If it's a new record, just filter by date and room type
                available_rooms = self.env["room.inventory"].search(
                    [
                        ("room_type", "=", record.room_type_id.id),
                    ]
                )
            else:
                conflicting_rooms = (
                    self.env["booking"]
                    .search(
                        [
                            ("check_in_date", "<", record.check_out_date),
                            ("check_out_date", ">", record.check_in_date),
                            ("id", "!=", record.id),
                        ]
                    )
                    .mapped("room_number.id")
                )

                available_rooms = self.env["room.inventory"].search(
                    [
                        ("id", "not in", conflicting_rooms),
                        ("room_type", "=", record.room_type_id.id),
                    ]
                )
            record.available_room_ids = available_rooms.ids

    @api.onchange("accommodation")
    def _onchange_accommodation(self):
        if self.accommodation:
            self.room_number = False
            self.room_type_id = self.accommodation.room_type.id
            self._compute_available_rooms()
            # if self.available_room_ids:
            #     self.room_number = self.available_room_ids[0].id
            return {
                "domain": {"room_number": [("id", "in", self.available_room_ids.ids)]}
            }
        else:
            self.room_type_id = False

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        param_obj = self.env["ir.config_parameter"].sudo()
        check_in_time_id = param_obj.get_param("property_settings.check_in_time")
        check_out_time_id = param_obj.get_param("property_settings.check_out_time")
        default_rate_plan = self.env["rate.plan"].search(
            [("front_desk_booking", "=", True)], limit=1
        )

        if check_in_time_id:
            defaults["check_in_time"] = int(check_in_time_id)
        if check_out_time_id:
            defaults["checkout_time"] = int(check_out_time_id)
        if default_rate_plan:
            defaults["rate_plan"] = default_rate_plan.id

        if defaults.get("room_type_id"):
            room_type_id = defaults["room_type_id"]
            default_room_number = self.env["room.inventory"].search(
                [("room_type", "=", room_type_id)], limit=1
            )
            if default_room_number:
                defaults["room_number"] = default_room_number.id

        return defaults

    @api.model
    def get_booking_data(self):
        # Fetch bookings
        arrivals = self.search([("arrival_status", "!=", False)])
        departures = self.search([("departure_status", "!=", False)])
        occupied_rooms = self.search([("arrival_status", "=", "arrival")])

        # Format data
        def format_booking_data(booking):
            return {
                "booking_number": booking.unique_id,
                "customer": booking.guest_id,
                "room_number": booking.room_number.number
                if booking.room_number
                else "",
                "check_in_time": booking.check_in_time.name
                if booking.check_in_time
                else "",
                "room_type": booking.room_type_id.rooms if booking.room_type_id else "",
                "Balance": f"{booking.total} uzs",
                "tags": booking.tag if booking.tag else "",
                "notes": booking.guest_comment or "No",
                "nights": booking.nights,
                "guest_comment": booking.guest_comment or "No",
                "arrival_status": booking.arrival_status,
                "departure_status": booking.departure_status,
            }

        data = {
            "arrivals": [format_booking_data(booking) for booking in arrivals],
            "departures": [format_booking_data(booking) for booking in departures],
            "occupied_rooms": [
                format_booking_data(booking) for booking in occupied_rooms
            ],
        }

        return data

    def action_move_room(self):
        self.ensure_one()

        move_room = self.env["front_desk.move_room"].create(
            {
                "booking_id": self.id,
            }
        )

        return {
            "type": "ir.actions.act_window",
            "res_model": "front_desk.move_room",
            "name": "Move Room",
            "target": "new",
            "view_mode": "form",
            "res_id": move_room.id,
        }

    def action_pay(self):
        self.ensure_one()

        reception = self.env["reception"].search(
            [("booking_id", "=", self.id)], limit=1
        )
        invoice = self.env["reception.invoice"].search(
            [("reception_id", "=", reception.id)], limit=1
        )

        payment = self.env["reception.payment"].create(
            {
                "invoice_id": invoice.id,
            }
        )

        return {
            "type": "ir.actions.act_window",
            "res_model": "reception.payment",
            "name": "Pay",
            "target": "new",
            "view_mode": "form",
            "res_id": payment.id,
        }

    def action_cancel(self):
        self.ensure_one()
        cancellation = self.env["front_desk.cancel_booking"].create(
            {"booking_id": self.id}
        )

        return {
            "type": "ir.actions.act_window",
            "res_model": "front_desk.cancel_booking",
            "name": "Cancel",
            "target": "new",
            "view_mode": "form",
            "res_id": cancellation.id,
        }

    @api.depends("room_number", "room_type_id", "guest_id")
    def _compute_name(self):
        for record in self:
            room_number = record.room_number.number
            guest = record.guest_id.full_name
            room_type = record.room_type_id.rooms
            record.name = f"{room_number} | {guest} | {room_type}"

    @api.onchange("booking_condition")
    def _set_housekeeping_status(self):
        for record in self:
            if record.booking_condition:
                if record.booking_condition == "checked_out":
                    housekeeping = self.env["room_inventory.housekeeping"].search(
                        [("number", "=", record.room_number.number)], limit=1
                    )
                    print("test")
                    print(
                        housekeeping.id,
                        housekeeping.status,
                        housekeeping.number,
                        housekeeping.room_type,
                        "test",
                    )
                    if housekeeping:
                        housekeeping.status = "need_to_clean"


class BookingChangeHistory(models.Model):
    _name = "booking.change.history"
    _description = "Booking Change History"

    booking_id = fields.Many2one("booking", string="Booking", ondelete="cascade")
    change_time = fields.Datetime(string="Change Time", default=fields.Datetime.now)
    room_number = fields.Many2one("room.inventory", string="Room Number")
    user_id = fields.Many2one("res.users", string="User")
    field_name = fields.Char(string="Changed Field")
    old_value = fields.Char(string="Old Value")
    new_value = fields.Char(string="New Value")


class BookingPriceDetail(models.Model):
    _name = "booking.price.detail"
    _description = "Booking Price Detail"

    booking_id = fields.Many2one("booking", string="Booking")
    booking_unique_id = fields.Char(related="booking_id.unique_id", string="Unique ID")
    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")
    price = fields.Float(string="Price")
    date = fields.Date(string="Date")
    discount_id = fields.Many2one("booking.discount", string="Discount")
    amount = fields.Float(string="Amount", compute="_compute_amount")
    active = fields.Boolean(string="Active", default=True)

    _sql_constraints = [
        (
            "unique_discount_id",
            "unique(discount_id)",
            "Each booking price detail must be linked to a unique discount.",
        ),
    ]

    @api.model
    def create(self, vals):
        existing_record = self.search(
            [
                ("booking_id", "=", vals.get("booking_id")),
                ("date", "=", vals.get("date")),
            ],
            limit=1,
        )
        if existing_record:
            existing_record.write(vals)
            return existing_record
        else:
            record = super().create(vals)
            if "discount_id" not in vals:
                discount = self.env["booking.discount"].create(
                    {
                        "price_detail_id": record.id,
                        "price": record.price,
                        "booking_unique_id": record.booking_unique_id,
                    }
                )
                record.discount_id = discount.id
            return record

    def unlink(self):
        for record in self:
            if record.discount_id:
                record.discount_id.unlink()
        return super().unlink()

    @api.depends("discount_id.discount_price", "price")
    def _compute_amount(self):
        for record in self:
            if record.discount_id and record.discount_id.discount_price != record.price:
                record.amount = record.discount_id.discount_price
            else:
                record.amount = record.price


class BookingDiscount(models.Model):
    _name = "booking.discount"
    _description = "Booking Discount"
    _rec_name = "display_value"

    booking_unique_id = fields.Char(string="Unique ID")
    price_detail_id = fields.Many2one("booking.price.detail", string="Price Detail")
    price = fields.Float(string="Price", compute="_compute_price", store=True)
    discount_price = fields.Float(
        string="Discount Price", compute="_compute_discount_price", store=True
    )
    type_of_discount = fields.Selection(
        [("flat_rate", "Flat Rate"), ("percent", "Percent")],
        string="Type of Discount",
        default="percent",
    )
    value = fields.Integer(string="Value")
    reason = fields.Text(string="Reason")
    apply = fields.Selection(
        [
            ("to_selected_date", "To Selected Date"),
            ("to_selected_and_future_dates", "To Selected and Future Dates"),
            ("to_all_dates", "To All Dates"),
        ],
        string="Apply",
    )
    display_value = fields.Char(
        string="Display Value", compute="_compute_display_value", store=True
    )

    @api.model
    def create(self, vals):
        existing_record = self.search(
            [("price_detail_id", "=", vals.get("price_detail_id"))],
            limit=1,
        )
        if existing_record:
            existing_record.write(vals)
            return existing_record
        else:
            return super().create(vals)

    @api.depends("price_detail_id")
    def _compute_price(self):
        for record in self:
            record.price = (
                record.price_detail_id.price if record.price_detail_id else 0.0
            )

    @api.depends("type_of_discount", "value", "price")
    def _compute_discount_price(self):
        for record in self:
            if record.type_of_discount == "flat_rate":
                record.discount_price = record.price - record.value
            elif record.type_of_discount == "percent":
                record.discount_price = record.price - (
                    record.price * (record.value / 100)
                )
            else:
                record.discount_price = record.price

    @api.depends("value")
    def _compute_display_value(self):
        for record in self:
            record.display_value = str(record.value if record.value else 0)


class RoomService(models.Model):
    _name = "room.service"
    _description = "Room Service"
    _rec_name = "service"

    booking_id = fields.Many2one(
        "booking", string="Booking", required=True, ondelete="cascade"
    )
    service = fields.Char(string="Service", required=True)
    payment_type = fields.Selection(
        [
            ("included", "Included in the room rate"),
            ("extra", "Extra charge"),
        ],
        string="Payment Type",
        default="included",
    )
    charge_type = fields.Selection(
        [
            ("per_guest_per_night", "Per guest per night"),
            ("per_room_per_night", "Per room per night"),
        ],
        string="Charge Type",
        default="per_guest_per_night",
    )
    delivery_date = fields.Date(
        string="Delivery Date",
        default=lambda self: fields.Date.today() + timedelta(days=1),
    )
    price = fields.Float(string="Price", default=0.0)
    quantity = fields.Integer(string="Quantity", default=1)
    amount = fields.Float(string="Amount", compute="_compute_amount", store=True)
    comment = fields.Text(string="Comment")

    @api.depends("price", "quantity")
    def _compute_amount(self):
        for record in self:
            record.amount = record.price * record.quantity
