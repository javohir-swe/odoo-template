from datetime import datetime, timedelta

from odoo import SUPERUSER_ID, api, fields, models
from odoo.exceptions import ValidationError


class DefaultData(models.Model):
    _name = "availability.default_data"
    _description = "Default Data"
    _rec_name = "number"

    room_type = fields.Many2one("triple", string="Room type")
    number = fields.Integer(string="Number")
    default_availability_id = fields.Many2one(
        "default.availability", string="Default Availability"
    )

    @api.model
    def create(self, vals):
        if "number" in vals and vals["number"] < 0:
            vals["number"] = 0
        return super().create(vals)

    def write(self, vals):
        if "number" in vals and vals["number"] < 0:
            vals["number"] = 0
        return super().write(vals)

    @api.model
    def _check_number(self, vals):
        if "number" in vals and vals["number"] < 0:
            vals["number"] = 0

        return vals


class DefaultAvailability(models.Model):
    _name = "default.availability"
    _description = "Default Availability"

    default_data = fields.One2many(
        "availability.default_data", "default_availability_id", string="Default Data"
    )

    @api.model
    def create(self, vals):
        existing_record = self.search([], limit=1)
        if existing_record:
            existing_record.write(vals)  # Update the existing record
            return existing_record
        return super().create(vals)

    @api.constrains("default_data")
    def _check_default_data_count(self):
        room_types = self.env["triple"].search([])
        if len(self.default_data) > len(room_types):
            raise ValidationError(
                "Default data record count cannot exceed the number of room types."
            )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        record = self.search([], limit=1)
        if record:
            res.update({"default_data": [(6, 0, record.default_data.ids)]})
        return res

    def write(self, vals):
        res = super().write(vals)
        # Ensure default_data entries are synchronized with room_types
        self._synchronize_default_data()

        # Update MainAvailability records based on the new default values
        self._update_main_availability()
        return res

    def _synchronize_default_data(self):
        room_types = self.env["triple"].search([])
        existing_room_types = self.default_data.mapped("room_type")
        for room_type in room_types - existing_room_types:
            self.env["availability.default_data"].create(
                {
                    "room_type": room_type.id,
                    "number": 0,
                    "default_availability_id": self.id,
                }
            )

    def _update_main_availability(self):
        for default_data in self.default_data:
            main_availabilities = self.env["main.availability"].search(
                [("room_type", "=", default_data.room_type.id)]
            )
            for availability in main_availabilities:
                availability.default = default_data.number
                availability.online = min(availability.front_desk, default_data.number)

    @api.model
    def get_all_default_data_fields(self, default_availability_id):
        record = self.browse(default_availability_id)
        result = {}  # Qaytarilayotgan result faqat id ni olishi kerak

        result["default_data"] = []
        for data in record.default_data:
            data_fields = data.read(["id", "room_type", "number"])
            # data_fields["room_type"] = data.room_type.read(["id", "name"])[0]
            result["default_data"].append(data_fields)
        print(result)
        return result


