from odoo import api, fields, models


class Notes(models.Model):
    _name = "reception.notes"
    _description = "Notes"

    text = fields.Text("text", required=True)
    status = fields.Selection(
        [
            ("not_scheduled", "Not scheduled"),
            ("scheduled", "Scheduled"),
            ("done", "Done"),
        ],
        string="status",
        default="not_scheduled",
    )

    scheduled = fields.Datetime("Scheduled")
    schedul_for = fields.Datetime("Schedul for", default=fields.Datetime.now)
    reception_id = fields.Many2one("reception", string="reception")
    readonly_schedul_for = fields.Boolean(
        "Read only schedul_for",
        compute="_compute_readonly_schedul_for",
        store=True,
        default=True,
    )
    room_number = fields.Char(
        "room_number",
        compute="_compute_room_number",
    )
    user = fields.Char("User", compute="_compute_user", store=True)
    room_type_id = fields.Many2one(
        related="reception_id.room_type_id", string="Room Type", readonly=False
    )
    room_number_id = fields.Many2one(
        related="reception_id.room_number", string="Room Number", readonly=False
    )

    @api.depends("room_type_id", "room_number_id")
    def _compute_room_number(self):
        for record in self:
            if record.room_type_id and record.room_number_id:
                record.room_number = (
                    f"{record.room_number_id.number}, {record.room_type_id.rooms}"
                )
            else:
                record.room_number = ""

    @api.depends("status")
    def _compute_readonly_schedul_for(self):
        for record in self:
            record.readonly_schedul_for = record.status != "scheduled"

    @api.depends("create_uid", "write_uid")
    def _compute_user(self):
        for record in self:
            if record.write_uid:
                record.user = record.write_uid.email
            elif record.create_uid:
                record.user = record.create_uid.email
            else:
                record.user = ""
