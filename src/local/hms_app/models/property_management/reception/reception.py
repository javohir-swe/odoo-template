import time
from datetime import date

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class Reception(models.Model):
    _name = "reception"
    _description = "Reception"

    name = fields.Char(string="Name", compute="_compute_name")
    booking_id = fields.Many2one("booking", string="Booking", readonly=False)
    check_in_date = fields.Date(
        related="booking_id.check_in_date", string="Check-in Date", readonly=False
    )
    check_out_date = fields.Date(
        related="booking_id.check_out_date", string="Check-out Date", readonly=False
    )
    nights = fields.Integer(
        related="booking_id.nights", string="Nights", readonly=False
    )
    adults = fields.Selection(
        related="booking_id.adults", string="Adults", readonly=False
    )
    children = fields.Selection(
        related="booking_id.children", string="Children", readonly=False
    )
    customer_company_id = fields.Many2one(
        related="booking_id.customer_company_id",
        string="Customer Company",
        readonly=False,
    )
    agent_company_id = fields.Many2one(
        related="booking_id.agent_company_id", string="Agent Company", readonly=False
    )
    rate_plan = fields.Many2one(
        related="booking_id.rate_plan", string="Rate Plan", readonly=False
    )
    room_type_id = fields.Many2one(
        related="booking_id.room_type_id", string="Room Type", readonly=False
    )
    accommodation = fields.Many2one(
        related="booking_id.accommodation", string="Accommodation", readonly=False
    )
    room_number = fields.Many2one(
        related="booking_id.room_number", string="Room Number", readonly=False
    )
    available_room_ids = fields.Many2many(
        related="booking_id.available_room_ids",
        string="Available Rooms",
        readonly=False,
    )
    dont_move = fields.Boolean(
        related="booking_id.dont_move", string="Do not allow room move", readonly=False
    )
    check_in_time = fields.Many2one(
        related="booking_id.check_in_time", string="Check In Time", readonly=False
    )
    checkout_time = fields.Many2one(
        related="booking_id.checkout_time", string="Check Out Time", readonly=False
    )
    price_detail_ids = fields.One2many(
        related="booking_id.price_detail_ids", string="Price Details", readonly=False
    )
    room_service_id = fields.One2many(
        related="booking_id.room_service_id", string="Room Service", readonly=False
    )
    guest_id = fields.Many2one(
        related="booking_id.guest_id", string="Guest", readonly=False
    )
    send_email = fields.Boolean(
        related="booking_id.send_email",
        string="Send email notifications",
        readonly=False,
    )
    deposit = fields.Float(
        related="booking_id.deposit", string="Deposit", readonly=False
    )
    guarantee_method = fields.Selection(
        related="booking_id.guarantee_method", string="Guarantee Method", readonly=False
    )
    service_and_accommodation = fields.Float(
        related="booking_id.service_and_accommodation",
        string="Service and Accommodation",
        readonly=False,
    )
    total = fields.Float(related="booking_id.total", string="Total", readonly=False)
    amount_paid = fields.Float(
        related="booking_id.amount_paid", string="Amount_paid", readonly=False
    )
    must_pay = fields.Float(
        related="booking_id.must_pay", string="Must_pay", readonly=False
    )
    residual = fields.Float(
        related="booking_id.residual", string="Residual", readonly=False
    )
    payment_due = fields.Float(
        related="booking_id.payment_due", string="Payment Due", readonly=False
    )
    unique_id = fields.Char(
        related="booking_id.unique_id", string="Unique ID", readonly=False
    )
    regenerate_accommodations = fields.Boolean(
        related="booking_id.regenerate_accommodations",
        string="Regenerate accommodations",
        readonly=False,
    )
    group_unique_id = fields.Char(
        related="booking_id.group_unique_id", string="Group Unique ID", readonly=False
    )
    total_summary = fields.Text(
        related="booking_id.total_summary", string="Booking Summary", readonly=False
    )
    price_detail_total = fields.Float(
        related="booking_id.price_detail_total",
        string="Total Price Detail",
        readonly=False,
    )
    average_daily_rate = fields.Float(
        related="booking_id.average_daily_rate",
        string="Average Daily Rate",
        readonly=False,
    )
    cost_of_stay = fields.Float(
        related="booking_id.cost_of_stay", string="Cost of Stay", readonly=False
    )
    point_of_sale = fields.Many2one(
        related="booking_id.point_of_sale", string="Point of Sale", readonly=False
    )

    purpose_of_visit = fields.Many2one(
        related="booking_id.purpose_of_visit", string="Purpose of Visit", readonly=False
    )
    tag = fields.Many2one(related="booking_id.tag", string="Tag", readonly=False)
    payment_method = fields.Many2one(
        related="booking_id.new_payment_method", string="Payment Method", readonly=False
    )
    market_segment = fields.Many2one(
        related="booking_id.market_segment", string="Market Segment", readonly=False
    )
    staff = fields.Many2one(related="booking_id.staff", string="Staff", readonly=False)
    guest_status = fields.Many2one(
        related="booking_id.guest_status", string="Guest Status", readonly=False
    )
    customer_language = fields.Selection(
        related="booking_id.customer_language",
        string="Customer Language",
        readonly=False,
    )
    guest_comment = fields.Text(
        related="booking_id.guest_comment", string="Guest Comment", readonly=False
    )
    total_services = fields.Char(
        related="booking_id.total_services", string="Total Services", readonly=False
    )
    status = fields.Selection(
        related="booking_id.status", string="Status", readonly=False
    )

    arrival_status = fields.Selection(
        related="booking_id.arrival_status", string="Arrival Status", readonly=False
    )
    departure_status = fields.Selection(
        related="booking_id.departure_status", string="Departure Status", readonly=False
    )
    change_history_ids = fields.One2many(
        related="booking_id.change_history_ids",
        string="Change History",
        readonly=True,
    )

    notes_ids = fields.One2many(
        "notes_and_instructions", "reception_id", string="Notes and Instructions"
    )
    is_check_in = fields.Boolean(
        related="booking_id.is_check_in", string="Is Check In", readonly=False
    )
    is_check_out = fields.Boolean(
        related="booking_id.is_check_out", string="Is Check Out", readonly=False
    )
    first_name = fields.Char(
        related="booking_id.guest_id.first_name", string="Fist Name", readonly=False
    )
    last_name = fields.Char(
        related="booking_id.guest_id.last_name", string="Last Name", readonly=False
    )
    middle_name = fields.Char(
        related="booking_id.guest_id.middle_name", string="Middle Name", readonly=False
    )
    email = fields.Char(
        related="booking_id.guest_id.email", string="Email", readonly=False
    )
    phone = fields.Char(
        related="booking_id.guest_id.phone", string="Phone", readonly=False
    )

    gender = fields.Selection(
        related="booking_id.guest_id.sex", string="Gender", readonly=False
    )
    # Selection field for countries
    citizenship = fields.Selection(
        selection="_get_country_selection", string="Citizenship"
    )

    # docs and invoices
    invoice_ids = fields.One2many(
        "reception.invoice", "reception_id", string="Invoices and Payments"
    )
    document_ids = fields.One2many("document", "reception_id", string="Documents")
    is_paid = fields.Boolean(related="booking_id.is_paid", string="Is Paid")

    def unlink(self):
        for record in self:
            # Find and unlink related invoices
            if record.invoice_ids:
                record.document_ids.unlink()
                record.invoice_ids.unlink()
        return super().unlink()

    @api.depends("booking_id")
    def _compute_name(self):
        for record in self:
            room_number = record.room_number.number
            guest = record.guest_id.full_name
            room_type = record.room_type_id.rooms
            record.name = f"{room_number} | {guest} | {room_type}"

    @api.model
    def create(self, vals):
        record = super().create(vals)
        # Update booking_id's reception_id with the newly created Reception's ID
        if record.booking_id:
            record.booking_id.reception_id = record.id

        self.env["reception.invoice"].create(
            {
                "reception_id": record.id,
            }
        )
        self.env["document"].create(
            {
                "reception_id": record.id,
            }
        )
        return record

    @api.model
    def _get_country_selection(self):
        countries = self.env["res.country"].search([])
        return [(country.code, country.name) for country in countries]

    @api.model
    def get_reception_data(self):
        # Fetch receptions
        arrivals = self.search([("arrival_status", "!=", False)])
        departures = self.search([("departure_status", "!=", False)])
        occupied_rooms = self.search([("arrival_status", "=", "arrival")])

        # Format data
        def format_reception_data(reception):
            return {
                "reception_id": reception.id,
                "booking_number": reception.unique_id,
                "customer": f"{reception.guest_id.first_name} {reception.guest_id.last_name}",
                "room_number": reception.room_number.number
                if reception.room_number
                else "",
                "check_in_date": reception.check_in_date,
                "check_out_date": reception.check_out_date,
                "check_in_time": reception.check_in_time.name,
                "check_out_time": reception.checkout_time.name,
                "room_type": reception.room_type_id.rooms
                if reception.room_type_id
                else "",
                "is_check_in": reception.is_check_in,
                "is_check_out": reception.is_check_out,
                "Balance": f"{reception.total} uzs",
                "tags": reception.tag or "",
                "notes": reception.guest_comment or "No",
                "nights": reception.nights,
                "guest_comment": reception.guest_comment or "No",
                "arrival_status": reception.arrival_status,
                "departure_status": reception.departure_status,
            }

        data = [
            {
                "type": "arrivals",
                "data": [format_reception_data(reception) for reception in arrivals],
            },
            {
                "type": "departures",
                "data": [format_reception_data(reception) for reception in departures],
            },
            {
                "type": "occupied_rooms",
                "data": [
                    format_reception_data(reception) for reception in occupied_rooms
                ],
            },
        ]

        return data


