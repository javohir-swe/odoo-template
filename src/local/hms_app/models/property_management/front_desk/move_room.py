from odoo import _, api, fields, models


class MoveRoom(models.Model):
    _name = "front_desk.move_room"
    _description = "Front Desk Move Room"

    booking_id = fields.Many2one("booking", string="Booking")
    booking_no = fields.Char(related="booking_id.unique_id", string="Booking No")
    old_accommodation_id = fields.Many2one(
        related="booking_id.accommodation", string="Old Accommodation"
    )
    room_number = fields.Many2one(
        related="booking_id.room_number", string="Room Number"
    )
    check_in_date = fields.Date(
        related="booking_id.check_in_date", string="Check In Date"
    )
    check_out_date = fields.Date(
        related="booking_id.check_out_date", string="Check Out Date"
    )
    prev_cost = fields.Float(
        related="booking_id.total",
        string="Previous Cost",
    )

    new_accommodation_id = fields.Many2one("accommodation", string="New Accommodation")
    new_room = fields.Many2one("room.inventory", string="New Room Number")
    new_check_in_date = fields.Date(
        default=fields.Date.context_today, string="New Check In Date"
    )
    new_check_out_date = fields.Date(
        related="booking_id.check_out_date", string="Check Out Date"
    )
    new_cost = fields.Float(string="New Cost", compute="_compute_new_cost")
    dont_charge = fields.Boolean(string="Do not change the cost of stay")
    charge_to_guest = fields.Float(
        string="Charge The Guest", compute="_compute_charge", store=True
    )
    charge_to_property = fields.Float(
        string="Charge The Property", compute="_compute_charge", store=True
    )
    available_room_ids = fields.Many2many(
        "room.inventory", compute="_compute_available_rooms", string="Available Rooms"
    )
    room_type = fields.Many2one(related="booking_id.room_type_id", string="Room Type")

    @api.depends("new_cost", "dont_charge", "prev_cost")
    def _compute_charge(self):
        for record in self:
            if not record.dont_charge:
                cost = record.prev_cost - record.new_cost
                if cost > 0:
                    record.charge_to_guest = cost
                    record.charge_to_property = 0.0
                else:
                    record.charge_to_property = -1 * cost
                    record.charge_to_guest = 0.0
            else:
                record.charge_to_guest = 0.0
                record.charge_to_property = 0.0

    @api.depends("new_accommodation_id", "new_check_in_date", "new_check_out_date")
    def _compute_new_cost(self):
        for record in self:
            if (
                record.new_accommodation_id
                and record.check_in_date
                and record.check_out_date
            ):
                room_price = record.new_accommodation_id.price

                old_price = record.old_accommodation_id.price

                lived_days = (record.check_in_date - record.new_check_in_date).days

                used_amount = lived_days * old_price

                days = (record.check_out_date - record.check_in_date).days

                record.new_cost = float(days * room_price) + used_amount

            else:
                record.new_cost = 0.0

    @api.onchange("new_accommodation_id")
    def _compute_available_rooms(self):
        for record in self:
            if not record.new_check_in_date or not record.new_check_out_date:
                record.available_room_ids = self.env["room.inventory"].search([]).ids
                continue

            if record.new_accommodation_id:
                conflicting_rooms = (
                    self.env["booking"]
                    .search(
                        [
                            ("check_in_date", "<", record.new_check_out_date),
                            ("check_out_date", ">", record.new_check_in_date),
                            ("id", "!=", record.booking_id.id),
                        ]
                    )
                    .mapped("room_number.id")
                )

                available_rooms = self.env["room.inventory"].search(
                    [
                        ("id", "not in", conflicting_rooms),
                        ("room_type", "=", record.new_accommodation_id.room_type.id),
                    ]
                )
                record.available_room_ids = available_rooms.ids
            else:
                record.available_room_ids = self.env["room.inventory"].search([]).ids

    def write(self, vals):
        for record in self:
            if (
                "new_accommodation_id" in vals
                or "new_room" in vals
                or "new_check_in_date" in vals
                or "new_check_out_date" in vals
            ):
                conflicting_bookings = self.env["booking"].search(
                    [
                        ("check_in_date", "<", record.new_check_out_date),
                        ("check_out_date", ">", record.new_check_in_date),
                        ("room_number", "=", vals.get("new_room", record.new_room.id)),
                        ("id", "!=", record.booking_id.id),
                    ]
                )
                if conflicting_bookings:
                    self.env.user.notify_warning(
                        message=_(
                            "The selected room is already booked for the chosen dates."
                        )
                    )
                    return False

        res = super().write(vals)
        for record in self:
            booking = record.booking_id
            booking.write(
                {
                    "is_moved_room": True,
                    "room_number": record.new_room.id,
                    "total": record.new_cost,
                    "accommodation": record.new_accommodation_id.id,
                    "room_type_id": record.new_room.room_type.id,
                    "booking_status": "moved",
                }
            )
        return res
