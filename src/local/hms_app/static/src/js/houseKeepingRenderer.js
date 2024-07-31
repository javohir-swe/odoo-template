/* @odoo-module */

import {registry} from "@web/core/registry";
import {listView} from "@web/views/list/list_view";
import {HouseKeeping} from "./houseKeeping";
import {FrontDeskController} from "./frontDeskController";

registry.category("views").add("HouseKeeping", {
  ...listView,
  Renderer: HouseKeeping,
  Controller: FrontDeskController,
});
