import logging
from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class DaySelection(models.Model):
    _name = "rate_plan.day_selection"
    _description = "Day Selection"

    name = fields.Char(string="Day", required=True)


class Closed(models.Model):
    _name = "rate_plan.closed"
    _description = "Rate plan > Closed"

    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")
    room_type_id = fields.Many2one("triple", string="Room Types Id", store=True)
    relevant_date = fields.Date()
    close_id = fields.Many2one("rate.plan", string="Extra")
    status = fields.Selection(
        [("close", "Close"), ("open", "Open")],
        string="Status",
        default="close",
        required=True,
    )

    # ====================== Multi update ====================== #
    @api.model
    def batch_update_or_create(self, domain, new_vals):
        """Update existing records or create new ones based on the specified domain."""
        records = self.search(domain)
        if records:
            records.write(new_vals)
        else:
            # Extract key parts of the domain to use for creating a new record
            create_vals = {}
            for condition in domain:
                field, operator, value = condition
                if operator == "=":
                    create_vals[field] = value
            # Merge with new_vals for creation
            combined_vals = {**create_vals, **new_vals}
            self.create(combined_vals)
        return True
        # ====================== Multi update ====================== #

    @api.model
    def get_statuses(self, date_list):
        """Fetch status for a list of dates."""
        domain = [("relevant_date", "in", date_list)]
        records = self.search(domain)
        return {rec.relevant_date.isoformat(): rec.status for rec in records}

    @api.model
    def get_room_statuses(self, room_type_ids=None, start_date=None, end_date=None):
        domain = [
            ("relevant_date", ">=", start_date),
            ("relevant_date", "<=", end_date),
        ]
        if room_type_ids:
            domain.append(("room_type_id", "in", room_type_ids))
        records = self.search(domain)
        return [
            {
                "date": record.relevant_date,
                "room_type_id": record.room_type_id.id,
                "status": record.status,
            }
            for record in records
        ]

    @api.model
    def create(self, vals):
        existing_record = self.search(
            [
                ("rate_plan_id", "=", vals.get("rate_plan_id")),
                ("room_type_id", "=", vals.get("room_type_id")),
                ("relevant_date", "=", vals.get("relevant_date")),
            ],
            limit=1,
        )

        if existing_record:
            existing_record.write(vals)
            res = existing_record
        else:
            res = super().create(vals)

        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "rate_plan_update",
            {"rate_plan_id": vals.get("rate_plan_id")},
        )
        return res


class MinLOS(models.Model):
    _name = "rate_plan.min_los"
    _description = "Rate plan > MinLOS"

    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")
    room_type_id = fields.Many2one("triple", string="Room Types Id")
    filter_id = fields.Many2one("rate.plan", string="Extra")
    relevant_date = fields.Date()
    number = fields.Integer()
    reset = fields.Boolean(default=False, string="Reset")

    # ====================== Multi update ====================== #
    @api.model
    def batch_update_or_create(self, domain, new_vals):
        """Update existing records or create new ones based on the specified domain."""
        # Reset 'number' to 0 if 'reset' is True
        if new_vals.get("reset", False):
            new_vals["number"] = 0

        records = self.search(domain)
        if records:
            records.write(new_vals)
        else:
            # Extract key parts of the domain to use for creating a new record
            create_vals = {}
            for condition in domain:
                field, operator, value = condition
                if operator == "=":
                    create_vals[field] = value
            # Merge with new_vals for creation
            combined_vals = {**create_vals, **new_vals}
            self.create(combined_vals)
        return True

    @api.model
    def get_statuses(self, date_list):
        """Fetch number for a list of dates."""
        domain = [("relevant_date", "in", date_list)]
        records = self.search(domain)
        return {rec.relevant_date.isoformat(): rec.number for rec in records}

    @api.model
    def get_room_statuses(self, room_type_ids=None, start_date=None, end_date=None):
        """Fetch number for room types within a date range."""
        domain = [
            ("relevant_date", ">=", start_date),
            ("relevant_date", "<=", end_date),
        ]
        if room_type_ids:
            domain.append(("room_type_id", "in", room_type_ids))
        records = self.search(domain)
        return [
            {
                "date": record.relevant_date,
                "room_type_id": record.room_type_id.id,
                "number": record.number,
            }
            for record in records
        ]

    @api.model
    def create(self, vals):
        """Create a new record or update the existing one if it matches the given criteria."""
        # Reset 'number' to 0 if 'reset' is True
        if vals.get("reset", False):
            vals["number"] = 0

        existing_record = self.search(
            [
                ("rate_plan_id", "=", vals.get("rate_plan_id")),
                ("room_type_id", "=", vals.get("room_type_id")),
                ("relevant_date", "=", vals.get("relevant_date")),
            ],
            limit=1,
        )

        if existing_record:
            existing_record.write(vals)
            res = existing_record
        else:
            res = super().create(vals)

        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "rate_plan_update",
            {"rate_plan_id": vals.get("rate_plan_id")},
        )
        return res


