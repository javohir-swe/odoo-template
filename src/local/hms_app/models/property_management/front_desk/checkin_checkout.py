from odoo import api, exceptions, fields, models


class BookingCheckIn(models.Model):
    _name = "booking.check_in"
    _description = "Check In"

    booking_id = fields.Many2one("booking", string="Booking")
    unique_id = fields.Char(
        related="booking_id.unique_id", string="Booking number", readonly=True
    )
    room_type_id = fields.Many2one(
        related="booking_id.room_type_id", string="Room Type", readonly=True
    )
    room_number = fields.Many2one(
        related="booking_id.room_number", string="Room Number", readonly=True
    )
    check_in_date = fields.Date(
        string="Check-in Date",
        default=fields.Datetime.now,
    )
    check_in_time = fields.Float(string="Check In Time")

    @api.model
    def create(self, vals):
        booking = self.env["booking"].browse(vals["booking_id"])

        # if not booking.checkinable:
        if not booking.is_check_out:
            if not booking.is_check_in:
                booking.arrival_status = "arrival"
                booking.is_check_in = True
                booking.is_check_out = False
                booking.arrival_date = vals.get("check_in_date")
                booking.arrival_time = vals.get("check_in_time")
            else:
                raise exceptions.ValidationError("Booking already checked-in.")
        else:
            raise exceptions.ValidationError("Booking already checked-out.")
        # else:
        #     raise exceptions.ValidationError(
        #         "The previous guest has not left the room yet."
        #     )

        return super().create(vals)


class BookingCheckout(models.Model):
    _name = "booking.check_out"
    _description = "Check Out"

    booking_id = fields.Many2one("booking", string="Booking")
    unique_id = fields.Char(
        related="booking_id.unique_id", string="Booking number", readonly=True
    )
    room_type_id = fields.Many2one(
        related="booking_id.room_type_id", string="Room Type", readonly=True
    )
    room_number = fields.Many2one(
        related="booking_id.room_number", string="Room Number", readonly=True
    )
    check_out_date = fields.Date(
        related="booking_id.check_out_date", string="Check-out Date", readonly=False
    )
    check_out_times = fields.Selection(
        related="booking_id.check_out_times",
        string="Check-out Times",
    )

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.booking_id and record.check_out_date and record.check_out_times:
            if not record.booking_id.is_check_out:
                if record.booking_id.is_check_in:
                    if record.booking_id.is_paid:
                        record.booking_id.is_check_out = True
                    else:
                        raise exceptions.ValidationError(
                            "Payment must be made before check-out"
                        )
                else:
                    raise exceptions.ValidationError(
                        "Must be checked-in before check-out"
                    )
            else:
                raise exceptions.ValidationError("Check-out is already done.")
        else:
            raise exceptions.ValidationError("Something is wrong!")
        return record
