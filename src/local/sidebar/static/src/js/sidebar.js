/** @odoo-module */

import {onMounted, useState, Component} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class SideBar extends Component {
  setup() {
    super.setup();
    this.actionService = useService("action");
    this.state = useState({
      menuItems: [],
      activeMenuItem: localStorage.getItem("activeMenuItem") || null,
      sectionVisibility: {},
      sidebarCollapse: false,
      oldkey: null,
      activeDropdown: null, // For tracking the active dropdown
    });

    this.toggleSectionVisibility = this.toggleSectionVisibility.bind(this);
    this.toggleSidebar = this.toggleSidebar.bind(this);
    this.showDropdown = this.showDropdown.bind(this);
    this.hideDropdown = this.hideDropdown.bind(this);

    onMounted(() => {
      this.fetchMenuItems();
    });
  }

  async fetchMenuItems() {
    const menuItems = [
      {
        name: "Dashboard",
        icon: "/sidebar/static/description/yordamchi.svg",
        model: "sales.and.occupancy",
        // children: [
        //   {model: "", name: "Sales distribution (Soon)"},
        //   {model: "", name: "Occupancy rate (Soon)"},
        //   {model: "occupancy.rate", name: "Occupancy pickup (Soon)"},
        //   {model: "", name: "Demand calendar (Soon)"},
        //   {model: "booking.window", name: "Booking Window (Soon)"},
        //   {model: "booking.cancellations", name: "Booking cancellations (Soon)"},
        // ],
      },
      {
        name: "Room Management",
        icon: "/sidebar/static/description/roommng.svg",
        children: [
          {model: "triple", name: "Room Types"},
          // {
          //   name: "Room Types", children: [
          //     // { model: "room_image", name: "Room Photos" },
          //     // { model: "accommodation_offer", name: "Accommodation Offers" },
          //     // { model: "smoking_in_room", name: "Smoking In Room" },
          //     // { model: "room_type.guests", name: "Guests" },
          //   ]
          // },
          {
            name: "Availability",
            children: [
              {model: "main.availability", name: "Main Availability", view: "calendar"},
              // { model: "availability.online_sales_role", name: "Online Sales Roles" },
              {model: "availability_settings", name: "Settings"},
              {model: "availability.manager", name: "Availability Manager"},
              // { model: "availability.default_data", name: "Default Data" },
              // { model: "default.availability", name: "Default Availability" },
            ],
          },
          {model: "rate.plan", name: "Rate plan"},
          // {
          //   name: "Rate Plan", children: [
          //     { model: "types", name: "Types" },
          //     { model: "point.of.sale", name: "Point of sale" },
          //     { model: "currency", name: "Rate plan currencies" },
          //   ]
          // },
          // {
          //   name: "Extras", children: [
          //     { model: "rate_plan.extras", name: "Extras" },
          //     { model: "rate_plan.service", name: "Extras Service" },
          //   ]
          // },
          {model: "promotion", name: "Promotion"},
          // {
          //   name: "Promotions", children: [
          //     { model: "promotion.types", name: "Promotion Types" },
          //   ]
          // }
        ],
      },
      {
        name: "Property Settings",
        icon: "/sidebar/static/description/property.svg",
        children: [
          {model: "res.config.settings", name: "Settings", view: "form"},
          // {
          //   name: "Main Settings", children: [
          //     { model: "base.types", name: "Building types" },
          //   ]
          // },
          {model: "payment.methods.for.guests", name: "Payment Methods"},
          {model: "comments", name: "Comments", view: "form"},
          {model: "check.in.check.out.roles", name: "Early check-in/Late check-out"},
          // {
          //   name: "Check-in / Check-out", children: [
          //     { model: "all.times", name: "All Times" },
          //   ]
          // },
          {model: "rule.name", name: "Cancellation Policy"},
          // {
          //   name: "Cancellation Policy", children: [
          //     { model: "cancellation.terms", name: "Cancellation terms" },
          //   ]
          // },
          // {model: "services.settings", name: "Extra services"},
          {
            name: "Extra services",
            children: [
              {model: "group.services", name: "Groups of services"},
              {model: "services.settings", name: "Services"},
            ],
          },
          {
            name: "Transfers",
            children: [
              {model: "vehicles", name: "Vehicles"},
              {model: "transport.companies", name: "Transport companies"},
              {model: "transfers", name: "All transfers"},
            ],
          },
          {
            name: "Promo codes",
            children: [
              {model: "promo_code.groups", name: "Promo Code Groups"},
              {model: "property_settings.promo_code", name: "Promo Codes"},
              {
                model: "promo.code.generate.wizard",
                name: "Generate Promo Codes",
                view: "form",
                target: "new",
              },
            ],
          },
          // {
          //   name: "Transfers", children: [
          //     { model: "transfer.type", name: "Transfer Types" },
          //     { model: "vehicles", name: "Vehicles" },
          //     { model: "transport.companies", name: "Transport Companies" },
          //     { model: "station", name: "Stations" },
          //   ]
          // },
          {model: "rounding.rule", name: "Rounding policy"},
          // { model: "city", name: "City" },
          // { model: "state", name: "State" },
          // { model: "child.age.range", name: "Child age range" },
        ],
      },
      {
        name: "Property Management",
        icon: "/sidebar/static/description/property.svg",
        children: [
          {model: "booking", name: "Front desk"},
          // {
          //   name: "Front Desk",
          //   children: [
          //     // {model: "group_booking", name: "Group Booking"},
          //   ],
          // },
          // {model: "reception", name: "Reception"},
          // {
          //   name: "All countries", children: [
          //     { model: "countries", name: "Countries" },
          //   ]
          // },
          // {
          //   name: "Company Management", children: [
          //     { model: "company", name: "Companies"},
          //     { model: "addition.account.number", name: "Account Numbers" },
          //     { model: "responsible.person", name: "Responsible Persons" },
          //   ]
          // },
          {model: "reception", name: "Reception"},
          {model: "notes_and_instructions", name: "Notes and Instructions"},
          {model: "property.building", name: "Buildings"},
          {model: "room.inventory", name: "Room Inventory"},
          {
            model: "room_inventory.generate",
            name: "Generate Room Inventory",
            view: "form",
            target: "new",
          },
          {model: "room_inventory.housekeeping", name: "Housekeeping"},
          {model: "guest", name: "Guest Profile"},
          {model: "company", name: "Companies"},
          // {model: "settings", name: "Settings", view: "form"},

          // {
          //   name: "Guests Management", children: [
          //     { model: "guest", name: "Guests" },
          //     { model: "legal.representative", name: "Representatives" },
          //   ]
          // },
        ],
      },
      // {
      //   name: "Reputation Manager",
      //   icon: "/sidebar/static/description/tie.svg",
      //   children: [],
      // },
      // {
      //   name: "Website Builder",
      //   icon: "/sidebar/static/description/device-desktop.svg",
      //   children: [],
      // },
      {
        name: "Automated Emails",
        icon: "/sidebar/static/description/message-2.svg",
        children: [{model: "mail.list", name: "Mail List", view: "form"}],
      },
      {
        name: "Accounting",
        icon: "/sidebar/static/description/file-export.svg",
        children: [{model: "booking.reconciliation", name: "Booking reconciliation"}],
      },
      // {
      //   name: "Reports (soon)",
      //   icon: "/sidebar/static/description/report.svg",
      //   children: [],
      // },
      // {
      //   name: "Channel Manager (soon)",
      //   icon: "/sidebar/static/description/sitemap.svg",
      //   children: [],
      // },
      // {
      //   name: "Price Monitor",
      //   icon: "/sidebar/static/description/scale.svg",
      //   children: [],
      // },
      // {
      //   name: "Guest relations",
      //   icon: "/sidebar/static/description/home-stats.svg",
      //   children: [],
      // },
      // {
      //   name: "Booking Engine",
      //   icon: "/sidebar/static/description/layout-grid.svg",
      //   children: [],
      // },
      // {
      //   icon: "/sidebar/static/description/home-stats.svg",
      //   model: "res.config.settings",
      //   name: "Settings",
      //   view: "form",
      // },
      {
        icon: "/sidebar/static/description/app.svg",
        model: "ir.module.module",
        name: "Apps",
        view: "kanban",
      },
    ];

    this.state.menuItems = menuItems;
    const sectionVisibility = {};
    this.initializeVisibilityState(menuItems, sectionVisibility);
    this.state.sectionVisibility = sectionVisibility;
  }

  initializeVisibilityState(menuItems, visibilityState, parentKey = "") {
    menuItems.forEach((item, index) => {
      const key = parentKey ? `${parentKey}-${index}` : `${index}`;
      visibilityState[key] = false;
      if (item.children) {
        this.initializeVisibilityState(item.children, visibilityState, key);
      }
    });
  }

  onMenuItemClick(menuItem) {
    this.state.activeMenuItem = menuItem.model;
    localStorage.setItem("activeMenuItem", menuItem.model);
    this.actionService
      .doAction(
        {
          type: "ir.actions.act_window",
          res_model: menuItem.model,
          name: menuItem.name,
          // target: "current",
          view_mode: ["list"],
          views: [
            [false, menuItem.view || "list"],
            [false, menuItem.view == "form" ? "list" : "form"],
          ],
          target: menuItem.target || "current",
        },
        {clearBreadcrumbs: true}
      )
      .catch((error) => {
        console.error(`Action ${menuItem.model} does not exist or failed:`, error);
        alert(`The action '${menuItem.model}' does not exist.`);
      });
  }

  toggleSectionVisibility(key) {
    let oldKeyConst = this.state.oldkey;
    const newSectionVisibility = {...this.state.sectionVisibility};
    newSectionVisibility[key] = !newSectionVisibility[key];
    if (!key.includes(this.state.oldkey)) {
      newSectionVisibility[this.state.oldkey] = false;
    }
    if (oldKeyConst) {
      if (!key.includes("parent-" + oldKeyConst.split("-")[1])) {
        newSectionVisibility["parent-" + oldKeyConst.split("-")[1]] = false;
      }
    }
    this.state.sectionVisibility = newSectionVisibility;
    this.state.oldkey = key;
  }

  toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const sidebarContainer = document.getElementById("container_action");

    if (sidebar) {
      this.state.sidebarCollapse = !this.state.sidebarCollapse;
      sidebar.classList.toggle("collapsed");

      if (this.state.sidebarCollapse) {
        const newSectionVisibility = {...this.state.sectionVisibility};
        Object.keys(newSectionVisibility).forEach((key) => {
          newSectionVisibility[key] = false;
        });
        this.state.sectionVisibility = newSectionVisibility;
      }
    }
    if (sidebarContainer) {
      if (this.state.sidebarCollapse) {
        sidebarContainer.classList.add("sidebar-close");
        sidebarContainer.classList.remove("sidebar-open");
      } else {
        sidebarContainer.classList.add("sidebar-open");
        sidebarContainer.classList.remove("sidebar-close");
      }
    }
  }

  showDropdown(key) {
    if (this.state.activeDropdown !== key) {
      this.state.activeDropdown = key;
    }
  }

  hideDropdown(key) {
    if (this.state.activeDropdown === key) {
      this.state.activeDropdown = null;
    }
  }
}

SideBar.template = "sidebar.SidebarControllerListView";
