from odoo import _, api, fields, models
from odoo.exceptions import UserError


class WelcomeMail(models.Model):
    _name = "welcome_mail"
    _description = "Welcome Mail"

    name = fields.Char(string="Name")
    email_from = fields.Char(string="From")
    subject = fields.Char(string="Subject")
    color = fields.Selection(
        [
            ("blue", "rgb(22, 96, 195)"),
            ("brown", "rgb(158, 122, 44)"),
            ("green", "rgb(64, 164, 40)"),
            ("gray", "rgb(75, 75, 75)"),
            ("purple", "rgb(116, 57, 147)"),
            ("red", "rgb(172, 31, 21)"),
            ("gold", "rgb(206, 139, 0)"),
            ("light_blue", "rgb(207, 228, 255)"),
            ("light_yellow", "rgb(232, 231, 203)"),
            ("light_green", "rgb(211, 248, 205)"),
            ("light_gray", "rgb(233, 233, 233)"),
            ("lavender", "rgb(228, 206, 253)"),
            ("pink", "rgb(253, 212, 206)"),
            ("peach", "rgb(250, 230, 167)"),
            ("light_gold", "rgb(236, 238, 241)"),
        ],
        string="Color",
        default="blue",
    )

    opening_note = fields.Html(string="Opening Note")
    include_opening_note = fields.Boolean(string="Include Opening Note", default=False)
    welcome_text = fields.Html(string="Welcome Text")
    include_welcome_text = fields.Boolean(string="Include Welcome text", default=False)
    booking_details = fields.Boolean(string="Booking Details")
    payment_methods_comments = fields.Boolean(string="Payment Methods and Comments")
    cancelation_terms = fields.Boolean(string="Cancelation Terms")
    outline = fields.Html(string="Outline")
    include_outline = fields.Boolean(string="Include Outline", default=False)

    result = fields.Html(string="Result", compute="_compute_result", store=True)
    booking_id = fields.Many2one("booking", string="Booking")

    @api.depends(
        "name",
        "email_from",
        "subject",
        "color",
        "opening_note",
        "include_opening_note",
        "welcome_text",
        "include_welcome_text",
        "booking_details",
        "payment_methods_comments",
        "cancelation_terms",
        "outline",
        "include_outline",
        "booking_id",
    )
    def _compute_result(self):
        for record in self:
            company = self.env.company
            user = self.env.user

            placeholders = {
                "#FirstName#": user.name.split(" ")[0] if user.name else "User",
                "#LastName#": user.name.split(" ")[-1] if user.name else "",
                "#PropertyName#": company.name,
                "#DaysBeforeArrival#": 3,
                "#Street#": company.street,
                "#City#": company.city,
                "#State#": company.state_id.name if company.state_id else "",
                "#Zip#": company.zip,
                "#Country#": company.country_id.name if company.country_id else "",
                "#Phone#": company.phone,
                "#Email#": company.email,
            }

            logo = company.logo.decode() if company.logo else ""
            logo_mime = "image/png"

            header = f"""
                <div style="background-color:{record.color}; padding: 20px;">
                    <img src="data:{logo_mime};base64,{logo}" alt="{company.name}" style="height: 100px;"/>
                    <div style="float: right; text-align: right;">
                        <strong>{company.name}</strong><br/>
                        {company.street}<br/>
                        {company.city}, {company.state_id.name}, {company.zip}<br/>
                        {company.country_id.name}<br/>
                        {company.phone}<br/>
                        {company.email}
                    </div>
                </div>
                <hr/>
            """
            footer = f"""
                <hr/>
                <div style="background-color:{record.color}; padding: 20px;">
                    <p>&copy; {fields.Date.today().year} {company.name}, {company.street}, {company.city}, {company.state_id.name}, {company.zip}</p>
                    <p>The message was automatically generated by MOVO</p>
                </div>
            """
            main_content = ""
            if record.include_opening_note:
                opening_note_content = record.opening_note
                if opening_note_content:
                    for placeholder, value in placeholders.items():
                        opening_note_content = opening_note_content.replace(
                            placeholder, str(value)
                        )
                    main_content += (
                        f"<div style='padding: 10px;'>{opening_note_content}</div>"
                    )
            if record.include_welcome_text:
                welcome_text_content = record.welcome_text
                if welcome_text_content:
                    for placeholder, value in placeholders.items():
                        welcome_text_content = welcome_text_content.replace(
                            placeholder, str(value)
                        )
                    main_content += (
                        f"<div style='padding: 10px;'>{welcome_text_content}</div>"
                    )

            if record.booking_details and record.booking_id:
                booking_details_content = record.get_booking_details(
                    record.booking_id.id
                )
                main_content += (
                    f"<div style='padding: 10px;'>{booking_details_content}</div>"
                )

            if record.payment_methods_comments:
                payment_methods_content = (
                    "<div style='padding: 20px;'>Payment Methods and Comments</div>"
                )
                for placeholder, value in placeholders.items():
                    payment_methods_content = payment_methods_content.replace(
                        placeholder, str(value)
                    )
                main_content += payment_methods_content
            if record.cancelation_terms:
                cancelation_terms_content = (
                    "<div style='padding: 20px;'>Cancelation Terms</div>"
                )
                for placeholder, value in placeholders.items():
                    cancelation_terms_content = cancelation_terms_content.replace(
                        placeholder, str(value)
                    )
                main_content += cancelation_terms_content
            if record.include_outline:
                outline_content = record.outline
                if outline_content:
                    for placeholder, value in placeholders.items():
                        outline_content = outline_content.replace(
                            placeholder, str(value)
                        )
                    main_content += (
                        f"<div style='padding: 10px;'>{outline_content}</div>"
                    )

            record.result = f"""
                {header}
                <div style="padding: 20px;">
                    {main_content}
                </div>
                {footer}
            """

    @api.model
    def get_booking_details(self, booking_id):
        booking = self.env["booking"].browse(booking_id)
        if booking:
            result = f"""
                <div>
                    <h2>Booking details</h2>
                    <p><strong>Booking No:</strong> {booking.unique_id}</p>
                    <table style="width:100%; border: 1px solid #ddd; border-collapse: collapse;">
                        <tr style="background-color:{self.color}">
                            <th style="border: 1px solid #ddd; padding: 8px;">Arrival:</th>
                            <td style="border: 1px solid #ddd; padding: 8px;">{booking.check_in_date}</td>
                        </tr>
                        <tr>
                            <th style="border: 1px solid #ddd; padding: 8px;">Departure:</th>
                            <td style="border: 1px solid #ddd; padding: 8px;">{booking.check_out_date}</td>
                        </tr>
                        <tr style="background-color:{self.color}">
                            <th style="border: 1px solid #ddd; padding: 8px;">Nights:</th>
                            <td style="border: 1px solid #ddd; padding: 8px;">{booking.nights}</td>
                        </tr>
                    </table>
                    <h3>Accommodation and services</h3>
                    <table style="width:100%; border: 1px solid #ddd; border-collapse: collapse;">
                        <tr style="background-color:{self.color}">
                            <th style="border: 1px solid #ddd; padding: 8px;">Name</th>
                            <th style="border: 1px solid #ddd; padding: 8px;">Quantity</th>
                            <th style="border: 1px solid #ddd; padding: 8px;">Total, USD</th>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #ddd; padding: 8px;">{booking.room_type_id.rooms}</td>
                            <td style="border: 1px solid #ddd; padding: 8px;">{len(booking.room_type_id)}</td>
                            <td style="border: 1px solid #ddd; padding: 8px;">{booking.accommodation.price}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #ddd; padding: 8px;">{booking.room_service_id.service}</td>
                            <td style="border: 1px solid #ddd; padding: 8px;">{len(booking.room_service_id)}</td>
                            <td style="border: 1px solid #ddd; padding: 8px;">included</td>
                        </tr>
                    </table>
                    <h3>Extra services</h3>
                    <table style="width:100%; border: 1px solid #ddd; border-collapse: collapse;">
                        <tr style="background-color:{self.color}">
                            <th style="border: 1px solid #ddd; padding: 8px;">Name</th>
                            <th style="border: 1px solid #ddd; padding: 8px;">Quantity</th>
                            <th style="border: 1px solid #ddd; padding: 8px;">Total, USD</th>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #ddd; padding: 8px;">{booking.room_service_ids.service_name}</td>
                            <td style="border: 1px solid #ddd; padding: 8px;">{len(booking.room_service_ids)}</td>
                            <td style="border: 1px solid #ddd; padding: 8px;">{booking.room_service_id}</td>
                        </tr>
                    </table>
                    <h3>Total due : {booking.total}</h3>
                </div>
            """
            return result

    def action_send_test_email(self):
        view_id = self.env.ref("hms_app.send_test_mail_form").id
        return {
            "type": "ir.actions.act_window",
            "name": _("Send Test Email"),
            "view_mode": "form",
            "res_model": "send.test.mail",
            "views": [(view_id, "form")],
            "target": "new",
        }

    def send_mail(self, booking_id):
        booking = self.env["booking"].browse(booking_id)

        mail_server = self.env["ir.mail_server"].search([], limit=1)
        if not mail_server:
            raise UserError(_("No outgoing mail server configured."))

        email_from = mail_server.smtp_user

        welcome_mail_template = self.search([], limit=1)
        welcome_mail_template.booking_id = booking_id
        welcome_mail_template._compute_result()

        content = welcome_mail_template.result

        if booking.guest_id.email:
            mail_values = {
                "subject": welcome_mail_template.subject,
                "body_html": content,
                "email_to": booking.guest_id.email,
                "email_from": email_from,
            }

            mail = self.env["mail.mail"].create(mail_values)
            mail.send()

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        record = self.search([], limit=1)
        if record:
            res.update(
                {
                    "name": record.name,
                    "email_from": record.email_from,
                    "subject": record.subject,
                    "color": record.color,
                    "opening_note": record.opening_note,
                    "include_opening_note": record.include_opening_note,
                    "welcome_text": record.welcome_text,
                    "include_welcome_text": record.include_welcome_text,
                    "booking_details": record.booking_details,
                    "payment_methods_comments": record.payment_methods_comments,
                    "cancelation_terms": record.cancelation_terms,
                    "outline": record.outline,
                    "include_outline": record.include_outline,
                    "result": record.result,
                }
            )
        return res

    @api.model
    def create(self, vals):
        record = self.search([], limit=1)
        if record:
            record.write(vals)  # Mavjud yozuvni yangilash
            return record
        return super().create(vals)