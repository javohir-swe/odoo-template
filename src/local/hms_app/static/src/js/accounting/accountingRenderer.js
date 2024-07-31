/* @odoo-module */

import {registry} from "@web/core/registry";
import {listView} from "@web/views/list/list_view";
import {AccountingRenderer} from "./accounting";

registry.category("views").add("Accounting", {
  ...listView,
  Renderer: AccountingRenderer,
});
