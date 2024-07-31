from odoo import api, fields, models


class AvailabilityRoomType(models.Model):
    _name = "availability.room_type"
    _description = "Room type"

    room_type_id = fields.Many2one(
        "triple",
        string="Room type",
        required=True,
    )
    number = fields.Integer(string="Last rooms", required=True)
    online_sales_id = fields.Many2one(
        "availability.online_sales_role", string="Online sales"
    )


class OnlineSalesRole(models.Model):
    _name = "availability.online_sales_role"
    _description = "Online sales"

    name = fields.Char(string="Internal name", required=True)
    mark_on = fields.Integer(string="Mark on the calendar", required=True)
    room_types = fields.One2many(
        "availability.room_type", "online_sales_id", string="Room types"
    )
    number_of_days = fields.Selection(
        [
            ("dont_return", "Do not return"),
            ("arrival", "0, An arrival day"),
            ("other", "Other"),
        ],
        string="Number of days",
        default="dont_return",
    )
    days_checkin = fields.Integer(string="Days before check-in")

    @api.onchange("number_of_days")
    def _onchange_number_of_days(self):
        if self.number_of_days and self.number_of_days != "other":
            self.days_checkin = 0

    @api.model
    def create(self, vals):
        if vals.get("number_of_days") and vals["number_of_days"] != "other":
            vals["days_checkin"] = 0

        # Get the current count of OnlineSalesRole records
        current_count = self.search_count([])
        vals["mark_on"] = current_count + 1

        return super().create(vals)

    def write(self, vals):
        if "number_of_days" in vals and vals["number_of_days"] != "other":
            vals["days_checkin"] = 0
        return super().write(vals)

    @api.model
    def get_all_data(self):
        roles = self.search([])
        data = []
        number_of_days_dict = {
            "dont_return": "Do not return",
            "arrival": "0, An arrival day",
            "other": "Other",
        }
        for role in roles:
            role_data = {
                "id": role.id,
                "name": role.name,
                "mark_on": role.mark_on,
                "room_types": [
                    {
                        "id": room_type.room_type_id.id,
                        "rooms": room_type.room_type_id.rooms,
                        "number": room_type.number,
                    }
                    for room_type in role.room_types
                ],
                "number_of_days": number_of_days_dict.get(
                    role.number_of_days, role.number_of_days
                ),
                "days_checkin": role.days_checkin,
            }
            data.append(role_data)
        return data