class MaxLOS(models.Model):
    _name = "rate_plan.max_los"
    _description = "Rate plan > MaxLOS"

    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")
    room_type_id = fields.Many2one("triple", string="Room Types Id")
    filter_id = fields.Many2one("rate.plan", string="Extra")
    relevant_date = fields.Date()
    number = fields.Integer()
    reset = fields.Boolean(default=False, string="Reset")

    @api.model
    def get_statuses(self, date_list):
        """Fetch number for a list of dates."""
        domain = [("relevant_date", "in", date_list)]
        records = self.search(domain)
        return {rec.relevant_date.isoformat(): rec.number for rec in records}

    @api.model
    def get_room_statuses(self, room_type_ids=None, start_date=None, end_date=None):
        """Fetch number for each room type in the specified date range."""
        domain = [
            ("relevant_date", ">=", start_date),
            ("relevant_date", "<=", end_date),
        ]
        if room_type_ids:
            domain.append(("room_type_id", "in", room_type_ids))
        records = self.search(domain)
        return [
            {
                "date": record.relevant_date,
                "room_type_id": record.room_type_id.id,
                "number": record.number,
            }
            for record in records
        ]

    @api.model
    def create(self, vals):
        """Create or update record if it already exists."""
        existing_record = self.search(
            [
                ("rate_plan_id", "=", vals.get("rate_plan_id")),
                ("room_type_id", "=", vals.get("room_type_id")),
                ("relevant_date", "=", vals.get("relevant_date")),
            ],
            limit=1,
        )

        if existing_record:
            if vals.get("reset", False):
                vals["number"] = 0
            existing_record.write(vals)
            res = existing_record
        else:
            if vals.get("reset", False):
                vals["number"] = 0
            res = super().create(vals)

        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "rate_plan_update",
            {"rate_plan_id": vals.get("rate_plan_id")},
        )
        return res


class MinLOSArrival(models.Model):
    _name = "rate_plan.min_los_arrival"
    _description = "Rate plan > MinLOSArrival"

    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")
    room_type_id = fields.Many2one("triple", string="Room Types Id")
    filter_id = fields.Many2one("rate.plan", string="Extra")
    relevant_date = fields.Date()
    number = fields.Integer()
    reset = fields.Boolean(default=False, string="Reset")

    @api.model
    def get_statuses(self, date_list):
        """Fetch number for a list of dates."""
        domain = [("relevant_date", "in", date_list)]
        records = self.search(domain)
        return {rec.relevant_date.isoformat(): rec.number for rec in records}

    @api.model
    def get_room_statuses(self, room_type_ids=None, start_date=None, end_date=None):
        """Fetch number for each room type in the specified date range."""
        domain = [
            ("relevant_date", ">=", start_date),
            ("relevant_date", "<=", end_date),
        ]
        if room_type_ids:
            domain.append(("room_type_id", "in", room_type_ids))
        records = self.search(domain)
        return [
            {
                "date": record.relevant_date,
                "room_type_id": record.room_type_id.id,
                "number": record.number,
            }
            for record in records
        ]

    @api.model
    def create(self, vals):
        """Create or update record if it already exists."""
        existing_record = self.search(
            [
                ("rate_plan_id", "=", vals.get("rate_plan_id")),
                ("room_type_id", "=", vals.get("room_type_id")),
                ("relevant_date", "=", vals.get("relevant_date")),
            ],
            limit=1,
        )

        if existing_record:
            if vals.get("reset", False):
                vals["number"] = 0
            existing_record.write(vals)
            res = existing_record
        else:
            if vals.get("reset", False):
                vals["number"] = 0
            res = super().create(vals)

        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "rate_plan_update",
            {"rate_plan_id": vals.get("rate_plan_id")},
        )
        return res


