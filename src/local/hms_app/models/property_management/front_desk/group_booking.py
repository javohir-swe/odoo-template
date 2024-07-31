import uuid
from datetime import timedelta

from odoo import api, fields, models

from ...data import ALL_TIMES


class GroupBooking(models.Model):
    _name = "group_booking"
    _description = "GroupBooking"
    _rec_name = "group_name"

    js_field = fields.Char(string="JS Field")
    group_name = fields.Char(string="Group Name", required=True)
    customer_company_id = fields.Many2one("company", string="Customer Company")
    agent_company_id = fields.Many2one("company", string="Agent Company")

    profile_id = fields.Many2one("guest", string="Profile")
    first_name = fields.Char(string="First Name", store=True)
    last_name = fields.Char(string="Last Name", store=True)
    middle_name = fields.Char(string="Middle Name", store=True)
    phone_number = fields.Char(string="Phone Number", store=True)
    email = fields.Char(string="Email", store=True)
    dates_of_stay_from = fields.Date(
        string="Dates of Stay From", default=fields.Date.today
    )
    dates_of_stay_to = fields.Date(
        string="Dates of Stay To",
        default=lambda self: fields.Date.today() + timedelta(days=1),
    )
    nights = fields.Integer(string="Nights", compute="_compute_nights", store=True)
    check_in_time = fields.Many2one("check.in.check.out.time", string="Check In Time")
    check_out_time = fields.Many2one("check.in.check.out.time", string="Check Out Time")
    check_in_times = fields.Selection(
        ALL_TIMES,
        string="Check-in Times",
        default=lambda self: self._get_default_check_in_time(),
    )

    check_out_times = fields.Selection(
        ALL_TIMES,
        string="Check-out Times",
        default=lambda self: self._get_default_check_out_time(),
    )

    # Done ✅
    # room_type va boshqa ma'lumotlarni bitta modelga yig'ib automatik ulanadigan qilish kerak

    rooms_info_ids = fields.One2many(
        "group_booking.room_type", "rooms_info", string="rooms_info"
    )

    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount")
    booking_details_ids = fields.One2many(
        "booking.details", "group_booking_id", string="Booking Details"
    )
    detail_total_amount = fields.Float(
        string="Detail Total Amount", compute="_compute_detail_total_amount"
    )
    comment = fields.Text(string="Comment")
    accommodation_ids = fields.One2many(
        "group.booking.accommodation", "group_booking_id", string="Accommodation"
    )
    done = fields.Boolean(string="Done")
    group_unique_id = fields.Char(
        string="Unique ID",
        readonly=True,
        copy=False,
        default=lambda self: self._generate_unique_uuid(),
    )

    @api.model
    def _get_default_check_in_time(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("property_settings.check_in_times")
        )

    @api.model
    def _get_default_check_out_time(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("property_settings.check_out_times")
        )

    def _generate_unique_uuid(self):
        while True:
            # Generate a UUID4 and take the first 6 characters
            group_unique_id = str(uuid.uuid4())[:6]
            # Check if it already exists
            if not self.search([("group_unique_id", "=", group_unique_id)]):
                return group_unique_id

    @api.depends("dates_of_stay_from", "dates_of_stay_to")
    def _compute_nights(self):
        for record in self:
            if record.dates_of_stay_from and record.dates_of_stay_to:
                delta = record.dates_of_stay_to - record.dates_of_stay_from
                record.nights = delta.days

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        param_obj = self.env["ir.config_parameter"].sudo()
        check_in_time_id = param_obj.get_param("property_settings.check_in_time")
        check_out_time_id = param_obj.get_param("property_settings.check_out_time")

        if check_in_time_id:
            defaults["check_in_time"] = int(check_in_time_id)
        if check_out_time_id:
            defaults["check_out_time"] = int(check_out_time_id)

        return defaults

    @api.model
    def create(self, vals):
        record = super().create(vals)
        triple_records = self.env["triple"].search([])
        record._create_accommodation_records()
        for triple in triple_records:
            main_availability_record = self.env["main.availability"].search(
                [
                    ("room_type", "=", triple.id),
                    ("date", "=", vals.get("dates_of_stay_from")),
                ],
                limit=1,
            )

            available = (
                main_availability_record.online if main_availability_record else 0
            )

            self.env["group_booking.room_type"].create(
                {
                    "rooms_info": record.id,
                    "room_type": triple.id,
                    "available": available,
                }
            )

        if vals.get("done"):
            self.create_related_bookings(record)

        return record

    def write(self, vals):
        res = super().write(vals)
        self._create_accommodation_records()
        if vals.get("done"):  # Check if 'done' is being set to True
            # self.create_related_report_bookings(record)
            for record in self:
                self.create_related_bookings(record)
        return res

    @api.depends("rooms_info_ids.rooms_id", "rooms_info_ids.price")
    def _compute_total_amount(self):
        for record in self:
            total = 0
            for room_type_data in record.rooms_info_ids:
                if room_type_data.rooms_id and room_type_data.price:
                    total += (
                        room_type_data.rooms_id.number * room_type_data.price.price
                    )  # Assuming price is a Many2one to rate_plan.price model which has a field 'amount'
            record.total_amount = total

    @api.depends("booking_details_ids.price")
    def _compute_detail_total_amount(self):
        for record in self:
            total = sum(
                detail.price.price
                for detail in record.booking_details_ids
                if detail.price
            )
            record.detail_total_amount = total

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        param_obj = self.env["ir.config_parameter"].sudo()
        check_in_time_id = param_obj.get_param("property_settings.check_in_time")
        check_out_time_id = param_obj.get_param("property_settings.check_out_time")

        if check_in_time_id:
            defaults["check_in_time"] = int(check_in_time_id)
        if check_out_time_id:
            defaults["check_out_time"] = int(check_out_time_id)

        return defaults

    def _create_accommodation_records(self):
        for record in self:
            assigned_rooms = []  # List to keep track of assigned rooms
            record.accommodation_ids.unlink()  # Clear existing records

            for room_info in record.rooms_info_ids:
                if room_info.rooms_id:
                    available_rooms = self.env["room.inventory"].search(
                        [
                            ("room_type", "=", room_info.room_type.id),
                            ("id", "not in", assigned_rooms),
                        ],
                        limit=room_info.rooms_id.number,
                    )  # Ensure to get only the required number of rooms

                    for room in available_rooms:
                        assigned_rooms.append(room.id)

                        # Check if an accommodation record already exists
                        existing_accommodation = self.env[
                            "group.booking.accommodation"
                        ].search(
                            [
                                ("group_booking_id", "=", record.id),
                                ("room_type", "=", room_info.room_type.id),
                                ("rooms", "=", room.id),
                                (
                                    "dates_of_stay",
                                    "=",
                                    f"{record.dates_of_stay_from} - {record.dates_of_stay_to} ({record.nights})",
                                ),
                            ],
                            limit=1,
                        )

                        if existing_accommodation:
                            existing_accommodation.write(
                                {
                                    "beds": 0,  # Adjust as per your requirement
                                    "extra_beds": 0,  # Adjust as needed
                                    "guests": len(
                                        room_info.adult_ids
                                    ),  # Example, adjust as needed
                                    "guest_full_name": record.profile_id.first_name,  # Adjust as needed
                                }
                            )
                        else:
                            self.env["group.booking.accommodation"].create(
                                {
                                    "room_type": room_info.room_type.id,
                                    "beds": 0,  # Adjust as per your requirement
                                    "extra_beds": 0,  # Adjust as needed
                                    "rooms": room.id,
                                    "guests": len(
                                        room_info.adult_ids
                                    ),  # Example, adjust as needed
                                    "guest_full_name": record.profile_id.first_name,  # Adjust as needed
                                    "dates_of_stay": f"{record.dates_of_stay_from} - {record.dates_of_stay_to} ({record.nights})",
                                    "group_booking_id": record.id,
                                    "dates_of_stay_from": record.dates_of_stay_from,
                                    "dates_of_stay_to": record.dates_of_stay_to,
                                }
                            )

    @api.onchange("accommodation_ids")
    def _onchange_accommodation_ids(self):
        if self.accommodation_ids:
            selected_room_types = self.accommodation_ids.mapped("room_type").ids
            return {
                "domain": {
                    "booking_details_ids": [("room_type", "in", selected_room_types)]
                }
            }

    def create_related_report_bookings(self, group_booking_record):
        """GroupBooking create bo'lganida nechta xona bo'lsa shuncha 'report.bookings' create bo'layapti. Sababi
        create_related_report_bookings ishlamayappti, va booking create qilayapti."""
        report_bookings = self.env["report.bookings"]
        for room_info in group_booking_record.accommodation_ids:
            report_booking_vals = {
                "customer_company_id": group_booking_record.customer_company_id.id,
                "agent_company_id": group_booking_record.agent_company_id.id,
                "check_in_date": group_booking_record.dates_of_stay_from,
                "check_out_date": group_booking_record.dates_of_stay_to,
                "nights": 1111111111,
                "first_name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "last_name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "middle_name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "email": group_booking_record.email,
                "phone": group_booking_record.phone_number,
                "group_unique_id": "salomlar",
            }
            print("============================================")
            print("============================================")
            print("============================================")
            print(report_booking_vals)
            print("============================================")
            print("============================================")
            print("============================================")
            report_bookings.create(report_booking_vals)

    def create_related_bookings(self, group_booking_record):
        Booking = self.env["booking"]
        if group_booking_record.done:  # Agar 'done' True bo'lsa
            for room_info in group_booking_record.accommodation_ids:
                rooms = self.env["room.inventory"].search(
                    [("id", "=", room_info.rooms.id)]
                )
                for room in rooms:  # Har bir xona uchun
                    booking_vals = {
                        "group_unique_id": group_booking_record.group_unique_id,
                        "customer_company_id": group_booking_record.customer_company_id.id,
                        "agent_company_id": group_booking_record.agent_company_id.id,
                        "guest_id": group_booking_record.profile_id.id,
                        "check_in_date": group_booking_record.dates_of_stay_from,
                        "check_out_date": group_booking_record.dates_of_stay_to,
                        "check_in_time": group_booking_record.check_in_time.id,
                        "checkout_time": group_booking_record.check_out_time.id,
                        "room_type_id": room_info.room_type.id,
                        "room_number": room.id,  # To'g'ridan-to'g'ri xona raqamini olish
                        "guest_comment": group_booking_record.comment,
                        "status": "done",
                    }
                    # Mavjud Booking yozuvini aniqlash
                    existing_booking = Booking.search(
                        [
                            (
                                "group_unique_id",
                                "=",
                                group_booking_record.group_unique_id,
                            ),
                            ("room_number", "=", room.id),
                            (
                                "check_in_date",
                                "=",
                                group_booking_record.dates_of_stay_from,
                            ),
                            (
                                "check_out_date",
                                "=",
                                group_booking_record.dates_of_stay_to,
                            ),
                        ],
                        limit=1,
                    )
                    if existing_booking:
                        existing_booking.write(booking_vals)
                    else:
                        Booking.create(booking_vals)


