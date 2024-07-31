import uuid

from odoo import api, fields, models


class BuildingFloor(models.Model):
    _name = "building.floor"
    _description = "Building Floor"
    _rec_name = "number"

    number = fields.Char(string="Floor Number", required=True)
    building_id = fields.Many2one(
        "property.building", string="Building", required=True, ondelete="cascade"
    )


class PropertyBuildings(models.Model):
    _name = "property.building"
    _description = "Property Building"
    _rec_name = "building_name"

    building_name = fields.Char(string="Building Name", required=True)
    number_of_floor = fields.Integer(string="Number of Floors", required=True)
    floor_ids = fields.One2many("building.floor", "building_id", string="Floor Details")

    @api.onchange("number_of_floor")
    def _onchange_number_of_floor(self):
        if self.number_of_floor:
            self.floor_ids = [(5, 0, 0)]  # Clear existing floors
            floors = [(0, 0, {"number": i + 1}) for i in range(self.number_of_floor)]
            self.floor_ids = floors


class RoomInventory(models.Model):
    _name = "room.inventory"
    _description = "Room Inventory"
    _rec_name = "number"

    dates_of_stay_from = fields.Date(string="Dates of Stay From")
    dates_of_stay_to = fields.Date(string="Dates of Stay To")
    building_id = fields.Many2one(
        "property.building", string="Building", ondelete="cascade"
    )
    floor_id = fields.Many2one("building.floor", string="Floor", ondelete="cascade")
    room_type = fields.Many2one("triple", string="Room Type")
    beds_in_room = fields.Selection(
        [("not_set", "Not Set"), ("double", "Double"), ("twin", "Twin")],
        string="Beds in Room",
        default="not_set",
    )
    number = fields.Char(string="Room Number", required=True)
    ignore_in_statistics = fields.Boolean(string="Ignore in Statistics")
    comment = fields.Text(string="Comment")
    generate_id = fields.Many2one(
        "room_inventory.generate", string="Generate Reference"
    )
    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()))

    @api.model
    def create(self, vals):
        if "uuid" not in vals:
            vals["uuid"] = str(uuid.uuid4())
        room_inventory = super().create(vals)
        if not vals.get("generate_id"):
            self.create_housekeeping(room_inventory)
        return room_inventory

    def create_housekeeping(self, room_inventory):
        self.env["room_inventory.housekeeping"].create(
            {
                "building_id": room_inventory.building_id.id,
                "floor_id": room_inventory.floor_id.id,
                "room_type": room_inventory.room_type.id,
                "beds_in_room": room_inventory.beds_in_room,
                "number": room_inventory.number,
                "ignore_in_statistics": room_inventory.ignore_in_statistics,
                "comment": room_inventory.comment,
                "generate_id": room_inventory.generate_id.id,
                "uuid": room_inventory.uuid,
            }
        )

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            new_number = vals.get("number", record.number)
            housekeeping = self.env["room_inventory.housekeeping"].search(
                [("uuid", "=", record.uuid)]
            )
            if housekeeping:
                housekeeping_vals = {
                    "building_id": record.building_id.id
                    if "building_id" in vals
                    else housekeeping.building_id.id,
                    "floor_id": record.floor_id.id
                    if "floor_id" in vals
                    else housekeeping.floor_id.id,
                    "room_type": record.room_type.id
                    if "room_type" in vals
                    else housekeeping.room_type.id,
                    "beds_in_room": record.beds_in_room
                    if "beds_in_room" in vals
                    else housekeeping.beds_in_room,
                    "number": new_number,
                    "ignore_in_statistics": record.ignore_in_statistics
                    if "ignore_in_statistics" in vals
                    else housekeeping.ignore_in_statistics,
                    "comment": record.comment
                    if "comment" in vals
                    else housekeeping.comment,
                    "generate_id": record.generate_id.id
                    if "generate_id" in vals
                    else housekeeping.generate_id.id,
                }
                housekeeping.write(housekeeping_vals)
        return res

    def unlink(self):
        housekeeping_records = self.env["room_inventory.housekeeping"].search(
            [("uuid", "in", self.mapped("uuid"))]
        )
        housekeeping_records.unlink()
        return super().unlink()


