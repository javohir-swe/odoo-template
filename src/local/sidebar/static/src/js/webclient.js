/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { WebClient } from "@web/webclient/webclient";
import { SideBar } from "./sidebar";
import { NewNavbar } from "./navbar";
import { Footer } from "./footer";
patch(WebClient, {
  components: {
    ...WebClient.components,
    SideBar,
    NewNavbar,
    Footer,
  },
  
});

patch(WebClient.prototype, {
  setup() {
      super.setup(this, arguments);
      this.title.setParts({ zopenerp: "MOVO" });
  },
});
WebClient.template = "hms.WebClient";
