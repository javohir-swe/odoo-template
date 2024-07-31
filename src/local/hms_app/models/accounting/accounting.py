# class BookingMonthlyReconciliation(models.Model):
#     _name = "booking.monthly.reconciliation"
#     _description = "Monthly Reconciliation"
#
#     detail_ids = fields.One2many(
#         "booking.monthly.detail", "reconciliation_id", string="Details"
#     )
#     month = fields.Date(string="Month", required=True)
#     total_amount = fields.Float(
#         string="Total Amount", compute="_compute_booking_data", store=True
#     )
#     booking_count = fields.Integer(
#         string="Booking Count", compute="_compute_booking_data", store=True
#     )
#
#     @api.depends("month")
#     def _compute_booking_data(self):
#         for record in self:
#             if not record.month:
#                 record.booking_count = 0
#                 record.total_amount = 0.0
#                 continue
#
#             start_date = record.month.replace(day=1)
#             end_date = (start_date + relativedelta(months=1)) - timedelta(days=1)
#
#             bookings = self.env["booking"].search(
#                 [
#                     ("check_in_date", ">=", start_date),
#                     ("check_in_date", "<=", end_date),
#                     ("guest_id", "!=", False),
#                 ]
#             )
#
#             record.booking_count = len(bookings)
#             record.total_amount = sum(booking.total for booking in bookings)
#
#             details = []
#             for booking in bookings:
#                 details.append(
#                     (
#                         0,
#                         0,
#                         {
#                             "month": record.month,
#                             "guest_id": booking.guest_id.id,
#                             "total_amount": booking.total,
#                             "booking_count": 1,
#                             "reconciliation_id": record.id,
#                         },
#                     )
#                 )
#             record.detail_ids = details
#
#     @api.model
#     def create(self, vals):
#         record = super().create(vals)
#         record._compute_booking_data()
#         return record
#
#     def write(self, vals):
#         result = super().write(vals)
#         if "month" in vals:
#             self._compute_booking_data()
#         return result


# class BookingMonthlyDetail(models.Model):
#     _name = "booking.monthly.detail"
#     _description = "Booking Monthly Detail"
#
#     month = fields.Date(string="Month", required=True)
#     guest_id = fields.Many2one("guest", string="Guest", required=True)
#     total_amount = fields.Float(string="Total Amount", required=True)
#     booking_count = fields.Integer(string="Booking Count", required=True)
#     reconciliation_id = fields.Many2one(
#         "booking.monthly.reconciliation", string="Reconciliation", ondelete="cascade"
#     )
