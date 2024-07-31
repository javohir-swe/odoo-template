# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class HmsApp(http.Controller):
    @http.route("/hms_app/hms_app", auth="public")
    def index(self, **kw):
        return "Hello, world"

    @http.route("/hms_app/hms_app/objects", auth="public")
    def list(self, **kw):
        return http.request.render(
            "hms_app.listing",
            {
                "root": "/hms_app/hms_app",
                "objects": http.request.env["hms_app.hms_app"].search([]),
            },
        )

    @http.route(
        '/hms_app/hms_app/objects/<model("hms_app.hms_app"):obj>', auth="public"
    )
    def object(self, obj, **kw):
        return http.request.render("hms_app.object", {"object": obj})

    class DayPilotSchedulerController(http.Controller):
        @http.route('/scheduler', auth='user', website=True)
        def scheduler(self, **kwargs):
            return request.render("hms_app.scheduler_template", {})
