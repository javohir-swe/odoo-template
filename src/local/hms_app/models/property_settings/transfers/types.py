from odoo import models, fields


class TransferType(models.Model):
    _name = "transfer.type"
    _description = "Type of Transfer"

    name = fields.Char(string="Name")
