/** @odoo-module **/

import {registry} from "@web/core/registry";

function openPdfReport(action) {
  const reportUrl = `/report/pdf/${action.report_name}/${action.context.active_ids.join(
    ","
  )}`;
  window.open(reportUrl, "_blank");
}

registry.category("ir.actions.report handlers").add("qweb-pdf", openPdfReport);
