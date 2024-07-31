/* @odoo-module */

import {registry} from "@web/core/registry";
import {listView} from "@web/views/list/list_view";
import {DetailedRenderer} from "./detailed";

registry.category("views").add("Detailed", {
  ...listView,
  Renderer: DetailedRenderer,
});
