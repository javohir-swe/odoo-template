/* @odoo-module */

import {Component, useState, onMounted, onWillStart, onWillUnmount} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {standardFieldProps} from "@web/views/fields/standard_field_props";
import {loadJS} from "@web/core/assets";

class GroupBooking extends Component {
  static props = {
    ...standardFieldProps,
  };
  setup() {
    super.setup();
    this.rpc = useService("rpc");
    this.orm = useService("orm");
    this.actionService = useService("action");
    onWillStart(async () => {
      await loadJS(
        "https://cdnjs.cloudflare.com/ajax/libs/toastify-js/1.6.1/toastify.js"
      );
    });
    this.state = useState({
      records: this.props.record,
      roomsData: [],
      activeTab: "General",
      times: [],
    });

    onMounted(() => {
      this.showToastTest();
      this.generateTimes();
    });
  }
  setActiveTab(tab) {
    this.state.activeTab = tab;
  }

  showToastTest() {
    Toastify({
      text: "Mazza qilib uxlash kerak",
      duration: 3000,
      // destination: "https://github.com/apvarun/toastify-js",
      // newWindow: true,
      className: "bg-danger",
      close: true,
      gravity: "top", // `top` or `bottom`
      position: "right", // `left`, `center` or `right`
      stopOnFocus: true, // Prevents dismissing of toast on hover
      // style: {
      //   background: "#fff",
      // },
    }).showToast();
  }

  generateTimes() {
    const times = [];
    for (let hour = 0; hour < 24; hour++) {
      for (let minutes = 0; minutes < 60; minutes += 30) {
        const time = `${this.padTime(hour)}:${this.padTime(minutes)}`;
        times.push(time);
      }
    }
    times.push("23:59");
    this.state.times = times;
    return times;
  }

  padTime(number) {
    return number.toString().padStart(2, "0");
  }
}

GroupBooking.template = "hms_app.GroupBooking";

export const groupBooking = {
  component: GroupBooking,
  supportedTypes: ["char"],
};

registry.category("fields").add("group_booking", groupBooking);
