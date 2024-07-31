# -*- coding: utf-8 -*-

from odoo import models, fields, api


class room_types(models.Model):
    _name = 'room_types.room_types'
    _description = 'room_types.room_types'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
