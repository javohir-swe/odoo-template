/* @odoo-module */

import {registry} from "@web/core/registry";
import {listView} from "@web/views/list/list_view";
import {AvailabilitySettingsRenderer} from "./availabilitySettings";
import {FrontDeskController} from "./frontDeskController";

registry.category("views").add("AvailabilitySettings", {
  ...listView,
  Renderer: AvailabilitySettingsRenderer,
  Controller: FrontDeskController,
});