class Invoice(models.Model):
    _name = "reception.invoice"
    _description = "Hotel Invoice"

    reception_id = fields.Many2one("reception", string="Reception")
    booking_id = fields.Many2one(
        related="reception_id.booking_id", string="Booking", readonly=False
    )
    invoice_number = fields.Char(string="Invoice Number", readonly=True)
    room_number = fields.Many2one(
        related="reception_id.room_number", string="Room Number", readonly=True
    )
    bill_to = fields.Many2one(
        related="reception_id.guest_id", string="Bill To", readonly=True
    )
    services = fields.Integer(string="Services")
    amount = fields.Float(
        related="reception_id.cost_of_stay", string="Amount", readonly=True
    )
    to_be_paid = fields.Float(string="To be Paid", compute="_compute_to_be_paid")
    to_be_refunded = fields.Float(string="To be Refunded", default=0.0)
    status = fields.Selection(
        [
            ("not_paid", "Not paid"),
            ("paid", "Paid"),
        ],
        string="Status",
        default="not_paid",
    )
    room_service_ids = fields.One2many(
        related="reception_id.room_service_id", string="Room Services", readonly=True
    )
    is_visible_payment_btn = fields.Boolean(string="Paid", compute="_compute_buttons")
    is_visible_refund_btn = fields.Boolean(string="Refund", compute="_compute_buttons")

    @api.depends("invoice_number", "status")
    def _compute_to_be_paid(self):
        for record in self:
            if record.status == "paid":
                record.to_be_paid = 0
            else:
                record.to_be_paid = record.amount

    def _compute_buttons(self):
        for record in self:
            if record.status == "paid":
                record.is_visible_refund_btn = True
                record.is_visible_payment_btn = False
            if record.status == "not_paid":
                record.is_visible_refund_btn = False
                record.is_visible_payment_btn = True

    @api.model
    def create(self, vals):
        timestamp = int(time.time())
        count = self.search_count([]) + 1
        vals["invoice_number"] = "{}-{:02d}".format(timestamp, count)
        return super().create(vals)

    @api.depends("reception_id.room_number", "reception_id.room_service_id")
    def _compute_services(self):
        for record in self:
            room_count = len(record.reception_id.room_number)
            room_service_count = len(record.reception_id.room_service_id)
            record.services = room_count + room_service_count

    def action_apply_payment(self):
        self.ensure_one()

        payment_record = self.env["reception.payment"].create(
            {
                "invoice_id": self.id,
                "reception_id": self.reception_id,
                "bill_to": self.bill_to,
                "payment_date": fields.Datetime.now(),
                "is_on": True,
                "service_name": self.room_number,
                "payment": self.to_be_paid,
                "amount": self.to_be_paid,
            }
        )

        return {
            "type": "ir.actions.act_window",
            "res_model": "reception.payment",
            "name": "Apply Payment",
            "target": "new",
            "view_mode": "form",
            "res_id": payment_record.id,
        }

    def action_apply_prefund(self):
        self.ensure_one()

        refund_record = self.env["reception.refund"].create(
            {
                "invoice_id": self.id,
                "reception_id": self.reception_id,
                "recipient": self.bill_to,
                "payment_date": fields.Datetime.now(),
                "service_name": self.to_be_paid,
                "refund": self.to_be_paid,
            }
        )

        return {
            "type": "ir.actions.act_window",
            "res_model": "reception.refund",
            "name": "Apply Refund",
            "target": "new",
            "view_mode": "form",
            "res_id": refund_record.id,
        }

    def action_make_deposit(self):
        self.ensure_one()
        deposit = self.env["reception.deposit"].create(
            {
                "booking_id": self.reception_id.booking_id.id,
                "amount": 0.0,
            }
        )

        return {
            "type": "ir.actions.act_window",
            "res_model": "reception.deposit",
            "name": "Make Deposit",
            "target": "new",
            "view_mode": "form",
            "res_id": deposit.id,
        }


