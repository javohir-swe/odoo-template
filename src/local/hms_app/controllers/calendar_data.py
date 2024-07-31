from odoo import http
from odoo.http import request


class RatePlanController(http.Controller):

    @http.route("/rate_plan/closed_status", type="json", auth="user")
    def get_closed_status(self, rate_plan_id):
        closed_records = request.env["rate_plan.closed"].search(
            [("rate_plan_id", "=", rate_plan_id)]
        )
        data = []
        for record in closed_records:
            data.append(
                {
                    "id": record.id,
                    "rate_plan_id": record.rate_plan_id.id,
                    "room_type_id": record.room_type_id.id,
                    "relevant_date": record.relevant_date,
                    "status": record.status,
                }
            )
        return data


# ====================== Multi update ====================== #
class BatchUpdateController(http.Controller):

    @http.route("/batch_update_or_create", type="json", auth="user")
    def batch_update_or_create(self, domain, new_vals):
        result = request.env["rate_plan.closed"].batch_update_or_create(
            domain, new_vals
        )
        return {"result": result}


# ====================== Multi update ====================== #