class MainAvailability(models.Model):
    _name = "main.availability"
    _description = "Main Availability"

    room_type = fields.Many2one("triple", string="Room type")
    close_open = fields.Boolean(string="Close Open", default=True)
    front_desk = fields.Integer(string="Front Desk availability")
    default = fields.Integer(string="Default availability")
    online = fields.Integer(string="Online availability")
    bookings = fields.Integer(
        "Bookings"
    )  # Booking qo'shilganida front_desk va default dan minus bo'lishi kerak.
    cancellations = fields.Integer("Cancellations")
    date = fields.Date("Date", default=fields.Date.today)

    @api.model
    def create_new_availability(self):
        room_types = self.env["triple"].search([])

        default_availability = self.env["default.availability"].search([], limit=1)

        for room_type in room_types:
            front_desk_count = self.env["room.inventory"].search_count(
                [("room_type", "=", room_type.id)]
            )

            default_value = 0
            if default_availability:
                default_data_record = default_availability.default_data.filtered(
                    lambda d: d.room_type.id == room_type.id
                )
                if default_data_record:
                    default_value = default_data_record[0].number

            online = min(front_desk_count, default_value)

            new_record_vals = {
                "close_open": True,
                "front_desk": front_desk_count,
                "default": default_value,
                "online": online,
                "room_type": room_type.id,
                "date": fields.Date.today(),  # Hozirgi sanani qo'shamiz
            }
            self.create(new_record_vals)

    def write(self, vals):
        for record in self:
            old_bookings = record.bookings or 0
            old_cancellations = record.cancellations or 0

            new_bookings = vals.get("bookings", old_bookings)
            new_cancellations = vals.get("cancellations", old_cancellations)

            bookings_diff = new_bookings - old_bookings
            cancellations_diff = new_cancellations - old_cancellations

            # bookings bo'lganda front_desk va default dan 1 birlikka minus qilish
            if bookings_diff > 0:
                record.front_desk -= 1
                record.default -= 1

            # cancellations bo'lganda front_desk va default ga 1 birlikka qo'shish
            if cancellations_diff > 0:
                record.front_desk += 1
                record.default += 1

            # Update online availability
            if bookings_diff != 0 or cancellations_diff != 0:
                vals["front_desk"] = record.front_desk
                vals["default"] = record.default
                vals["online"] = min(record.front_desk, record.default)

        res = super().write(vals)
        return res

    @api.model
    def create(self, vals):
        if "front_desk" in vals and "default" in vals:
            vals["online"] = min(vals["front_desk"], vals["default"])
        if "date" not in vals:
            vals[
                "date"
            ] = (
                fields.Date.today()
            )  # Agar sana berilmagan bo'lsa, hozirgi sanani qo'shish

        # Sanaga ko'ra mavjud yozuvni tekshirish
        existing_record = self.search(
            [("date", "=", vals["date"]), ("room_type", "=", vals["room_type"])],
            limit=1,
        )
        if existing_record:
            # Mavjud yozuvni yangilash
            existing_record.write(vals)
            return existing_record

        return super().create(vals)

    @api.model
    def _check_negative_values(self, vals):
        if "front_desk" in vals and vals["front_desk"] < 0:
            vals["front_desk"] = 0
        if "default" in vals and vals["default"] < 0:
            vals["default"] = 0
        if "online" in vals and vals["online"] < 0:
            vals["online"] = 0
        return vals


# ir.cron modeliga cron job qo'shish
class IrCron(models.Model):
    _inherit = "ir.cron"

    @api.model
    def _create_main_availability_cron(self):
        self.create(
            {
                "name": "Create Main Availability Every Minute",
                "model_id": self.env.ref("hms_app.model_main_availability").id,
                "state": "code",
                "code": "model.create_new_availability()",
                "user_id": self.env.user.id,
                "interval_number": 1,
                "interval_type": "minutes",
                "nextcall": datetime.now() + timedelta(minutes=1),
                "numbercall": -1,
            }
        )


def _register_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["ir.cron"]._create_main_availability_cron()


def pre_init_hook(cr):
    pass


def post_init_hook(cr, registry):
    _register_hook(cr, registry)


def uninstall_hook(cr, registry):
    pass


class AvailabilityManager(models.Model):
    _name = "availability.manager"
    _description = "Availability Manager"

    start_date = fields.Date(string="Start Date", required=True)
    stop_date = fields.Date(string="Stop Date", required=True)

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record.create_new_availability()
        return record

    def create_new_availability(self):
        room_types = self.env["triple"].search([])
        default_availability = self.env["default.availability"].search([], limit=1)

        for room_type in room_types:
            front_desk_count = self.env["room.inventory"].search_count(
                [("room_type", "=", room_type.id)]
            )

            default_value = 0
            if default_availability:
                default_data_record = default_availability.default_data.filtered(
                    lambda d: d.room_type.id == room_type.id
                )
                if default_data_record:
                    default_value = default_data_record[0].number

            online = min(front_desk_count, default_value)

            current_date = fields.Date.from_string(self.start_date)
            end_date = fields.Date.from_string(self.stop_date)

            while current_date <= end_date:
                new_record_vals = {
                    # "close_open": True,
                    "front_desk": front_desk_count,
                    "default": default_value,
                    "online": online,
                    "room_type": room_type.id,
                    "date": current_date,
                }
                self.env["main.availability"].create(new_record_vals)
                current_date += timedelta(days=1)
