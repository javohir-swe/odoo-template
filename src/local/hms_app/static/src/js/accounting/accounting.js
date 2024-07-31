/** @odoo-module **/

import {ListRenderer} from "@web/views/list/list_renderer";
import {useState, onMounted, onWillUnmount, onWillStart} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class AccountingRenderer extends ListRenderer {
  setup() {
    super.setup();
    this.action = useService("action");
    this.state = useState({
      monthItems: [],
      columns: this.state.columns,
      records: this.props.list.records,
      activeYear: 2024,
      currentMonth: this.getCurrentMonth(),
      currentMonthId: new Date().getMonth(),
      currentYear: new Date().getFullYear(),
    });
    onMounted(() => {
      this.fetchItems();
      // this.action.doAction(this.sendCustomNotification());
    });
  }

  fetchItems() {
    const monthItems = [
      {
        quarter: "I",
        months: [
          {
            month: "January",
            id: "1",
          },
          {
            month: "February",
            id: "2",
          },
          {
            month: "March",
            id: "3",
          },
        ],
      },
      {
        quarter: "II",
        months: [
          {
            month: "April",
            id: "4",
          },
          {
            month: "May",
            id: "5",
          },
          {
            month: "June",
            id: "6",
          },
        ],
      },
      {
        quarter: "III",
        months: [
          {
            month: "July",
            id: "7",
          },
          {
            month: "August",
            id: "8",
          },
          {
            month: "September",
            id: "9",
          },
        ],
      },
      {
        quarter: "IV",
        months: [
          {
            month: "October",
            id: "10",
          },
          {
            month: "November",
            id: "11",
          },
          {
            month: "December",
            id: "12",
          },
        ],
      },
    ];
    this.state.monthItems = monthItems;
  }

  setActiveYear(year) {
    this.state.activeYear = year;
  }

  getCurrentMonth() {
    const month = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];

    const d = new Date();
    return month[d.getMonth()];
  }

  sendCustomNotification() {
    return {
      type: "ir.actions.client",
      tag: "display_notification",
      params: {
        type: "info",
        message: `Accounting Solishtirish: keyingi oning 1 sanasigacha. Bandlov tanlash: Jo’natish sanasi bo’yicha (kalendar oyi)`,
        sticky: "False",
      },
    };
  }

  monthHasRecord(id) {
    const hasRecord = this.state.records.find(
      (data) =>
        data.data.check_out_date.c.month == id &&
        data.data.check_out_date.c.year == this.state.activeYear
    );
    if (hasRecord) {
      return true;
    } else {
      return false;
    }
  }

  fillTotal(id) {
    let total = 0;
    this.state.records.map((data, index) => {
      if (
        data.data.check_out_date.c.month == id &&
        data.data.check_out_date.c.year == this.state.activeYear
      ) {
        total += data.data.total;
      }
    });
    return `${this.formatNumber(total)} UZS`;
  }
  fillCount(id) {
    let count = 0;
    this.state.records.map((data, index) => {
      if (
        data.data.check_out_date.c.month == id &&
        data.data.check_out_date.c.year == this.state.activeYear
      ) {
        count += 1;
      }
    });
    return count;
  }

  goMonthlyData(month) {
    sessionStorage.setItem("selectedMonth", month);
    this.action
      .doAction(
        {
          type: "ir.actions.act_window",
          res_model: "accounting.calendar",
          name: "Monthly Data",
          target: "current",
          views: [[false, "list"]],
        },
        {clearBreadcrumbs: false}
      )
      .catch((error) => {
        console.error(`Action does not exist or failed:`, error);
        alert(`The action does not exist.`);
      });
  }

  formatNumber(number) {
    return new Intl.NumberFormat().format(number);
  }
}

AccountingRenderer.template = "hms_app.AccountingSettings";