class MaxLOSArrival(models.Model):
    _name = "rate_plan.max_los_arrival"
    _description = "Rate plan > MaxLOSArrival"

    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")
    room_type_id = fields.Many2one("triple", string="Room Types Id")
    filter_id = fields.Many2one("rate.plan", string="Extra")
    relevant_date = fields.Date()
    number = fields.Integer()
    reset = fields.Boolean(default=False, string="Reset")

    @api.model
    def get_statuses(self, date_list):
        """Fetch number for a list of dates."""
        domain = [("relevant_date", "in", date_list)]
        records = self.search(domain)
        return {rec.relevant_date.isoformat(): rec.number for rec in records}

    @api.model
    def get_room_statuses(self, room_type_ids=None, start_date=None, end_date=None):
        """Fetch number for each room type in the specified date range."""
        domain = [
            ("relevant_date", ">=", start_date),
            ("relevant_date", "<=", end_date),
        ]
        if room_type_ids:
            domain.append(("room_type_id", "in", room_type_ids))
        records = self.search(domain)
        return [
            {
                "date": record.relevant_date,
                "room_type_id": record.room_type_id.id,
                "number": record.number,
            }
            for record in records
        ]

    @api.model
    def create(self, vals):
        """Create or update record if it already exists."""
        existing_record = self.search(
            [
                ("rate_plan_id", "=", vals.get("rate_plan_id")),
                ("room_type_id", "=", vals.get("room_type_id")),
                ("relevant_date", "=", vals.get("relevant_date")),
            ],
            limit=1,
        )

        if existing_record:
            if vals.get("reset", False):
                vals["number"] = 0
            existing_record.write(vals)
            res = existing_record
        else:
            if vals.get("reset", False):
                vals["number"] = 0
            res = super().create(vals)

        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "rate_plan_update",
            {"rate_plan_id": vals.get("rate_plan_id")},
        )
        return res


class FullParentLOS(models.Model):
    _name = "rate_plan.full_parent_los"
    _description = "Rate plan > FullParentLOS"

    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")
    room_type_id = fields.Many2one("triple", string="Room Types Id")
    filter_id = fields.Many2one("rate.plan", string="Extra")
    relevant_date = fields.Date()
    long_of_stay = fields.Many2many("rate_plan.day_selection", string="Days of Stay")

    @api.model
    def get_statuses(self, date_list):
        """Fetch number for a list of dates."""
        domain = [("relevant_date", "in", date_list)]
        records = self.search(domain)
        return {rec.relevant_date.isoformat(): rec.number for rec in records}

    @api.model
    def get_room_statuses(self, room_type_ids=None, start_date=None, end_date=None):
        """Fetch number for each room type in the specified date range."""
        domain = [
            ("relevant_date", ">=", start_date),
            ("relevant_date", "<=", end_date),
        ]
        if room_type_ids:
            domain.append(("room_type_id", "in", room_type_ids))
        records = self.search(domain)
        return [
            {
                "date": record.relevant_date,
                "room_type_id": record.room_type_id.id,
                "long_of_stay": record.long_of_stay.id,
            }
            for record in records
        ]

    @api.model
    def create(self, vals):
        """Create or update record if it already exists."""
        existing_record = self.search(
            [
                ("rate_plan_id", "=", vals.get("rate_plan_id")),
                ("room_type_id", "=", vals.get("room_type_id")),
                ("relevant_date", "=", vals.get("relevant_date")),
            ],
            limit=1,
        )

        if existing_record:
            existing_record.write(vals)
            res = existing_record
        else:
            res = super().create(vals)

        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "rate_plan_update",
            {"rate_plan_id": vals.get("rate_plan_id")},
        )
        return res


