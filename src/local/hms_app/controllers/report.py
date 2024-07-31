from odoo import http


class ReportController(http.Controller):
    @http.route("/report/download/<int:report_id>", type="http", auth="user")
    def download_report(self, report_id):
        report = http.request.env["booking.monthly.reconciliation"].browse(report_id)
        context = {
            "guest_id": report.guest_id.id,
            # Other context variables as needed
        }
        return self._generate_report(report, context)

    def _generate_report(self, report, context):
        # Prepare data and context
        report.ensure_one()  # Assuming only one record
        data = {
            "docs": [report],
            "context": context,
        }
        return http.request.env.ref("hms_app.report_booking_guest_document").render(
            data
        )