class InvoicePayment(models.Model):
    _name = "reception.payment"
    _description = "Hotel Invoice Payment"

    invoice_id = fields.Many2one("reception.invoice", string="Invoice")
    reception_id = fields.Many2one(
        related="invoice_id.reception_id", string="Reception"
    )
    bill_to = fields.Many2one(related="reception_id.guest_id", string="Bill To")
    payment_date = fields.Datetime(string="Payment Date", default=fields.Datetime.now)
    payment_method = fields.Many2one(
        related="reception_id.payment_method", string="Payment Method", readonly=False
    )

    # price details
    is_on = fields.Boolean(string="Is Payment On", default=True)
    service_name = fields.Many2one(related="reception_id.room_number", string="Service")
    payment = fields.Float(string="Payment", readonly=False)
    amount = fields.Float(related="reception_id.total", string="Amount")
    to_be_paid = fields.Float(related="reception_id.must_pay", string="To be Paid")
    comment = fields.Text(string="Payment Comment")
    payment_methods = fields.Selection(
        [
            ("cash_cashbox", "By cash via cashbox"),
            (
                "bank_transfer_legal",
                "Bank transfer for legal entities (invoice issued by hotel)",
            ),
            (
                "bank_transfer_individual",
                "Bank transfer for individuals (invoice issued by hotel)",
            ),
            ("card_terminal", "By card via terminal"),
        ],
        string="Payment Method",
        default="cash_cashbox",
    )

    @api.constrains("payment", "to_be_paid")
    def _check_payment(self):
        for record in self:
            if record.payment > record.to_be_paid:
                raise UserError("Payment must be less than or equal to To Be Paid.")

    @api.model
    def create(self, vals):
        if "to_be_paid" in vals:
            vals["payment"] = vals["to_be_paid"]
        record = super().create(vals)
        record._check_payment()
        return record

    def write(self, vals):
        for record in self:
            if "to_be_paid" in vals:
                vals["payment"] = vals["to_be_paid"]
            elif "payment" in vals and vals["payment"] > record.to_be_paid:
                raise UserError("Payment must be less than or equal to To Be Paid.")
        res = super().write(vals)

        for record in self:
            booking = self.env["booking"].search(
                [("unique_id", "=", record.reception_id.unique_id)], limit=1
            )

            if record.payment_methods and not booking.is_paid:
                if booking:
                    if booking.must_pay > 0.0 and record.payment > 0.0:
                        booking.amount_paid += record.payment
                        if booking.must_pay == 0.0:
                            booking.write({"is_paid": True})
                            record.invoice_id.write(
                                {
                                    "status": "paid",
                                }
                            )
                        else:
                            booking.write({"is_paid": False})

            else:
                if booking:
                    booking.write({"is_paid": False})
                    record.invoice_id.write(
                        {
                            "status": "not_paid",
                        }
                    )

        return res

    def unlink(self):
        for record in self:
            super(InvoicePayment, record).unlink()
        return super().unlink()