class GroupBookingAccommodation(models.Model):
    _name = "group.booking.accommodation"
    _description = "Group Booking Accommodation"

    room_type = fields.Many2one("triple", string="Room Type")
    beds = fields.Integer(string="Beds")
    extra_beds = fields.Integer(string="Extra Beds")
    rooms = fields.Many2one(
        "room.inventory", string="Rooms", domain="[('room_type', '=', room_type)]"
    )
    guests = fields.Integer(string="Guests")
    guest_full_name = fields.Char(string="Guest Full Name")
    dates_of_stay = fields.Char(string="Dates of Stay")
    group_booking_id = fields.Many2one("group_booking", string="Group Booking")
    dates_of_stay_from = fields.Date("dates_of_stay_from")
    dates_of_stay_to = fields.Date("dates_of_stay_to")
    available_rooms = fields.Many2many("room.inventory", string="Available Rooms")

    @api.onchange("room_type", "dates_of_stay_from", "dates_of_stay_to")
    def _onchange_room_type_dates(self):
        if self.room_type and self.dates_of_stay_from and self.dates_of_stay_to:
            dates_of_stay_from_str = fields.Date.to_string(self.dates_of_stay_from)
            dates_of_stay_to_str = fields.Date.to_string(self.dates_of_stay_to)

            booked_room_ids = (
                self.env["room.inventory"]
                .search(
                    [
                        ("room_type", "=", self.room_type.id),
                        "|",
                        "&",
                        ("dates_of_stay_from", "<=", dates_of_stay_to_str),
                        ("dates_of_stay_from", ">=", dates_of_stay_from_str),
                        "&",
                        ("dates_of_stay_to", ">=", dates_of_stay_from_str),
                        ("dates_of_stay_to", "<=", dates_of_stay_to_str),
                    ]
                )
                .ids
            )

            available_rooms = self.env["room.inventory"].search(
                [
                    ("room_type", "=", self.room_type.id),
                    ("id", "not in", booked_room_ids),
                ]
            )

            self.available_rooms = available_rooms
            self.rooms = False  # Reset the rooms field
            return {"domain": {"rooms": [("id", "in", available_rooms.ids)]}}
        else:
            self.available_rooms = [(5, 0, 0)]
            self.rooms = False
            return {"domain": {"rooms": []}}

    # @api.constrains("rooms", "dates_of_stay_from", "dates_of_stay_to")
    # def _check_room_availability(self):
    #     for record in self:
    #         if record.rooms:
    #             overlapping_bookings = self.env["group.booking.accommodation"].search(
    #                 [
    #                     ("rooms", "=", record.rooms.id),
    #                     ("id", "!=", record.id),
    #                     ("dates_of_stay_from", "<=", record.dates_of_stay_to),
    #                     ("dates_of_stay_to", ">=", record.dates_of_stay_from),
    #                 ]
    #             )
    #             if overlapping_bookings:
    #                 raise exceptions.ValidationError(
    #                     "The room %s is already booked for the selected dates."
    #                     % record.rooms.number
    #                 )


