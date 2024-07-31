/* @odoo-module */

import {registry} from "@web/core/registry";
import {listView} from "@web/views/list/list_view";
import {FrontDeskRenderer} from "./frontDesk";
import {FrontDeskController} from "./frontDeskController";

registry.category("views").add("FrontDesk", {
  ...listView,
  Renderer: FrontDeskRenderer,
  Controller: FrontDeskController,
});
