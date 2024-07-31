import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class IconNo(models.Model):
    _name = "icon_no"
    _description = "Icon No"

    name = fields.Char(required=True)
    icon = fields.Binary(required=True)


# class AllIcons(models.Model):
#     _name = "all.icons"
#     _description = "All Icons"
#
#     icon_ids = fields.Many2many("icon_no", required=True)


class Triple(models.Model):
    """Room Types"""

    _name = "triple"
    _description = "Room Types"
    _rec_name = "rooms"

    # Primary Key
    sequence = fields.Integer("Sequence", help="Determines the order of items")
    id = fields.Integer(primary_key=True)

    # Main settings
    rooms = fields.Char(required=True)
    room_code = fields.Char(required=True)

    # Occupancy
    accommodation_offer = fields.Many2one(
        "accommodation_offer", string="Accommodation Offer"
    )
    accommodation_offers = fields.Selection(
        [
            ("apartment", "Apartment"),
            ("villa", "Villa"),
            ("house", "House"),
            ("small_house", "Small house"),
            ("flat", "Flat"),
            ("room", "Room"),
            ("cottage", "Cottage"),
            ("bed_in_room", "Bed in room"),
            ("studio", "Studio"),
            ("a_frame_house", "A-frame house"),
            ("barn_house", "Barn house"),
            ("bell_tent", "Bell tent"),
            ("bungalow", "Bungalow"),
            ("houseboat", "Houseboat"),
            ("motorhome", "Motorhome"),
            ("indian_tipi", "Indian tipi"),
            ("camp_house", "Camp house"),
            ("camping", "Camping"),
            ("dome_tent", "Dome tent"),
            ("campsite", "Campsite"),
            ("tent", "Tent"),
            ("floating_home", "Floating home"),
            ("safari_tent", "Safari tent"),
            ("folding_tent", "Folding tent"),
            ("tent_house", "Tent house"),
            ("hut", "Hut"),
            ("chalet", "Chalet"),
            ("pavilion", "Pavilion"),
            ("eco_house", "Eco-house"),
            ("yurt", "Yurt"),
        ],
        default="room",
        string="Accommodation Offer",
    )
    area = fields.Selection(
        [("same", "Same"), ("different", "Different")], default="same"
    )
    area_m = fields.Float("from (m²)")
    area_max_value = fields.Float("up to (m²)")
    number_of_rooms = fields.Integer()

    child_aged_from = fields.Many2many(
        "child.age.range",
        string="Child Age Range",
        relation="triple_child_age_rel",
        column1="triple",
        column2="child_id",
        domain=lambda self: [("id", "in", self._get_allowed_child_ages())],
    )

    number_of_guests = fields.Selection(
        [
            ("0", 0),
            ("1", 1),
            ("2", 2),
            ("3", 3),
            ("4", 4),
            ("5", 5),
            ("6", 6),
            ("7", 7),
        ],
        default="0",
        string="Number Of Guests",
    )
    # Bug quyidagi fildlarni many2manyga o'zgartirish kerak.
    # Assuming that there's a Boolean field for each room type
    single_room = fields.Boolean(store=True, readonly=False)
    double_room = fields.Boolean(store=True, readonly=False)
    triple_room = fields.Boolean(store=True, readonly=False)
    fourth_room = fields.Boolean(store=True, readonly=False)
    fifth_room = fields.Boolean(store=True, readonly=False)
    sixth_room = fields.Boolean(store=True, readonly=False)
    seventh_room = fields.Boolean(store=True, readonly=False)

    guest_ids = fields.Many2many(
        "room_type.guests",
        "triple_guest_ids_rel",
        "triple_id",
        "guests_id",
        string="Guests",
    )
    guest_count = fields.Integer(
        string="Guest Count",
        compute="_compute_guest_count",
        store=True,
    )

    number_of_extra_guests = fields.Selection(
        [("0", "0"), ("1", "1"), ("2", "2"), ("3", "3")],
        default="0",
        string="Extra guests",
    )
    number_of_baby = fields.Selection(
        [("0", "0"), ("1", "1"), ("2", "2")],
        default="0",
        string="Number of children without bed",
    )

    # Room amenities
    video_and_audio = fields.Many2many(
        "video_and_audio",
        "triple_video_audio_rel",
        "triple_id",
        "audio_video_id",
        string="Video and Audio",
    )
    electronic_devices = fields.Many2many(
        "electronic_devices",
        "triple_electronic_devices_rel",
        "triple_id",
        "device_id",
        string="Electronic Devices",
    )
    bathroom = fields.Many2many(
        "bathroom", "triple_bathroom_rel", "triple_id", "bathroom_id", string="Bathroom"
    )
    outdoor_area_and_window_view = fields.Many2many(
        "outdoor_area_and_window_view",
        "triple_outdoor_area_rel",
        "triple_id",
        "outdoor_area_id",
        string="Outdoor Area and Window View",
    )
    internet_and_telephony = fields.Many2many(
        "internet_and_telephony",
        "triple_internet_telephony_rel",
        "triple_id",
        "internet_telephony_id",
        string="Internet and Telephony",
    )
    furniture = fields.Many2many(
        "furniture",
        "triple_furniture_rel",
        "triple_id",
        "furniture_id",
        string="Furniture",
    )
    others = fields.Many2many(
        "others", "triple_others_rel", "triple_id", "other_id", string="Others"
    )

    # Room preferences
    smoking_in_room = fields.Many2many(
        "smoking_in_room",
        "triple_smoking_room_rel",
        "triple_id",
        "smoking_id",
        string="Smoking in Room",
    )
    non_smoking_room = fields.Boolean("non-smoking room")
    smoking_room = fields.Selection(
        [
            ("not_selected", "not selected"),
            ("smoking_room", "smoking room"),
            ("non_smoking_room", "non-smoking room"),
        ],
        default="not_selected",
    )
    beds = fields.Many2many(
        "beds", "triple_beds_rel", "triple_id", "bed_id", string="Beds"
    )
    window_view = fields.Many2many(
        "outdoor_area_and_window_view",
        "triple_window_view_rel",
        "triple_id",
        "window_view_id",
        string="Window View",
    )
    all_icons = fields.Many2many("icon_no")
    # Priority of room amenities
    icon_no_1 = fields.Many2one(
        "icon_no",
        string="Icon No (Category 1)",
    )
    icon_no_2 = fields.Many2one(
        "icon_no",
        string="Icon No (Category 2)",
    )
    icon_no_3 = fields.Many2one(
        "icon_no",
        string="Icon No (Category 3)",
    )
    icon_no_4 = fields.Many2one(
        "icon_no",
        string="Icon No (Category 4)",
    )
    icon_no_5 = fields.Many2one(
        "icon_no",
        string="Icon No (Category 5)",
    )
    # Room description
    room_description = fields.Text()

    # Room photos
    room_photos = fields.Many2many(
        "room_image",
        "triple_room_image_rel",
        "triple_id",
        "image_id",
        string="Room Photos",
    )
    active = fields.Boolean(default=True, string="On/off", store=True, readonly=False)
    photo_count = fields.Integer(string="Photos", compute="_compute_related_count")

    @api.onchange("number_of_guests")
    def _onchange_number_of_guests(self):
        guests = int(self.number_of_guests) if self.number_of_guests else 0

        self.single_room = guests >= 1
        self.double_room = guests >= 2
        self.triple_room = guests >= 3
        self.fourth_room = guests >= 4
        self.fifth_room = guests >= 5
        self.sixth_room = guests >= 6
        self.seventh_room = guests >= 7

    @api.onchange(
        "single_room",
        "double_room",
        "triple_room",
        "fourth_room",
        "fifth_room",
        "sixth_room",
        "seventh_room",
    )
    def _onchange_room_selection(self):
        guest_numbers = []
        if self.single_room:
            guest_numbers.append("1")
        if self.double_room:
            guest_numbers.append("2")
        if self.triple_room:
            guest_numbers.append("3")
        if self.fourth_room:
            guest_numbers.append("4")
        if self.fifth_room:
            guest_numbers.append("5")
        if self.sixth_room:
            guest_numbers.append("6")
        if self.seventh_room:
            guest_numbers.append("7")

        if guest_numbers:
            self.guest_ids = [
                (
                    6,
                    0,
                    self.env["room_type.guests"]
                    .search(
                        [
                            ("guest_number", "in", guest_numbers),
                            ("room_type", "=", self.rooms),
                        ]
                    )
                    .ids,
                )
            ]
        else:
            self.guest_ids = [
                (5, 0, 0)
            ]  # Clear the guest_ids field if no rooms are selected

    @api.depends("guest_ids")
    def _compute_guest_count(self):
        for record in self:
            record.guest_count = len(record.guest_ids)

    @api.model
    def _get_allowed_child_ages(self):
        # Access the company directly from the environment
        company = self.env.user.company_id
        return company.child_ages.ids if company else []

    @api.onchange("child_aged_from")
    def _onchange_child_aged_from(self):
        # This method ensures that the domain is updated interactively in the UI
        return {
            "domain": {
                "child_aged_from": [("id", "in", self._get_allowed_child_ages())]
            }
        }

    @api.depends("number_of_guests")
    def _compute_child_aged_from(self):
        for record in self:
            record.child_aged_from = record.number_of_guests > "1"

    # room photo sonini aniqlash
    @api.depends("room_photos")
    def _compute_related_count(self):
        for record in self:
            record.photo_count = len(record.room_photos)

    @api.onchange("area")
    def _onchange_area(self):
        if self.area == "same":
            # Hide the area_max_value field or set it to a default/empty value
            self.area_max_value = False
        else:
            # Show the area_max_value field for user input
            pass

    @api.constrains("room_photos")
    def _check_room_photos_limit(self):
        for record in self:
            _logger.info(
                "Constraint check for record %s with %s photos",
                record.id,
                len(record.room_photos),
            )
            if len(record.room_photos) > 30:
                raise ValidationError("You can only add up to 30 photos.")

    # Hozircha faqat create bo'layapti.
    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._create_icon_no_records()

        # DefaultAvailability modeliga yozuv qo'shish
        default_availability = self.env["default.availability"].search([], limit=1)
        if not default_availability:
            default_availability = self.env["default.availability"].create({})

        self.env["availability.default_data"].create(
            {
                "room_type": record.id,
                "number": 0,
                "default_availability_id": default_availability.id,
            }
        )

        for i in range(1, 8):
            self.env["room_type.guests"].create(
                {
                    "guest_number": str(i),
                    "room_type": record.id,
                }
            )

        return record

    def write(self, vals):
        result = super().write(vals)
        self._create_icon_no_records()
        return result

    def unlink(self):
        for record in self:
            default_data_records = self.env["availability.default_data"].search(
                [("room_type", "=", record.id)]
            )
            default_data_records.unlink()

            # `Guests` yozuvlarini o'chirish
            guest_records = self.env["room_type.guests"].search(
                [("room_type", "=", record.id)]
            )
            guest_records.unlink()

        return super().unlink()

    def _create_icon_no_records(self):
        icon_no_model = self.env["icon_no"]

        for record in self:
            # Create records for video_and_audio
            for item in record.video_and_audio:
                icon_no_model.create({"name": item.name, "icon": item.icon})
            # Create records for electronic_devices
            for item in record.electronic_devices:
                icon_no_model.create({"name": item.name, "icon": item.icon})
            # Create records for bathroom
            for item in record.bathroom:
                icon_no_model.create({"name": item.name, "icon": item.icon})
            # Create records for outdoor_area_and_window_view
            for item in record.outdoor_area_and_window_view:
                icon_no_model.create({"name": item.name, "icon": item.icon})
            # Create records for internet_and_telephony
            for item in record.internet_and_telephony:
                icon_no_model.create({"name": item.name, "icon": item.icon})
            # Create records for furniture
            for item in record.furniture:
                icon_no_model.create({"name": item.name, "icon": item.icon})
            # Create records for others
            for item in record.others:
                icon_no_model.create({"name": item.name, "icon": item.icon})


