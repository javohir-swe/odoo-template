from odoo import models, fields, api


class CloseData(models.Model):
    """Close uchun kerakli ma'lumotlar shu modelda saqlanadi."""

    _name = "close"
    _description = "Calendar Data for Guests"
    _rec_name = "open_close"

    date = fields.Date(
        required=True,
        default=lambda self: self._context_today(),  # Default value function
    )
    room_type_id = fields.Many2one("triple", string="Room Types", readonly=False)
    #
    child_aged_from_price = fields.Char("Child (0-2)")
    single_room_price = fields.Char(string="Single Room Price")
    double_room_price = fields.Char(string="Souble Room Price")
    triple_room_price = fields.Char(string="Sriple Room Price")
    fourth_room_price = fields.Char(string="Sourth Room Price")
    fifth_room_price = fields.Char(string="Sifth Room Price")
    sixth_room_price = fields.Char(string="Sixth Room Price")
    seventh_room_price = fields.Char(string="Seventh Room Price")
    #
    open_close = fields.Boolean(store=True, readonly=False)
    status_display = fields.Char(compute="_compute_status_display", string="Status")
    tag_names = fields.Char(compute="_get_tag_names")

    # Assuming you need to compute some tag names based on other fields
    @api.depends(
        "child_aged_from_price", "single_room_price"
    )  # Depend on actual fields
    def _get_tag_names(self):
        for record in self:
            # Compute tag names based on some logic
            # This is just an example, replace with your actual logic
            tags = []
            if record.child_aged_from_price:
                tags.append("Child Price")
            if record.single_room_price:
                tags.append("Single Room")
            record.tag_names = ", ".join(tags)

    @api.model
    def _context_today(self):
        return fields.Date.context_today(self)  # Helper to set default date

    @api.depends("open_close")
    def _compute_status_display(self):
        for record in self:
            record.status_display = "open" if record.open_close else "close"

    def name_get(self):
        res = []
        for record in self:
            # Here, we use the value of `status_display` for the name
            name = record.status_display or ""
            res.append((record.id, name))
        return res


# class Guests(models.Model):
#     _name = "guests"
#     _description = "Guests information"

#     name = fields.Char(required=True)
#     room_type_ids = fields.Many2many(
#         "triple",
#         "guest_triple_rel",
#         "guest_id",
#         "triple_id",
#         string="Room Types",
#     )
