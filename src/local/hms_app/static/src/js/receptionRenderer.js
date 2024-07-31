/* @odoo-module */

import {registry} from "@web/core/registry";
import {listView} from "@web/views/list/list_view";
import {ReceptionRenderer} from "./reception";
import {FrontDeskController} from "./frontDeskController";

registry.category("views").add("Reception", {
  ...listView,
  Renderer: ReceptionRenderer,
  Controller: FrontDeskController,
});
