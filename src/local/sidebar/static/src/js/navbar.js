/** @odoo-module */

import {Component, useState, onMounted, onWillUnmount, useRef} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class NewNavbar extends Component {
  setup() {
    this.userService = useService("user");
    this.action = useService("action");
    this.state = useState({
      user: this.userService,
      dropdownVisible: false,
    });
    this.toggleDropdown = this.toggleDropdown.bind(this);
    this.handleClickOutside = this.handleClickOutside.bind(this);
    this.navigateToUserProfile = this.navigateToUserProfile.bind(this);

    // Reference to the component's DOM element
    this.componentRef = useRef("componentRef");

    // Add event listener for clicks outside the dropdown
    onMounted(() => {
      document.addEventListener("click", this.handleClickOutside);
    });

    // Clean up the event listener
    onWillUnmount(() => {
      document.removeEventListener("click", this.handleClickOutside);
    });
  }

  toggleDropdown(event) {
    // Prevent the click event from propagating to the document
    event.stopPropagation();
    this.state.dropdownVisible = !this.state.dropdownVisible;
  }

  handleClickOutside(event) {
    const componentElement = this.componentRef.el;
    if (
      this.state.dropdownVisible &&
      componentElement &&
      !componentElement.contains(event.target)
    ) {
      this.state.dropdownVisible = false;
    }
  }

  navigateToUserProfile() {
    this.state.dropdownVisible = false; // Hide the dropdown
    this.action.doAction(
      {
        type: "ir.actions.act_window",
        res_model: "res.users",
        views: [[false, "form"]],
        res_id: this.state.user.userId,
      },
      {clearBreadcrumbs: true}
    );
  }
  goSettings() {
    this.state.dropdownVisible = false;
    this.action
      .doAction(
        {
          type: "ir.actions.act_window",
          res_model: "res.config.settings",
          name: "Settings",
          target: "current",
          views: [[false, "form"]],
        },
        {clearBreadcrumbs: true}
      )
      .catch((error) => {
        console.error(`Action does not exist or failed:`, error);
        alert(`The action does not exist.`);
      });
  }
}

NewNavbar.template = "hms.ProfileComponent";
