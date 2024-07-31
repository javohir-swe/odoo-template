/** @odoo-module */

import {ListController} from "@web/views/list/list_controller";
import {onMounted, onWillUnmount} from "@odoo/owl";
export class FrontDeskController extends ListController {
  setup() {
    super.setup();
    onMounted(() => {
      let controlPanel = document.getElementsByClassName("o_control_panel");
      if (controlPanel) {
        this.addClass(controlPanel, "d-none");
      }
    });
    onWillUnmount(() => {
      let controlPanel = document.getElementsByClassName("o_control_panel");
      if (controlPanel) {
        this.removeClass(controlPanel, "d-none");
      }
    });
  }
  addClass(elements, className) {
    for (var i = 0; i < elements.length; i++) {
      var element = elements[i];
      if (element.classList) {
        element.classList.add(className);
      } else {
        element.className += " " + className;
      }
    }
  }
  removeClass(elements, className) {
    for (var i = 0; i < elements.length; i++) {
      var element = elements[i];
      if (element.classList) {
        element.classList.remove(className);
      } else {
        element.className = element.className.replace(
          new RegExp("(^|\\b)" + className.split(" ").join("|") + "(\\b|$)", "gi"),
          " "
        );
      }
    }
  }
}

FrontDeskController.template = "hms_app.FrontDeskController";