class BookingDetails(models.Model):
    _name = "booking.details"
    _description = "Booking Details"

    room_type = fields.Many2one("triple", string="Room Type")
    date_of_stay = fields.Char(string="Date of Stay")
    rooms = fields.Many2one("room.inventory", string="Rooms")
    guest = fields.Integer(string="Guest")
    rate_plan = fields.Many2one("rate.plan", string="Rate Plan")
    price = fields.Many2one("rate_plan.price", string="Price")
    discount = fields.Many2one("booking.discount", string="Discount")

    check_in = fields.Char(string="Check-in")
    check_out = fields.Char(string="Check-out")
    amount = fields.Char(string="Amount")

    group_booking_id = fields.Many2one("group_booking", string="Group Booking")


class GroupBookingRoomTypeData(models.Model):
    _name = "group_booking.room_type"
    _description = "Group Booking Room Type Data"
    _rec_name = "room_type"

    room_type = fields.Many2one("triple", string="Room Type")
    dates_of_stay_from = fields.Date(
        related="rooms_info.dates_of_stay_from", string="Dates of Stay From"
    )
    dates_of_stay_to = fields.Date(
        related="rooms_info.dates_of_stay_to", string="Dates of Stay To"
    )
    available = fields.Integer(string="Available", compute="_compute_available")
    adult_id = fields.Many2one(
        "room_type.guests", string="adult_id", domain="[('id', 'in', adult_ids)]"
    )
    adult_ids = fields.Many2many("room_type.guests", string="Adult IDs")
    rooms_id = fields.Many2one("group_booking.selection", string="rooms_id")
    rate_plan = fields.Many2one("rate.plan", string="Rate Plan")
    price = fields.Many2one("rate_plan.price", string="Price", compute="_compute_price")
    rooms_info = fields.Many2one("group_booking", string="Rooms Info")

    @api.depends("dates_of_stay_from", "room_type")
    def _compute_available(self):
        for record in self:
            if record.dates_of_stay_from and record.room_type:
                main_availability_records = self.env["main.availability"].search(
                    [
                        ("date", "=", record.dates_of_stay_from),
                        ("room_type", "=", record.room_type.id),
                    ]
                )
                if main_availability_records:
                    min_front_desk_availability = min(
                        avail.online for avail in main_availability_records
                    )
                    record.available = min_front_desk_availability
                else:
                    record.available = 0
            else:
                record.available = 0

    @api.depends(
        "dates_of_stay_from", "dates_of_stay_to", "rate_plan", "room_type", "adult_ids"
    )
    def _compute_price(self):
        for record in self:
            price_record = self.env["rate_plan.price"].search(
                [
                    ("rate_plan_id", "=", record.rate_plan.id),
                    ("room_type_id", "=", record.room_type.id),
                    ("guest_id", "in", record.adult_ids.ids),
                    ("relevant_date", ">=", record.dates_of_stay_from),
                    ("relevant_date", "<=", record.dates_of_stay_to),
                ],
                limit=1,
            )
            record.price = price_record.id if price_record else False

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        default_rate_plan = self.env["rate.plan"].search(
            [("front_desk_booking", "=", True)], limit=1
        )
        if default_rate_plan:
            defaults["rate_plan"] = default_rate_plan.id

        # room_type maydoni oldindan tanlangan bo'lsa, adult_ids maydonini yangilash
        if "room_type" in defaults and defaults["room_type"]:
            room_type = self.env["triple"].browse(defaults["room_type"])
            defaults["adult_ids"] = [(6, 0, room_type.guest_ids.ids)]

        return defaults

    @api.model
    def create(self, vals):
        record = super().create(vals)
        # Create method adjustments
        if record.available:
            for i in range(1, record.available + 1):
                self.env["group_booking.selection"].create(
                    {
                        "name": f"Selection {i}",
                        "number": i,
                        "room_type_data_id": record.id,
                    }
                )
        return record

    def write(self, vals):
        result = super().write(vals)
        # Write method adjustments
        if "available" in vals and vals["available"]:
            # Remove existing selections
            self.env["group_booking.selection"].search(
                [("room_type_data_id", "=", self.id)]
            ).unlink()
            # Create new selections based on available value
            for i in range(1, vals["available"] + 1):
                self.env["group_booking.selection"].create(
                    {
                        "name": f"Selection {i}",
                        "number": i,
                        "room_type_data_id": self.id,
                    }
                )
        return result

    @api.onchange("room_type")
    def _onchange_room_type(self):
        if self.room_type:
            self.adult_ids = self.room_type.guest_ids


class GroupBookingSelection(models.Model):
    _name = "group_booking.selection"
    _description = "Group Booking Celection"
    _rec_name = "name"

    name = fields.Char("Name", compute="_compute_name", store=True)
    number = fields.Integer("Number of Rooms")
    # max_person = fields.Integer("Max Persons")
    room_type_data_id = fields.Many2one(
        "group_booking.room_type", string="Room Type Data"
    )

    @api.depends("number")
    def _compute_name(self):
        for record in self:
            record.name = "{} rooms ".format(
                record.number
                # record.number, record.max_person
            )