class MinAdvBooking(models.Model):
    _name = "rate_plan.min_adv_booking"
    _description = "Rate plan > MinAdvBooking"

    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")
    room_type_id = fields.Many2one("triple", string="Room Types Id")
    filter_id = fields.Many2one("rate.plan", string="Extra")
    relevant_date = fields.Date()
    number = fields.Integer()
    reset = fields.Boolean(default=False, string="Reset")

    @api.model
    def get_statuses(self, date_list):
        """Fetch number for a list of dates."""
        domain = [("relevant_date", "in", date_list)]
        records = self.search(domain)
        return {rec.relevant_date.isoformat(): rec.number for rec in records}

    @api.model
    def get_room_statuses(self, room_type_ids=None, start_date=None, end_date=None):
        """Fetch number for each room type in the specified date range."""
        domain = [
            ("relevant_date", ">=", start_date),
            ("relevant_date", "<=", end_date),
        ]
        if room_type_ids:
            domain.append(("room_type_id", "in", room_type_ids))
        records = self.search(domain)
        return [
            {
                "date": record.relevant_date,
                "room_type_id": record.room_type_id.id,
                "number": record.number,
            }
            for record in records
        ]

    @api.model
    def create(self, vals):
        """Create or update record if it already exists."""
        existing_record = self.search(
            [
                ("rate_plan_id", "=", vals.get("rate_plan_id")),
                ("room_type_id", "=", vals.get("room_type_id")),
                ("relevant_date", "=", vals.get("relevant_date")),
            ],
            limit=1,
        )

        if existing_record:
            if vals.get("reset", False):
                vals["number"] = 0
            existing_record.write(vals)
            res = existing_record
        else:
            if vals.get("reset", False):
                vals["number"] = 0
            res = super().create(vals)

        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "rate_plan_update",
            {"rate_plan_id": vals.get("rate_plan_id")},
        )
        return res


class MaxAdvBooking(models.Model):
    _name = "rate_plan.max_adv_booking"
    _description = "Rate plan > MaxAdvBooking"

    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")
    room_type_id = fields.Many2one("triple", string="Room Types Id")
    filter_id = fields.Many2one("rate.plan", string="Extra")
    relevant_date = fields.Date()
    number = fields.Integer()
    reset = fields.Boolean(default=False, string="Reset")

    @api.model
    def get_statuses(self, date_list):
        """Fetch number for a list of dates."""
        domain = [("relevant_date", "in", date_list)]
        records = self.search(domain)
        return {rec.relevant_date.isoformat(): rec.number for rec in records}

    @api.model
    def get_room_statuses(self, room_type_ids=None, start_date=None, end_date=None):
        """Fetch number for each room type in the specified date range."""
        domain = [
            ("relevant_date", ">=", start_date),
            ("relevant_date", "<=", end_date),
        ]
        if room_type_ids:
            domain.append(("room_type_id", "in", room_type_ids))
        records = self.search(domain)
        return [
            {
                "date": record.relevant_date,
                "room_type_id": record.room_type_id.id,
                "number": record.number,
            }
            for record in records
        ]

    @api.model
    def create(self, vals):
        """Create or update record if it already exists."""
        existing_record = self.search(
            [
                ("rate_plan_id", "=", vals.get("rate_plan_id")),
                ("room_type_id", "=", vals.get("room_type_id")),
                ("relevant_date", "=", vals.get("relevant_date")),
            ],
            limit=1,
        )

        if existing_record:
            if vals.get("reset", False):
                vals["number"] = 0
            existing_record.write(vals)
            res = existing_record
        else:
            if vals.get("reset", False):
                vals["number"] = 0
            res = super().create(vals)

        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "rate_plan_update",
            {"rate_plan_id": vals.get("rate_plan_id")},
        )
        return res