class RoomInventoryGenerateWizard(models.Model):
    _name = "room_inventory.generate"
    _description = "Room Inventory Generate"

    building_id = fields.Many2one(
        "property.building", string="Building", ondelete="cascade", required=True
    )
    floor_id = fields.Many2one(
        "building.floor", string="Floor", ondelete="cascade", required=True
    )
    room_type = fields.Many2one("triple", string="Room Type")
    beds_in_room = fields.Selection(
        [("not_set", "Not Set"), ("double", "Double"), ("twin", "Twin")],
        string="Beds in Room",
        required=True,
    )
    number = fields.One2many(
        "room.inventory", "generate_id", string="Room Number", required=True
    )
    ignore_in_statistics = fields.Boolean(string="Ignore in Statistics")
    comment = fields.Text(string="Comment")

    def generate_room_inventory(self):
        for wizard in self:
            for room in wizard.number:
                room.write(
                    {
                        "building_id": wizard.building_id.id,
                        "floor_id": wizard.floor_id.id,
                        "room_type": wizard.room_type.id,
                        "beds_in_room": wizard.beds_in_room,
                        "ignore_in_statistics": wizard.ignore_in_statistics,
                        "comment": wizard.comment,
                    }
                )
                self.env["room_inventory.housekeeping"].create(
                    {
                        "building_id": wizard.building_id.id,
                        "floor_id": wizard.floor_id.id,
                        "room_type": wizard.room_type.id,
                        "beds_in_room": wizard.beds_in_room,
                        "number": room.number,
                        "ignore_in_statistics": wizard.ignore_in_statistics,
                        "comment": wizard.comment,
                        "generate_id": room.generate_id.id,
                        "uuid": room.uuid,
                    }
                )
            wizard.unlink()


