from odoo import api, fields, models


class References(models.Model):
    _name = "references"
    _description = "References"
    _rec_name = "reference_name"

    reference_name = fields.Char(string="Reference")
    default_element = fields.Char(string="Default Element")
    number_of_elements = fields.Integer(
        string="Number of Elements", compute="_compute_number_of_elements"
    )
    date_last_modified = fields.Datetime(string="Last Modified")
    modified_by_user_id = fields.Many2one(
        "res.users", required=True, default=lambda self: self.env.user, string="User"
    )
    settings_id = fields.Many2one("settings", string="Settings")
    element_id = fields.Many2many("references.element", string="Element")

    @api.depends("element_id")
    def _compute_number_of_elements(self):
        for record in self:
            record.number_of_elements = len(record.element_id)


class ReferencesElement(models.Model):
    _name = "references.element"
    _description = "References"

    name = fields.Char(string="Name")
    comment = fields.Text(string="Comment")
    element_date_last_modified = fields.Datetime(string="Last Modified")
    element_modified_by_user_id = fields.Many2one(
        "res.users", required=True, default=lambda self: self.env.user, string="User"
    )
    element_status = fields.Selection(
        [("active", "Active"), ("in_active", "In active")], default="active"
    )


class SettingsPointOfSale(models.Model):
    _name = "settings.pointofsale"
    _description = "Settings Point of Sale"

    element_name = fields.Char(string="Element Name", required=True)
    comment = fields.Text(string="Comment")
    datelast_modified = fields.Datetime(
        string="Date Last Modified", default=fields.Datetime.now
    )
    status = fields.Boolean(string="Status", default=True)
    set_default = fields.Boolean(
        string="Set as Default", help="Set as default element in 'Point of sale'"
    )
    settings_id = fields.Many2one("settings", string="Settings")


class PurposeOfVisit(models.Model):
    _name = "purpose.ofvisit"
    _description = "Purpose of Visit"

    element_name = fields.Char(string="Element Name", required=True)
    comment = fields.Text(string="Comment")
    datelast_modified = fields.Datetime(
        string="Date Last Modified", default=fields.Datetime.now
    )
    status = fields.Boolean(string="Status", default=True)
    set_default = fields.Boolean(
        string="Set as Default", help="Set as default element in 'Point of sale'"
    )
    settings_id = fields.Many2one("settings", string="Settings")


class Tag(models.Model):
    _name = "tag"
    _description = "Tag"

    element_name = fields.Char(string="Element Name", required=True)
    comment = fields.Text(string="Comment")
    datelast_modified = fields.Datetime(
        string="Date Last Modified", default=fields.Datetime.now
    )
    status = fields.Boolean(string="Status", default=True)
    set_default = fields.Boolean(
        string="Set as Default", help="Set as default element in 'Point of sale'"
    )
    settings_id = fields.Many2one("settings", string="Settings")


class PaymentMethod(models.Model):
    _name = "payment.method"
    _description = "Payment Method"
    _rec_name = "element_name"

    element_name = fields.Char(string="Element Name", required=True)
    comment = fields.Text(string="Comment")
    datelast_modified = fields.Datetime(
        string="Date Last Modified", default=fields.Datetime.now
    )
    status = fields.Boolean(string="Status", default=True)
    set_default = fields.Boolean(
        string="Set as Default", help="Set as default element in 'Point of sale'"
    )
    settings_id = fields.Many2one("settings", string="Settings")


class MarketSegment(models.Model):
    _name = "market.segment"
    _description = "Market Segment"

    element_name = fields.Char(string="Element Name", required=True)
    comment = fields.Text(string="Comment")
    datelast_modified = fields.Datetime(
        string="Date Last Modified", default=fields.Datetime.now
    )
    status = fields.Boolean(string="Status", default=True)
    set_default = fields.Boolean(
        string="Set as Default", help="Set as default element in 'Point of sale'"
    )
    settings_id = fields.Many2one("settings", string="Settings")


class Staff(models.Model):
    _name = "staff"
    _description = "Staff"

    element_name = fields.Char(string="Element Name", required=True)
    comment = fields.Text(string="Comment")
    datelast_modified = fields.Datetime(
        string="Date Last Modified", default=fields.Datetime.now
    )
    status = fields.Boolean(string="Status", default=True)
    set_default = fields.Boolean(
        string="Set as Default", help="Set as default element in 'Point of sale'"
    )
    settings_id = fields.Many2one("settings", string="Settings")


class GuestStatus(models.Model):
    _name = "guest.status"
    _description = "Guest Status"

    element_name = fields.Char(string="Element Name", required=True)
    comment = fields.Text(string="Comment")
    datelast_modified = fields.Datetime(
        string="Date Last Modified", default=fields.Datetime.now
    )
    status = fields.Boolean(string="Status", default=True)
    set_default = fields.Boolean(
        string="Set as Default", help="Set as default element in 'Point of sale'"
    )
    settings_id = fields.Many2one("settings", string="Settings")


class NewTemplate(models.Model):
    _name = "new.template"
    _description = "New Template"

    status = fields.Boolean(string="Status", default=True)
    name = fields.Char(string="Name", required=True)
    room_type = fields.Char(string="Room Type")
    document_rules = fields.Char(string="Document Rules")
    document = fields.Binary(string="Document")
    document_name = fields.Char(string="Document Name")
    settings_id = fields.Many2one("settings", string="Settings")