class InvoiceRefund(models.Model):
    _name = "reception.refund"
    _description = "Hotel Invoice Refund"

    invoice_id = fields.Many2one("reception.invoice", string="Invoice")
    reception_id = fields.Many2one(
        related="invoice_id.reception_id", string="Reception"
    )
    recipient = fields.Many2one(related="reception_id.guest_id", string="Recipient")
    refund_direction = fields.Selection(
        [("to_guest", "To Guest"), ("for_deposit", "For Deposit")], default="to_guest"
    )
    payment_date = fields.Datetime(string="Payment Date", default=fields.Datetime.now)
    payment_method = fields.Many2one(
        related="reception_id.payment_method", string="Payment Method", readonly=False
    )

    # refund details

    is_on = fields.Boolean(string="Is Payment On", default=True)
    service_name = fields.Many2one(related="reception_id.room_number", string="Service")
    refund = fields.Float(string="Refund", readonly=False, compute="_compute_refund")
    amount = fields.Float(related="reception_id.total", string="Amount")
    to_be_refunded = fields.Float(related="reception_id.total", string="To be Refunded")
    comment = fields.Text(string="Payment Comment")

    def _compute_refund(self):
        for record in self:
            if record.invoice_id:
                record.refund = record.reception_id.total

    @api.model
    def create(self, vals):
        invoice = self.env["reception.invoice"].browse(vals["invoice_id"])
        invoice.status = "not_paid"
        return super().create(vals)

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            record.invoice_id.write(
                {
                    "status": "not_paid",
                }
            )
        return res

    def unlink(self):
        for record in self:
            super(InvoiceRefund, record).unlink()
        return super().unlink()


