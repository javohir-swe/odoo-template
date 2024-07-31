from datetime import timedelta

from odoo import api, fields, models


class MailList(models.Model):
    _name = "mail.list"
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
    welcome_mail = fields.Many2one("welcome_mail", string="Welcome Mail")

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
    feedback_mail = fields.Many2one("feedback_mail", string="Feedback Mail")

    # ig -> incomplete booking for a guest
    ig_booking_engine = fields.Boolean(string="Booking Engine", default=True)
    ig_send_to_guest = fields.Char(
        string="Send to the Guest", compute="_compute_incomplete_booking_guest"
    )
    incomplete_booking_guest = fields.Many2one(
        "incomplete_booking_mail_for_guest", string="Incomplete booking for guest"
    )

    # ip -> incomplete booking for property
    ip_booking_engine = fields.Boolean(string="Booking Engine")
    ip_mail_copies = fields.Char(string="Mail Copies")
    ip_send_to_guest = fields.Char(
        string="Send to the Property", compute="_compute_incomplete_booking_property"
    )
    incomplete_booking_property = fields.Many2one(
        "incomplete_booking.mail", string="Incomplete booking for property"
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

        # Agar welcome_mail maydoniga qiymat berilmagan bo'lsa
        if "welcome_mail" not in vals or not vals["welcome_mail"]:
            welcome_mail = self.env["welcome_mail"].search([], limit=1)
            if welcome_mail:
                vals["welcome_mail"] = welcome_mail.id

        # Agar feedback_mail maydoniga qiymat berilmagan bo'lsa
        if "feedback_mail" not in vals or not vals["feedback_mail"]:
            feedback_mail = self.env["feedback_mail"].search([], limit=1)
            if feedback_mail:
                vals["feedback_mail"] = feedback_mail.id

        # Agar incomplete_booking_guest maydoniga qiymat berilmagan bo'lsa
        if (
            "incomplete_booking_guest" not in vals
            or not vals["incomplete_booking_guest"]
        ):
            incomplete_booking_guest = self.env[
                "incomplete_booking_mail_for_guest"
            ].search([], limit=1)
            if incomplete_booking_guest:
                vals["incomplete_booking_guest"] = incomplete_booking_guest.id

        # Agar incomplete_booking_property maydoniga qiymat berilmagan bo'lsa
        if (
            "incomplete_booking_property" not in vals
            or not vals["incomplete_booking_property"]
        ):
            incomplete_booking_property = self.env["incomplete_booking.mail"].search(
                [], limit=1
            )
            if incomplete_booking_property:
                vals["incomplete_booking_property"] = incomplete_booking_property.id

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

    def send_welcome_mails_today_checkins(self):
        record = self.env["mail.list"].search([], limit=1)
        today = fields.Date.today()
        days_before_checkin = int(record.wm_send_to_guest)
        target_date = today + timedelta(days=days_before_checkin)
        today_checkins = self.env["booking"].search(
            [
                ("check_in_date", "=", target_date),
                ("is_front_desk_booking", "=", "front_desk"),
            ]
        )
        for booking in today_checkins:
            if booking.guest_id.email:
                self.welcome_mail.send_mail(booking.id)
                print("test mail")

    def send_feedback_mail_for_departures(self):
        record = self.env["mail.list"].search([], limit=1)
        today = fields.Date.today()
        days_after_checkout = int(record.fb_send_to_guest)
        print(days_after_checkout)
        target_date = today - timedelta(days=days_after_checkout)
        print(target_date)
        recent_checkouts = self.env["booking"].search(
            [
                ("check_out_date", "=", target_date),
                ("is_front_desk_booking", "=", "front_desk"),
            ]
        )
        print("ishlayapman")
        print(recent_checkouts)
        for booking in recent_checkouts:
            if booking.guest_id.email:
                self.feedback_mail.send_mail(booking.guest_id.email)
                print("test mail")


class IrCron(models.Model):
    _inherit = "ir.cron"

    @api.model
    def _create_cron_send_welcome_mails(self):
        print("test cron")
        if not self.search([("name", "=", "Send Welcome Mails for Today Check-ins")]):
            self.create(
                {
                    "name": "Send Welcome Mails for Today Check-ins",
                    "model_id": self.env.ref("hms_app.model_mail_list").id,
                    "state": "code",
                    "code": "model.send_welcome_mails_today_checkins()",
                    "interval_type": "days",
                    "interval_number": 1,
                    "numbercall": -1,
                    "doall": False,
                    "active": True,
                }
            )

    @api.model
    def _create_cron_send_feedback_mails(self):
        print("test cron")
        if not self.search([("name", "=", "Send Feedback Mails for Departures")]):
            self.create(
                {
                    "name": "Send Feedback Mails for Departures",
                    "model_id": self.env.ref("hms_app.model_mail_list").id,
                    "state": "code",
                    "code": "model.send_feedback_mail_for_departures()",
                    "interval_type": "days",
                    "interval_number": 1,
                    "numbercall": -1,
                    "doall": False,
                    "active": True,
                }
            )

    @api.model
    def init(self):
        if self.env.ref("hms_app.model_mail_list", raise_if_not_found=False):
            self._create_cron_send_welcome_mails()
            self._create_cron_send_feedback_mails()