class CTA(models.Model):
    _name = "rate_plan.cta"
    _description = "Rate plan > CTA"

    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")
    room_type_id = fields.Many2one("triple", string="Room Types Id")
    filter_id = fields.Many2one("rate.plan", string="Extra")
    relevant_date = fields.Date()
    status = fields.Selection(
        [("close", "Close"), ("open", "Open")],
        string="Status",
        default="close",
        required=True,
    )

    @api.model
    def get_statuses(self, date_list):
        """Fetch status for a list of dates."""
        domain = [("relevant_date", "in", date_list)]
        records = self.search(domain)
        return {rec.relevant_date.isoformat(): rec.status for rec in records}

    @api.model
    def get_room_statuses(self, room_type_ids=None, start_date=None, end_date=None):
        domain = [
            ("relevant_date", ">=", start_date),
            ("relevant_date", "<=", end_date),
        ]
        if room_type_ids:
            domain.append(("room_type_id", "in", room_type_ids))
        records = self.search(domain)
        return [
            {
                "date": record.relevant_date,
                "room_type_id": record.room_type_id.id,
                "status": record.status,
            }
            for record in records
        ]

    @api.model
    def create(self, vals):
        existing_record = self.search(
            [
                ("rate_plan_id", "=", vals.get("rate_plan_id")),
                ("room_type_id", "=", vals.get("room_type_id")),
                ("relevant_date", "=", vals.get("relevant_date")),
            ],
            limit=1,
        )

        if existing_record:
            existing_record.write(vals)
            res = existing_record
        else:
            res = super().create(vals)

        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "rate_plan_update",
            {"rate_plan_id": vals.get("rate_plan_id")},
        )
        return res


class RatePlanCTD(models.Model):
    _name = "rate_plan.rate_plan_ctd"
    _description = "Rate plan > CTD"

    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")
    room_type_id = fields.Many2one("triple", string="Room Types Id")
    filter_id = fields.Many2one("rate.plan", string="Extra")
    relevant_date = fields.Date()
    status = fields.Selection(
        [("close", "Close"), ("open", "Open")],
        string="Status",
        default="close",
        required=True,
    )

    @api.model
    def get_statuses(self, date_list):
        """Fetch status for a list of dates."""
        domain = [("relevant_date", "in", date_list)]
        records = self.search(domain)
        return {rec.relevant_date.isoformat(): rec.status for rec in records}

    @api.model
    def get_room_statuses(self, room_type_ids=None, start_date=None, end_date=None):
        domain = [
            ("relevant_date", ">=", start_date),
            ("relevant_date", "<=", end_date),
        ]
        if room_type_ids:
            domain.append(("room_type_id", "in", room_type_ids))
        records = self.search(domain)
        return [
            {
                "date": record.relevant_date,
                "room_type_id": record.room_type_id.id,
                "status": record.status,
            }
            for record in records
        ]

    @api.model
    def create(self, vals):
        existing_record = self.search(
            [
                ("rate_plan_id", "=", vals.get("rate_plan_id")),
                ("room_type_id", "=", vals.get("room_type_id")),
                ("relevant_date", "=", vals.get("relevant_date")),
            ],
            limit=1,
        )

        if existing_record:
            existing_record.write(vals)
            res = existing_record
        else:
            res = super().create(vals)

        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "rate_plan_update",
            {"rate_plan_id": vals.get("rate_plan_id")},
        )
        return res


class CheckInCheckOut(models.Model):
    _name = "rate_plan.check_in.check_out"
    _description = "Rate plan > CheckIn CheckOut"

    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")
    filter_id = fields.Many2one("rate.plan", string="Extra")
    relevant_date = fields.Date()
    checkin_checkout = fields.Many2one(
        "check.in.check.out.roles", string="CheckIn CheckOut"
    )

    # ====================== Multi update ====================== #
    @api.model
    def batch_update_or_create(self, domain, new_vals):
        """Update existing records or create new ones based on the specified domain."""
        records = self.search(domain)
        if records:
            # Update existing records
            records.write(new_vals)
        else:
            # Extract key parts of the domain to use for creating a new record
            create_vals = {}
            for condition in domain:
                field, operator, value = condition
                if operator == "=":
                    create_vals[field] = value
            # Merge with new_vals for creation
            combined_vals = {**create_vals, **new_vals}
            self.create(combined_vals)
        return True

    @api.model
    def get_statuses(self, date_list):
        """Fetch check-in/check-out status for a list of dates."""
        domain = [("relevant_date", "in", date_list)]
        records = self.search(domain)
        return {
            rec.relevant_date.isoformat(): rec.checkin_checkout.name for rec in records
        }

    @api.model
    def get_room_statuses(self, rate_plan_ids=None, start_date=None, end_date=None):
        """Fetch check-in/check-out statuses for specific room types within a date range."""
        domain = [
            ("relevant_date", ">=", start_date),
            ("relevant_date", "<=", end_date),
        ]
        if rate_plan_ids:
            domain.append(("rate_plan_id", "in", rate_plan_ids))
        records = self.search(domain)
        return [
            {
                "date": record.relevant_date,
                "rate_plan_id": record.rate_plan_id.id,
                "checkin_checkout": record.checkin_checkout.name,
            }
            for record in records
        ]

    @api.model
    def create(self, vals):
        """Create or update a check-in/check-out record."""
        existing_record = self.search(
            [
                ("rate_plan_id", "=", vals.get("rate_plan_id")),
                ("relevant_date", "=", vals.get("relevant_date")),
            ],
            limit=1,
        )

        if existing_record:
            # Update existing record if it already exists
            existing_record.write(vals)
            res = existing_record
        else:
            # Create a new record if none exists
            res = super().create(vals)

        # Notify the user interface about the update
        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "rate_plan_update",
            {"rate_plan_id": vals.get("rate_plan_id")},
        )
        return res