class Document(models.Model):
    _name = "document"
    _description = "Document"

    reception_id = fields.Many2one("reception", string="Reception")
    booking_id = fields.Many2one(
        related="reception_id.booking_id", string="Booking", readonly=True
    )
    check_in_date = fields.Date(
        related="reception_id.check_in_date", string="Check-in Date", readonly=True
    )
    check_out_date = fields.Date(
        related="reception_id.check_out_date", string="Check-out Date", readonly=True
    )
    nights = fields.Integer(
        related="reception_id.nights", string="Nights", readonly=True
    )
    adults = fields.Selection(
        related="reception_id.adults", string="Adults", readonly=True
    )
    children = fields.Selection(
        related="reception_id.children", string="Children", readonly=True
    )
    customer_company_id = fields.Many2one(
        related="reception_id.customer_company_id",
        string="Customer Company",
        readonly=True,
    )
    agent_company_id = fields.Many2one(
        related="reception_id.agent_company_id", string="Agent Company", readonly=True
    )
    rate_plan = fields.Many2one(
        related="reception_id.rate_plan", string="Rate Plan", readonly=True
    )
    room_type_id = fields.Many2one(
        related="reception_id.room_type_id", string="Room Type", readonly=True
    )
    accommodation = fields.Many2one(
        related="reception_id.accommodation", string="Accommodation", readonly=True
    )
    room_number = fields.Many2one(
        related="reception_id.room_number", string="Room Number", readonly=True
    )
    available_room_ids = fields.Many2many(
        related="reception_id.available_room_ids",
        string="Available Rooms",
        readonly=True,
    )
    dont_move = fields.Boolean(
        related="reception_id.dont_move", string="Do not allow room move", readonly=True
    )
    check_in_time = fields.Many2one(
        related="reception_id.check_in_time", string="Check In Time", readonly=True
    )
    checkout_time = fields.Many2one(
        related="reception_id.checkout_time", string="Check Out Time", readonly=True
    )
    price_detail_ids = fields.One2many(
        related="reception_id.price_detail_ids", string="Price Details", readonly=True
    )
    room_service_id = fields.One2many(
        related="reception_id.room_service_id", string="Room Service", readonly=True
    )
    guest_id = fields.Many2one(
        related="reception_id.guest_id", string="Guest", readonly=True
    )
    send_email = fields.Boolean(
        related="reception_id.send_email",
        string="Send email notifications",
        readonly=True,
    )
    deposit = fields.Float(
        related="reception_id.deposit", string="Deposit", readonly=True
    )
    guarantee_method = fields.Selection(
        related="reception_id.guarantee_method",
        string="Guarantee Method",
        readonly=True,
    )
    service_and_accommodation = fields.Float(
        related="reception_id.service_and_accommodation",
        string="Service and Accommodation",
        readonly=True,
    )
    total = fields.Float(related="reception_id.total", string="Total", readonly=True)
    payment_due = fields.Float(
        related="reception_id.payment_due", string="Payment Due", readonly=True
    )
    unique_id = fields.Char(
        related="reception_id.unique_id", string="Unique ID", readonly=True
    )
    regenerate_accommodations = fields.Boolean(
        related="reception_id.regenerate_accommodations",
        string="Regenerate accommodations",
        readonly=True,
    )
    group_unique_id = fields.Char(
        related="reception_id.group_unique_id", string="Group Unique ID", readonly=True
    )
    total_summary = fields.Text(
        related="reception_id.total_summary", string="Booking Summary", readonly=True
    )
    price_detail_total = fields.Float(
        related="reception_id.price_detail_total",
        string="Total Price Detail",
        readonly=True,
    )
    average_daily_rate = fields.Float(
        related="reception_id.average_daily_rate",
        string="Average Daily Rate",
        readonly=True,
    )
    cost_of_stay = fields.Float(
        related="reception_id.cost_of_stay", string="Cost of Stay", readonly=True
    )
    point_of_sale = fields.Many2one(
        related="reception_id.point_of_sale", string="Point of Sale", readonly=True
    )
    purpose_of_visit = fields.Many2one(
        related="reception_id.purpose_of_visit",
        string="Purpose of Visit",
        readonly=True,
    )
    tag = fields.Many2one(related="reception_id.tag", string="Tag", readonly=True)
    payment_method = fields.Many2one(
        related="reception_id.payment_method", string="Payment Method", readonly=True
    )
    market_segment = fields.Many2one(
        related="reception_id.market_segment", string="Market Segment", readonly=True
    )
    staff = fields.Many2one(related="reception_id.staff", string="Staff", readonly=True)
    guest_status = fields.Many2one(
        related="reception_id.guest_status", string="Guest Status", readonly=True
    )
    customer_language = fields.Selection(
        related="reception_id.customer_language",
        string="Customer Language",
        readonly=True,
    )
    guest_comment = fields.Text(
        related="reception_id.guest_comment", string="Guest Comment", readonly=True
    )
    total_services = fields.Char(
        related="reception_id.total_services", string="Total Services", readonly=True
    )
    reception_status = fields.Selection(
        related="reception_id.status", string="Status", readonly=True
    )
    arrival_status = fields.Selection(
        related="reception_id.arrival_status", string="Arrival Status", readonly=True
    )
    departure_status = fields.Selection(
        related="reception_id.departure_status",
        string="Departure Status",
        readonly=True,
    )
    change_history_ids = fields.One2many(
        related="reception_id.change_history_ids",
        string="Change History",
        readonly=True,
    )
    is_check_in = fields.Boolean(
        related="reception_id.is_check_in", string="Is Check In", readonly=True
    )
    is_check_out = fields.Boolean(
        related="reception_id.is_check_out", string="Is Check Out", readonly=True
    )
    first_name = fields.Char(
        related="reception_id.first_name", string="First Name", readonly=True
    )
    last_name = fields.Char(
        related="reception_id.last_name", string="Last Name", readonly=True
    )
    middle_name = fields.Char(
        related="reception_id.middle_name", string="Middle Name", readonly=True
    )
    email = fields.Char(related="reception_id.email", string="Email", readonly=True)
    phone = fields.Char(related="reception_id.phone", string="Phone", readonly=True)
    gender = fields.Selection(
        related="reception_id.gender", string="Gender", readonly=True
    )
    citizenship = fields.Selection(
        related="reception_id.citizenship", string="Citizenship", readonly=True
    )
    status = fields.Selection(
        [("sent", "sent"), ("not_sent", "not_sent")],
        default="not_sent",
        string="Status",
        readonly=True,
    )