class Housekeeping(models.Model):
    _name = "room_inventory.housekeeping"
    _description = "Housekeeping"

    building_id = fields.Many2one(
        "property.building", string="Building", ondelete="cascade"
    )
    floor_id = fields.Many2one("building.floor", string="Floor", ondelete="cascade")
    room_type = fields.Many2one("triple", string="Room Type")
    beds_in_room = fields.Selection(
        [("not_set", "Not Set"), ("double", "Double"), ("twin", "Twin")],
        string="Beds in Room",
    )
    number = fields.Char(string="Room Number", required=True)
    ignore_in_statistics = fields.Boolean(string="Ignore in Statistics")
    comment = fields.Text(string="Comment")
    generate_id = fields.Many2one(
        "room_inventory.generate", string="Generate Reference"
    )
    uuid = fields.Char(string="UUID", required=True)

    # for housekeeping
    occupancy = fields.Selection(
        [("band", "band"), ("bo'sh", "bo'sh")], string="Occupancy"
    )
    people_count = fields.Integer(string="Number of adults/children")
    room_will_be_vacant_from = fields.Datetime(string="Room will be vacant from")
    room_will_be_vacant_until = fields.Datetime(string="Room will be vacant until")
    room_will_be_occupied_from = fields.Datetime(string="Room will be occupied from")
    room_will_be_occupied_until = fields.Datetime(string="Room will be occupied until")
    status = fields.Selection(
        [
            ("need_to_clean", "Need to Clean"),
            ("clean", "Clean"),
            ("checked", "Checked"),
            ("out_of_order", "Out of Order"),
        ],
        string="Status",
        default="clean",
    )

    out_of_order_ids = fields.One2many(
        "room_inventory.out_of_order", "housekeeping_id", string="Out Of Order"
    )

    is_out_of_order = fields.Boolean(
        string="Is Out of Order", compute="_compute_is_out_of_order"
    )

    out_of_order_period = fields.Char(
        string="Out of Order", compute="_compute_out_of_order_period"
    )

    room_will_be_vacant_period = fields.Char(
        string="Room will be vacant", compute="_compute_room_will_be_vacant"
    )
    room_will_be_occupied_period = fields.Char(
        string="Room will be occupied", compute="_compute_room_will_be_occupied"
    )

    @api.depends("room_will_be_vacant_from", "room_will_be_vacant_until")
    def _compute_room_will_be_vacant(self):
        for record in self:
            if record.room_will_be_vacant_from and record.room_will_be_vacant_until:
                from_dt = fields.Datetime.to_datetime(record.room_will_be_vacant_from)
                until_dt = fields.Datetime.to_datetime(record.room_will_be_vacant_until)
                record.room_will_be_vacant_period = "{} / {} - {} / {}".format(
                    from_dt.strftime("%d.%m.%Y"),
                    from_dt.strftime("%H:%M"),
                    until_dt.strftime("%d.%m.%Y"),
                    until_dt.strftime("%H:%M"),
                )
            else:
                record.room_will_be_vacant_period = ""

    @api.depends("room_will_be_occupied_from", "room_will_be_occupied_until")
    def _compute_room_will_be_occupied(self):
        for record in self:
            if record.room_will_be_occupied_from and record.room_will_be_occupied_until:
                from_dt = fields.Datetime.to_datetime(record.room_will_be_occupied_from)
                until_dt = fields.Datetime.to_datetime(
                    record.room_will_be_occupied_until
                )
                record.room_will_be_occupied_period = "{} / {} - {} / {}".format(
                    from_dt.strftime("%d.%m.%Y"),
                    from_dt.strftime("%H:%M"),
                    until_dt.strftime("%d.%m.%Y"),
                    until_dt.strftime("%H:%M"),
                )
            else:
                record.room_will_be_occupied_period = ""

    @api.depends(
        "out_of_order_ids.unavailable_from", "out_of_order_ids.unavailable_until"
    )
    def _compute_out_of_order_period(self):
        for record in self:
            periods = []
            for out_order in record.out_of_order_ids:
                if out_order.unavailable_from and out_order.unavailable_until:
                    from_dt = fields.Datetime.to_datetime(out_order.unavailable_from)
                    until_dt = fields.Datetime.to_datetime(out_order.unavailable_until)
                    period = "{} / {} - {} / {}".format(
                        from_dt.strftime("%d.%m.%Y"),
                        from_dt.strftime("%H:%M"),
                        until_dt.strftime("%d.%m.%Y"),
                        until_dt.strftime("%H:%M"),
                    )
                    periods.append(period)
            record.out_of_order_period = ", ".join(periods) if periods else ""

    @api.depends("status")
    def _compute_is_out_of_order(self):
        for record in self:
            record.is_out_of_order = record.status == "out_of_order"

    @api.model
    def get_rooms_by_type(self):
        records = self.search([])
        grouped_result = {}
        for record in records:
            room_type_name = record.room_type.rooms

            if room_type_name not in grouped_result:
                grouped_result[room_type_name] = {"count": 0, "rooms": []}

            grouped_result[room_type_name]["count"] += 1
            status_label = dict(
                self.fields_get(allfields=["status"])["status"]["selection"]
            )[record.status]
            room_data = {
                "number": record.number,
                "status": status_label,
                "beds_in_room": record.beds_in_room,
                "room_type_id": record.room_type.id,
                "housekeeping_id": record.id,
            }

            grouped_result[room_type_name]["rooms"].append(room_data)

        result = []
        for room_type, data in grouped_result.items():
            result.append(
                {"room_type": room_type, "count": data["count"], "rooms": data["rooms"]}
            )

        return result


class OutOfOrder(models.Model):
    _name = "room_inventory.out_of_order"
    _description = "Room Inventory Out Of Order"

    works = fields.Char(string="Works")
    description = fields.Text(string="Description")
    unavailable_from = fields.Datetime(string="Unavailable for accommodation from")
    unavailable_until = fields.Datetime(string="Unavailable for accommodation until")
    housekeeping_id = fields.Many2one(
        "room_inventory.housekeeping",
        string="Housekeeping",
        required=True,
        ondelete="cascade",
    )

    @api.model
    def name_get(self):
        res = []
        for record in self:
            name = f"{record.unavailable_from} - {record.unavailable_until}"
            res.append((record.id, name))
        return res
