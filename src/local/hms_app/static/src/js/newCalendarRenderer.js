/* @odoo-module */

import {registry} from "@web/core/registry";
import {calendarView} from "@web/views/calendar/calendar_view";
import {CustomCalendarRenderer} from "./newCalendarView";
import {CalendarArchParser} from "./newArchParser";
registry.category("views").add("NewCalendarTable", {
  ...calendarView,
  Renderer: CustomCalendarRenderer,
  ArchParser: CalendarArchParser,
});