class CheckIn(models.Model):
    _name = "reception.checkin"
    _description = "Check In"

    reception_id = fields.Many2one("reception", string="Reception")
    unique_id = fields.Char(
        related="reception_id.unique_id", string="Booking number", readonly=True
    )
    room_type_id = fields.Many2one(
        related="reception_id.room_type_id", string="Room Type", readonly=True
    )
    room_number = fields.Many2one(
        related="reception_id.room_number", string="Room Number", readonly=True
    )
    check_in_date = fields.Date(
        related="reception_id.check_in_date", string="Check-in Date", readonly=False
    )
    check_in_time = fields.Many2one(
        related="reception_id.check_in_time", string="Check In Time", readonly=False
    )

    @api.model
    def create(self, vals):
        reception = self.env["reception"].browse(vals["reception_id"])

        # Check if check_in_date is today or earlier
        if reception.check_in_date > date.today():
            raise ValidationError("Check-in date cannot be in the future.")

        # Check if check_in_date is before or the same as check_out_date
        if reception.check_in_date > reception.check_out_date:
            raise ValidationError("Check-in date cannot be after the check-out date.")

        # Perform the necessary actions
        reception.booking_id.arrival_status = "arrival"
        reception.is_check_in = True

        # Create the CheckIn record
        return super().create(vals)