class PaymentMethodsRatePlans(models.Model):
    _name = "rate_plan.payment_methods"
    _description = "Rate plan > PaymentMethods"

    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")
    room_type_id = fields.Many2one("triple", string="Room Types Id")
    filter_id = fields.Many2one("rate.plan", string="Extra")
    relevant_date = fields.Date()
    payment_methods = fields.Many2many(
        "payment.methods.for.guests",
        string="Payment Methods",
        relation="payment_methods_payment_method_rel",
        column1="payment_methods_id",
        column2="payment_method_id",
    )

    # ====================== Multi update ====================== #
    @api.model
    def batch_update_or_create(self, domain, new_vals):
        """Update existing records or create new ones based on the specified domain."""
        records = self.search(domain)
        if records:
            records.write(new_vals)
        else:
            # Extract key parts of the domain to use for creating a new record
            create_vals = {}
            for condition in domain:
                field, operator, value = condition
                if operator == "=":
                    create_vals[field] = value
            # Merge with new_vals for creation
            combined_vals = {**create_vals, **new_vals}
            self.create(combined_vals)
        return True

    @api.model
    def get_statuses(self, date_list):
        """Fetch payment methods for a list of dates."""
        domain = [("relevant_date", "in", date_list)]
        records = self.search(domain)
        return {
            rec.relevant_date.isoformat(): rec.payment_methods.ids for rec in records
        }

    @api.model
    def get_room_statuses(self, room_type_ids=None, start_date=None, end_date=None):
        """Fetch payment methods for a specific room type and date range."""
        domain = [
            ("relevant_date", ">=", start_date),
            ("relevant_date", "<=", end_date),
        ]
        if room_type_ids:
            domain.append(("room_type_id", "in", room_type_ids))
        records = self.search(domain)
        return [
            {
                "date": record.relevant_date,
                "room_type_id": record.room_type_id.id,
                "payment_methods": record.payment_methods.ids,
            }
            for record in records
        ]

    @api.model
    def create(self, vals):
        """Create or update a record if it already exists."""
        existing_record = self.search(
            [
                ("rate_plan_id", "=", vals.get("rate_plan_id")),
                ("room_type_id", "=", vals.get("room_type_id")),
                ("relevant_date", "=", vals.get("relevant_date")),
            ],
            limit=1,
        )

        if existing_record:
            existing_record.write({"payment_methods": [(6, 0, [])]})
            existing_record.write(vals)
            res = existing_record
        else:
            res = super().create(vals)

        # Notify about the rate plan update
        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "rate_plan_update",
            {"rate_plan_id": vals.get("rate_plan_id")},
        )
        return res

    def write(self, vals):
        """Ensure payment_methods are not duplicated or copied if empty."""
        if "payment_methods" in vals:
            for record in self:
                # Check if the operation is of type (6, 0, [])
                if vals["payment_methods"][0][0] == 6:
                    new_methods = vals["payment_methods"][0][2]
                    if not new_methods:
                        vals["payment_methods"] = [
                            (6, 0, [])
                        ]  # Clear payment methods if new value is empty
                    else:
                        existing_methods = record.payment_methods.ids
                        combined_methods = list(set(existing_methods + new_methods))
                        vals["payment_methods"] = [(6, 0, combined_methods)]
                else:
                    # Handle other operations like (4, id)
                    new_methods = [
                        method_id
                        for operation, method_id in vals["payment_methods"]
                        if operation == 4
                    ]
                    if new_methods:
                        existing_methods = record.payment_methods.ids
                        combined_methods = list(set(existing_methods + new_methods))
                        vals["payment_methods"] = [(6, 0, combined_methods)]

        return super().write(vals)


