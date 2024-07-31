from odoo import fields, models


class Vehicles(models.Model):
    _name = "vehicles"
    _description = "Vehicles Information"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    capacity = fields.Integer(string="Capacity")
    usd = fields.Integer(string="Price in USD")
    uzs = fields.Integer(string="Price in UZS")
    rub = fields.Integer(string="Price in RUB")
