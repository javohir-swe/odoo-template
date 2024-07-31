from odoo import fields, models


class VideoAndAudio(models.Model):
    _name = "video_and_audio"
    _description = "Beds"

    name = fields.Char(required=True)
    icon = fields.Binary(required=True)


class ElectronicDevices(models.Model):
    _name = "electronic_devices"
    _description = "Beds"

    name = fields.Char(required=True)
    icon = fields.Binary(required=True)


class Bathroom(models.Model):
    _name = "bathroom"
    _description = "Beds"

    name = fields.Char(required=True)
    icon = fields.Binary(required=True)


class OutdoorAreaAndWindowView(models.Model):
    _name = "outdoor_area_and_window_view"
    _description = "Beds"

    name = fields.Char(required=True)
    icon = fields.Binary(required=True)


class InternetAndTelephony(models.Model):
    _name = "internet_and_telephony"
    _description = "Beds"

    name = fields.Char(required=True)
    icon = fields.Binary(required=True)


class Beds(models.Model):
    _name = "beds"
    _description = "Beds"

    name = fields.Char(required=True)
    icon = fields.Binary(required=True)


class Furniture(models.Model):
    _name = "furniture"
    _description = "Beds"

    name = fields.Char(required=True)
    icon = fields.Binary(required=True)


class Others(models.Model):
    _name = "others"
    _description = "Beds"

    name = fields.Char(required=True)
    icon = fields.Binary(required=True)


# class OutDoorAreaAndWindowView(models.Model):
#     _name = "outdoor_area_and_window_view"
#     _description = "Beds"

#     name = fields.Char(required=True)    icon = fields.Binary(required=True)