class PaymentMethodsRatePlansWizard(models.Model):
    _name = "payment_methods_rate_plans.wizard"
    _description = "Payment Methods Rates Plans Generate Wizard"

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._generate_rate_plans()
        return record

    def _generate_rate_plans(self):
        start_date = fields.Date.from_string(self.start_date)
        end_date = fields.Date.from_string(self.end_date)

        rate_plans = self.env["rate.plan"].search([])
        room_types = self.env["triple"].search([])

        for rate_plan in rate_plans:
            for room_type in room_types:
                date = start_date
                while date <= end_date:
                    existing_entry = self.env["rate_plan.payment_methods"].search(
                        [
                            ("rate_plan_id", "=", rate_plan.id),
                            ("room_type_id", "=", room_type.id),
                            ("relevant_date", "=", date),
                        ]
                    )
                    if not existing_entry:
                        payment_methods = self.env["payment.methods.for.guests"].search(
                            [], limit=1
                        )
                        if not payment_methods:
                            raise UserError(
                                "No payment methods found. Please create a payment method first."
                            )

                        self.env["rate_plan.payment_methods"].create(
                            {
                                "rate_plan_id": rate_plan.id,
                                "room_type_id": room_type.id,
                                "relevant_date": date,
                                "payment_methods": [(6, 0, payment_methods.ids)],
                            }
                        )
                    date += timedelta(days=1)


class StayControls(models.Model):
    _name = "rate_plan.stay_controls"
    _description = "Rate plan > StayControls"

    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")
    room_type_id = fields.Many2one("triple", string="Room Types Id")
    guest_id = fields.Many2one(
        "room_type.guests", string="Guest", domain="[('room_type', '=', room_type_id)]"
    )
    child_age_range = fields.Many2one(
        "child.age.range",
        string="Child Age Range",
        domain="[('room_type', '=', room_type_id)]",
    )
    filter_id = fields.Many2one("room_type.guests", string="Extra")
    relevant_date = fields.Date()
    status = fields.Selection(
        [("close", "Close"), ("open", "Open")],
        string="Status",
        default="close",
        required=True,
    )

    @api.model
    def batch_update_or_create(self, domain, new_vals):
        """Update existing records or create new ones based on the specified domain."""
        records = self.search(domain)
        if records:
            records.write(new_vals)
        else:
            create_vals = {}
            for condition in domain:
                field, operator, value = condition
                if operator == "=":
                    create_vals[field] = value
            combined_vals = {**create_vals, **new_vals}
            self.create(combined_vals)
        return True

    @api.model
    def get_stay_controls(self, date_list):
        """Fetch stay controls for a list of dates."""
        domain = [("relevant_date", "in", date_list)]
        records = self.search(domain)
        return {rec.relevant_date.isoformat(): rec.status for rec in records}

    @api.model
    def get_room_stay_controls(
        self, room_type_ids=None, start_date=None, end_date=None
    ):
        domain = [
            ("relevant_date", ">=", start_date),
            ("relevant_date", "<=", end_date),
        ]
        if room_type_ids:
            domain.append(("room_type_id", "in", room_type_ids))
        records = self.search(domain)
        return [
            {
                "date": record.relevant_date,
                "room_type_id": record.room_type_id.id,
                "status": record.status,
            }
            for record in records
        ]

    @api.model
    def create(self, vals):
        """Override create method to check for existing records and update if found."""
        if not vals.get("guest_id") and not vals.get("child_age_range"):
            raise UserError("Either guest_id or child_age_range must be provided.")
        elif vals.get("guest_id") and vals.get("child_age_range"):
            raise UserError(
                "Only one of guest_id or child_age_range should be provided."
            )

        existing_record = self.search(
            [
                ("rate_plan_id", "=", vals.get("rate_plan_id")),
                ("room_type_id", "=", vals.get("room_type_id")),
                ("guest_id", "=", vals.get("guest_id")),
                ("child_age_range", "=", vals.get("child_age_range")),
                ("relevant_date", "=", vals.get("relevant_date")),
            ],
            limit=1,
        )

        if existing_record:
            existing_record.write(vals)
            res = existing_record
        else:
            res = super().create(vals)

        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "rate_plan_update",
            {"rate_plan_id": vals.get("rate_plan_id")},
        )
        return res

    @api.model
    def write(self, vals):
        """Override write method."""
        res = super().write(vals)
        return res


