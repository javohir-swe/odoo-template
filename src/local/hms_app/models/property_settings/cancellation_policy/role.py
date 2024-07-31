from odoo import fields, models


class RuleName(models.Model):
    _name = "rule.name"
    _description = "Rule Name"

    name = fields.Char(string="Name", required=True)
    starting_from = fields.Selection(
        [
            ("check_in_time", "Check-in time"),
            ("check_out_time", "Check-out time"),
            ("check_in_time_guest", "Check-in time selected by guest"),
            ("selected_time", "Selected time"),
            ("booking_creation_time", "Booking creation time"),
        ],
        string="Starting From",
        default="check_in_time_guest",
        required=True,
    )
    # time = fields.Datetime(string="Time", required=True)
    description = fields.Text(string="Description")
    show_cancellation_terms = fields.Boolean(string="Show Cancellation Terms")
    cancellation_term_ids = fields.One2many(
        "cancellation.terms",
        "cancellation_policy",
        string="Cancellation Term",
        ondelete="restrict",
    )

    # Not neeed
    cancellation_term_id = fields.Many2one(
        "cancellation.terms", string="Cancellation Term", ondelete="restrict"
    )
