from odoo import models, fields


class Station(models.Model):
    _name = "station"
    _description = "Station"

    name = fields.Char(string="Name")
    transfer_type_id = fields.Many2one("transfer.type", string="Transfer Type")
