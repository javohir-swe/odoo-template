/* @odoo-module */

import {Component, useState} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {standardFieldProps} from "@web/views/fields/standard_field_props";

export class GuestProfile extends Component {
  static props = {
    ...standardFieldProps,
  };
  setup() {
    super.setup();
    this.state = useState({
      documentTab: "Not specified",
    });
    this.documentType = this.documentType.bind(this);
  }

  documentType(e) {
    this.state.documentTab = e.target.value;
  }
}

GuestProfile.template = "hms_app.GuestProfile";

export const guestProfile = {
  component: GuestProfile,
  supportedTypes: ["char"],
};

registry.category("fields").add("guest_profile", guestProfile);