class ChildAgeRange(models.Model):
    _name = "child.age.range"
    _description = "Child Age Range"

    name = fields.Char()
    age_from = fields.Integer(string="Age From", required=True, default=0)
    age_to = fields.Integer(string="Age To", required=True, default=2)
    room_type = fields.Many2one("triple", string="Room Type")
    company_id = fields.Many2one("res.company", string="Company", required=True)

    @api.model
    def create(self, vals):
        # age_from va age_to ni name fieldiga moslashtirish
        vals["name"] = f"child ({vals.get('age_from', 0)} - {vals.get('age_to', 2)})"
        return super().create(vals)

    def write(self, vals):
        # age_from va age_to yangilanganda name fieldini ham moslashtirish
        for record in self:
            age_from = vals.get("age_from", record.age_from)
            age_to = vals.get("age_to", record.age_to)
            vals["name"] = f"child ({age_from} - {age_to})"
        return super().write(vals)


class Guests(models.Model):
    """
    Room Types > Guest information
    Avval Guest yaratib olinadi keyin Room Types o'ziga bog'langan Guestlarni olib ishlatishi mumkin.
    """

    _name = "room_type.guests"
    _description = "Room Types > Guests"

    name = fields.Char(string="Name", compute="_compute_name", store=True)
    guest_number = fields.Selection(
        [(str(i), str(i)) for i in range(8)], string="Guest Number", required=True
    )
    room_type = fields.Many2one("triple", string="Room Type")

    @api.depends("guest_number")
    def _compute_name(self):
        for record in self:
            if record.guest_number:
                record.name = f"{record.guest_number}-guest(s)"
