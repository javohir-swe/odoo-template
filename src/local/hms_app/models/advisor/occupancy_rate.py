from odoo import fields, models


class OccupancyRate(models.Model):
    _name = "occupancy.rate"
    _description = "Occupancy Rate"

    booking_id = fields.Many2one("booking", string="Booking")
    check_in_date = fields.Date(
        related="booking_id.check_in_date", string="Check-in Date"
    )
    check_out_date = fields.Date(
        related="booking_id.check_out_date", string="Check-out Date"
    )
    nights = fields.Integer(related="booking_id.nights", string="Nights")
    adults = fields.Selection(related="booking_id.adults", string="Adults")
    children = fields.Selection(related="booking_id.children", string="Children")
    customer_company_id = fields.Many2one(
        related="booking_id.customer_company_id", string="Customer Company"
    )
    agent_company_id = fields.Many2one(
        related="booking_id.agent_company_id", string="Agent Company"
    )
    rate_plan = fields.Many2one(related="booking_id.rate_plan", string="Rate Plan")
    room_type_id = fields.Many2one(
        related="booking_id.room_type_id", string="Room Type"
    )
    accommodation = fields.Many2one(
        related="booking_id.accommodation", string="Accommodation"
    )
    room_number = fields.Many2one(
        related="booking_id.room_number", string="Room Number"
    )
    available_room_ids = fields.Many2many(
        related="booking_id.available_room_ids", string="Available Rooms"
    )
    dont_move = fields.Boolean(
        related="booking_id.dont_move", string="Do not allow room move"
    )
    check_in_time = fields.Many2one(
        related="booking_id.check_in_time", string="Check In Time"
    )
    checkout_time = fields.Many2one(
        related="booking_id.checkout_time", string="Check Out Time"
    )
    price_detail_ids = fields.One2many(
        related="booking_id.price_detail_ids", string="Price Details"
    )
    room_service_id = fields.One2many(
        related="booking_id.room_service_id", string="Room Service"
    )
    room_service_ids = fields.Many2many(
        related="booking_id.room_service_ids", string="Room Service (2)"
    )
    guest_id = fields.Many2one(related="booking_id.guest_id", string="Guest")
    first_name = fields.Char(related="booking_id.first_name", string="First Name")
    last_name = fields.Char(related="booking_id.last_name", string="Last Name")
    middle_name = fields.Char(related="booking_id.middle_name", string="Middle Name")
    email = fields.Char(related="booking_id.email", string="Email")
    phone = fields.Char(related="booking_id.phone", string="Phone")
    gender = fields.Selection(related="booking_id.gender", string="Gender")
    send_email = fields.Boolean(
        related="booking_id.send_email", string="Send email notifications"
    )
    citizenship = fields.Selection(
        related="booking_id.citizenship", string="Citizenship"
    )
    deposit = fields.Float(related="booking_id.deposit", string="Deposit")
    guarantee_method = fields.Selection(
        related="booking_id.guarantee_method", string="Guarantee Method"
    )
    service_and_accommodation = fields.Float(
        related="booking_id.service_and_accommodation",
        string="Service and Accommodation",
    )
    total = fields.Float(related="booking_id.total", string="Total")
    payment_due = fields.Float(related="booking_id.payment_due", string="Payment Due")
    unique_id = fields.Char(related="booking_id.unique_id", string="Unique ID")
    regenerate_accommodations = fields.Boolean(
        related="booking_id.regenerate_accommodations",
        string="Regenerate Accommodations",
    )
    group_unique_id = fields.Char(
        related="booking_id.group_unique_id", string="Group Unique ID"
    )
    total_summary = fields.Text(
        related="booking_id.total_summary", string="Booking Summary"
    )
    price_detail_total = fields.Float(
        related="booking_id.price_detail_total", string="Total Price Detail"
    )
    average_daily_rate = fields.Float(
        related="booking_id.average_daily_rate", string="Average Daily Rate"
    )
    cost_of_stay = fields.Float(
        related="booking_id.cost_of_stay", string="Cost of Stay"
    )
    point_of_sale = fields.Many2one(
        related="booking_id.point_of_sale", string="Point of Sale"
    )
    purpose_of_visit = fields.Many2one(
        related="booking_id.purpose_of_visit", string="Purpose of Visit"
    )
    tag = fields.Many2one(related="booking_id.tag", string="Tag")
    payment_method = fields.Many2one(
        related="booking_id.payment_method", string="Payment Method"
    )
    market_segment = fields.Many2one(
        related="booking_id.market_segment", string="Market Segment"
    )
    staff = fields.Many2one(related="booking_id.staff", string="Staff")
    guest_status = fields.Many2one(
        related="booking_id.guest_status", string="Guest Status"
    )
    customer_language = fields.Selection(
        related="booking_id.customer_language", string="Customer Language"
    )
    guest_comment = fields.Text(
        related="booking_id.guest_comment", string="Guest Comment"
    )
    total_services = fields.Char(
        related="booking_id.total_services", string="Total Services"
    )
    status = fields.Selection(related="booking_id.status", string="Status")
    arrival_status = fields.Selection(
        related="booking_id.arrival_status", string="Arrival Status"
    )
    departure_status = fields.Selection(
        related="booking_id.departure_status", string="Departure Status"
    )
    # date_of_stay_and_guests = fields.Char(
    #     related="booking_id.date_of_stay_and_guests", string="Date of Stay and Guests"
    # )
    tags = fields.Selection(related="booking_id.tags", string="Tags")
    change_history_ids = fields.One2many(
        related="booking_id.change_history_ids", string="Change History"
    )
    is_check_in = fields.Boolean(
        related="booking_id.is_check_in", string="Is In Check-In"
    )
    is_check_out = fields.Boolean(
        related="booking_id.is_check_out", string="Is In Check-Out"
    )
