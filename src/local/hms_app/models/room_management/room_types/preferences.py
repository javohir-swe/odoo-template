from odoo import models, fields


class SmokingInRoom(models.Model):
    _name = "smoking_in_room"
    _description = "Smoking In Room"

    name = fields.Char(required=True)