class Checkout(models.Model):
    _name = "reception.checkout"
    _description = "Check Out"

    reception_id = fields.Many2one("reception", string="Reception")
    unique_id = fields.Char(
        related="reception_id.unique_id", string="Booking number", readonly=True
    )
    room_type_id = fields.Many2one(
        related="reception_id.room_type_id", string="Room Type", readonly=True
    )
    room_number = fields.Many2one(
        related="reception_id.room_number", string="Room Number", readonly=True
    )
    check_out_date = fields.Date(
        related="reception_id.check_out_date", string="Check-out Date", readonly=False
    )
    check_out_time = fields.Many2one(
        related="reception_id.checkout_time", string="Check out Time", readonly=False
    )

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.reception_id and record.reception_id.arrival_status == "arrival":
            record.reception_id.booking_id.departure_status = "checked_out"
            record.reception_id.is_check_out = True
        return record


class Arrival(models.Model):
    _name = "reception.arrival"
    _description = "Arrival"

    booking_id = fields.Many2one("booking", string="Booking")
    tags = fields.Char(string="Tags")
    status = fields.Selection(
        [
            ("waiting", "Waiting"),
            ("same_day_bookings", "Same-day bookings"),
            ("overdue", "Overdue"),
            ("arrival", "Arrival"),
        ],
        string="Status",
    )

    guest_id = fields.Many2one(
        related="booking_id.guest_id", string="Guest", readonly=False
    )
    guest_name = fields.Char(
        related="booking_id.guest_id.first_name", string="Customer", readonly=False
    )
    room_number = fields.Char(
        related="booking_id.room_number.number", string="Room Number", store=True
    )
    checkin_time = fields.Char(
        related="booking_id.check_in_time.name", string="Check-in Time", store=True
    )
    room_type = fields.Char(
        related="booking_id.room_type_id.rooms", string="Room Type", store=True
    )
    balance = fields.Float(related="booking_id.total", string="Balance", store=True)
    number_of_nights = fields.Integer(
        related="booking_id.nights", string="Number of Nights", store=True
    )
    guest_comment = fields.Text(
        related="booking_id.guest_comment", string="Guest Comment", store=True
    )


class Occupied(models.Model):
    _name = "reception.occupied"
    _description = "Occupied"

    booking_id = fields.Many2one("booking", string="Booking")
    tags = fields.Char(string="Tags")

    guest_id = fields.Many2one(
        related="booking_id.guest_id", string="Guest", store=True
    )
    guest_name = fields.Char(
        related="booking_id.guest_id.first_name", string="Customer", store=True
    )
    room_number = fields.Char(
        related="booking_id.room_number.number", string="Room Number", store=True
    )
    checkin_time = fields.Char(
        related="booking_id.check_in_time.name", string="Check-in Time", store=True
    )
    room_type = fields.Char(
        related="booking_id.room_type_id.rooms", string="Room Type", store=True
    )
    balance = fields.Float(related="booking_id.total", string="Balance", store=True)
    number_of_nights = fields.Integer(
        related="booking_id.nights", string="Number of Nights", store=True
    )
    guest_comment = fields.Text(
        related="booking_id.guest_comment", string="Guest Comment", store=True
    )