class Price(models.Model):
    _name = "rate_plan.price"
    _description = "Rate plan > Price"
    _rec_name = "price"

    rate_plan_id = fields.Many2one("rate.plan", string="Rate Plan")
    room_type_id = fields.Many2one("triple", string="Room Types Id")
    guest_id = fields.Many2one(
        "room_type.guests", string="Guest", domain="[('room_type', '=', room_type_id)]"
    )
    child_age_range = fields.Many2one(
        "child.age.range",
        string="Child Age Range",
        # domain="[('room_type', '=', room_type_id)]",
    )
    filter_id = fields.Many2one(
        "room_type.guests",
        string="Guest (extra)",
        domain="[('room_type', '=', room_type_id)]",
    )
    relevant_date = fields.Date()
    price = fields.Float("Price")

    # ====================== Multi update ====================== #
    @api.model
    def batch_update_or_create(self, domain, new_vals):
        """Update existing records or create new ones based on the specified domain."""
        records = self.search(domain)
        if records:
            records.write(new_vals)
        else:
            # Extract key parts of the domain to use for creating a new record
            create_vals = {}
            for condition in domain:
                field, operator, value = condition
                if operator == "=":
                    create_vals[field] = value
            # Merge with new_vals for creation
            combined_vals = {**create_vals, **new_vals}
            self.create(combined_vals)
        return True

    @api.model
    def get_prices(self, date_list):
        """Fetch price for a list of dates."""
        domain = [("relevant_date", "in", date_list)]
        records = self.search(domain)
        return {rec.relevant_date.isoformat(): rec.price for rec in records}

    @api.model
    def get_room_prices(self, room_type_ids=None, start_date=None, end_date=None):
        domain = [
            ("relevant_date", ">=", start_date),
            ("relevant_date", "<=", end_date),
        ]
        if room_type_ids:
            domain.append(("room_type_id", "in", room_type_ids))
        records = self.search(domain)
        return [
            {
                "date": record.relevant_date,
                "room_type_id": record.room_type_id.id,
                "price": record.price,
            }
            for record in records
        ]

    @api.model
    def create(self, vals):
        """Override create method to check for existing records and update if found."""
        if not vals.get("guest_id") and not vals.get("child_age_range"):
            raise UserError("Either guest_id or child_age_range must be provided.")
        elif vals.get("guest_id") and vals.get("child_age_range"):
            raise UserError(
                "Only one of guest_id or child_age_range should be provided."
            )

        existing_record = self.search(
            [
                ("rate_plan_id", "=", vals.get("rate_plan_id")),
                ("room_type_id", "=", vals.get("room_type_id")),
                ("guest_id", "=", vals.get("guest_id")),
                ("child_age_range", "=", vals.get("child_age_range")),
                ("relevant_date", "=", vals.get("relevant_date")),
            ],
            limit=1,
        )

        if existing_record:
            existing_record.write(vals)
            res = existing_record
        else:
            res = super().create(vals)

        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "rate_plan_update",
            {"rate_plan_id": vals.get("rate_plan_id")},
        )
        return res

    @api.model
    def write(self, vals):
        """Override write method to check for guest_id and child_age_range."""
        # Check if both guest_id and child_age_range are missing or both are present
        if (
            not vals.get("guest_id")
            and not vals.get("child_age_range")
            and "guest_id" not in vals
            and "child_age_range" not in vals
        ):
            raise UserError("Either guest_id or child_age_range must be provided.")
        elif (
            vals.get("guest_id")
            and vals.get("child_age_range")
            and "guest_id" in vals
            and "child_age_range" in vals
        ):
            raise UserError(
                "Only one of guest_id or child_age_range should be provided."
            )

        res = super().write(vals)

        return res
