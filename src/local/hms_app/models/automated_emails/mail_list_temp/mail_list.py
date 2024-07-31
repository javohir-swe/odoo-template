from odoo import api, fields, models


class MailList(models.Model):
    _name = "mail_list.temp"
    _description = "Mail List"

    name = fields.Char(string="Name", default="Mail List")
    # wm -> welcome mail
    wm_booking_engine = fields.Boolean(string="Booking Engine")
    wm_channel_manager = fields.Boolean(string="Channel Manager")
    wm_channel_manager_send_cancellation = fields.Boolean(
        string="Channel Manager Send Cancellation"
    )
    wm_front_desk = fields.Boolean(string="Front Desk")
    wm_send_to_guest = fields.Selection(
        [(str(i), str(i)) for i in range(1, 11)],
        string="Send to the Guest",
        default="1",
    )
    wm_mail_copies = fields.Char(string="Mail Copies")
    welcome_mail = fields.Char(string="Welcome Email", default="Welcome Mail")

    # fb -> feedback mail
    fb_booking_engine = fields.Boolean(string="Booking Engine")
    fb_channel_manager = fields.Boolean(string="Channel Manager")
    fb_front_desk = fields.Boolean(string="Front Desk")
    fb_send_to_guest = fields.Selection(
        [(str(i), str(i)) for i in range(1, 11)],
        string="Send to the Guest",
        default="1",
    )
    fb_mail_copies = fields.Char(string="Mail Copies")
    feedback_mail = fields.Char(
        string="Feedback Mail",
        default="Feedback Mail",
    )

    # ig -> incomplete booking for a guest
    ig_booking_engine = fields.Boolean(string="Booking Engine", default=True)
    ig_send_to_guest = fields.Char(
        string="Send to the Guest", compute="_compute_incomplete_booking_guest"
    )
    incomplete_booking_guest = fields.Char(
        string="Incomplete booking for guest",
        default="Incomplete booking for guest",
    )

    # ip -> incomplete booking for property
    ip_booking_engine = fields.Boolean(string="Booking Engine")
    ip_mail_copies = fields.Char(string="Mail Copies")
    ip_send_to_guest = fields.Char(
        string="Send to the Property", compute="_compute_incomplete_booking_property"
    )
    incomplete_booking_property = fields.Char(
        string="Incomplete booking for property",
        default="Incomplete booking for property",
    )

    @api.depends("ig_send_to_guest")
    def _compute_incomplete_booking_guest(self):
        for mail in self:
            mail.ig_send_to_guest = "instantly (enabled by default)"

    @api.depends("ip_send_to_guest")
    def _compute_incomplete_booking_property(self):
        for mail in self:
            mail.ip_send_to_guest = "instantly"

    @api.model
    def create(self, vals):
        record = self.search([], limit=1)
        if record:
            record.write(vals)
            return record
        return super().create(vals)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        record = self.search([], limit=1)
        if record:
            res.update(
                {
                    "wm_booking_engine": record.wm_booking_engine,
                    "wm_channel_manager": record.wm_channel_manager,
                    "wm_channel_manager_send_cancellation": record.wm_channel_manager_send_cancellation,
                    "wm_front_desk": record.wm_front_desk,
                    "wm_send_to_guest": record.wm_send_to_guest,
                    "wm_mail_copies": record.wm_mail_copies,
                    "welcome_mail": record.welcome_mail,
                    "fb_booking_engine": record.fb_booking_engine,
                    "fb_channel_manager": record.fb_channel_manager,
                    "fb_front_desk": record.fb_front_desk,
                    "fb_send_to_guest": record.fb_send_to_guest,
                    "fb_mail_copies": record.fb_mail_copies,
                    "feedback_mail": record.feedback_mail,
                    "ig_booking_engine": record.ig_booking_engine,
                    "ig_send_to_guest": record.ig_send_to_guest,
                    "incomplete_booking_guest": record.incomplete_booking_guest,
                    "ip_booking_engine": record.ip_booking_engine,
                    "ip_mail_copies": record.ip_mail_copies,
                    "ip_send_to_guest": record.ip_send_to_guest,
                    "incomplete_booking_property": record.incomplete_booking_property,
                }
            )
        return res
