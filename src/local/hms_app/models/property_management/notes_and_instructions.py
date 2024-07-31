from odoo import api, fields, models


class NotesAndInstructions(models.Model):
    _name = "notes_and_instructions"
    _description = "Notes and Instructions"
    _rec_name = "unique_id"

    booking_id = fields.Many2one(
        "booking",
        string="Booking",
        domain=[("status", "=", "done")],
    )
    reception_id = fields.Many2one(
        "reception",
        string="reception",
        compute="_compute_reception_id",
        store=True,
        index=True,  # Make the field searchable
    )
    unique_id = fields.Char(related="reception_id.unique_id", string="Booking Number")
    full_name = fields.Char(string="Full Name")
    created_changed_time = fields.Datetime(
        string="Created/Changed Time", compute="_compute_created_changed_time"
    )
    room_number_id = fields.Many2one(
        related="reception_id.room_number", string="Room Number"
    )
    room_type_id = fields.Many2one("triple", string="Room Type")
    text = fields.Text(string="Text", required=True)
    scheduled = fields.Datetime(string="Scheduled", default=fields.Datetime.now)
    user = fields.Many2one(
        "res.users", string="User", required=True, default=lambda self: self.env.user
    )
    status = fields.Selection(
        [
            ("not_scheduled", "Not scheduled"),
            ("scheduled", "Scheduled"),
            ("done", "Done"),
            ("overdue", "Overdue"),
        ],
        string="Status",
        default="not_scheduled",
    )
    readonly_schedul_for = fields.Boolean(
        "Read only schedul_for",
        compute="_compute_readonly_schedul_for",
        store=True,
        default=True,
    )

    # @api.depends("booking_id", "reception_id")
    # def _compute_room_number_id(self):
    #     for record in self:
    #         if record.booking_id:
    #             record.room_number_id = record.booking_id.room_number
    #
    #         if record.reception_id:
    #             record.room_type_id = record.reception_id.room_number

    # @api.depends("booking_id", "reception_id")
    # def _compute_unique_id(self):
    #     for record in self:
    #         if record.booking_id:
    #             record.unique_id = record.booking_id.unique_id
    #         if record.reception_id:
    #             record.unique_id = record.reception_id.unique_id

    # @api.depends("booking_id", "reception_id")
    # def _compute_room_type_id(self):
    #     for record in self:
    #         if record.booking_id:
    #             record.room_type_id = record.booking_id.room_type_id
    #         if record.reception_id:
    #             record.room_type_id = record.reception_id.room_type_id

    @api.depends("booking_id")
    def _compute_reception_id(self):
        for record in self:
            if record.booking_id:
                reception = self.env["reception"].search(
                    [("booking_id", "=", record.booking_id.id)], limit=1
                )
                record.reception_id = reception.id if reception else False

    @api.depends("create_date", "write_date")
    def _compute_created_changed_time(self):
        for record in self:
            record.created_changed_time = record.write_date or record.create_date

    @api.onchange("status")
    def _onchange_status(self):
        if self.status == "scheduled":
            self.scheduled = fields.Datetime.now()
        elif self.status != "scheduled":
            self.scheduled = False

    @api.model
    def create(self, vals):
        if vals.get("status") == "scheduled" and vals.get("scheduled"):
            scheduled_date = fields.Datetime.from_string(vals.get("scheduled"))
            if scheduled_date < fields.Datetime.now():
                vals["status"] = "overdue"
        res = super().create(vals)
        return res

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if record.status == "scheduled" and record.scheduled:
                scheduled_date = fields.Datetime.from_string(record.scheduled)
                if scheduled_date < fields.Datetime.now():
                    record.status = "overdue"
        return res

    @api.depends("status")
    def _compute_readonly_schedul_for(self):
        for record in self:
            record.readonly_schedul_for = record.status != "scheduled"

    def action_done(self):
        for record in self:
            record.status = "done"

    def action_edit(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Edit Note",
            "res_model": self._name,
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }
