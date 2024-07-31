/* @odoo-module */
import {registry} from "@web/core/registry";
import {listView} from "@web/views/list/list_view";
import {SalesAndOccupancyViews} from "./salesAndOccupancyViews";
import {FrontDeskController} from "./frontDeskController";

registry.category("views").add("SalesAndOccupancyViews", {
  ...listView,
  Renderer: SalesAndOccupancyViews,
  Controller: FrontDeskController,
});
