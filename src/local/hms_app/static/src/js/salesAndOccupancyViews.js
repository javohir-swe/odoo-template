/** @odoo-module */
import {ListRenderer} from "@web/views/list/list_renderer";
import {useState, onWillStart, onMounted, onWillUnmount} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {ChartRenderer} from "./chart_renderer";
import {Widget} from "@web/views/widgets/widget";
import {CheckBox} from "@web/core/checkbox/checkbox";
import {Dropdown} from "@web/core/dropdown/dropdown";
import {DropdownItem} from "@web/core/dropdown/dropdown_item";
import {Field} from "@web/views/fields/field";
import {ViewButton} from "@web/views/view_button/view_button";
import {Pager} from "@web/core/pager/pager";
export class SalesAndOccupancyViews extends ListRenderer {
  setup() {
    super.setup();
    this.state = useState({
      activeTab: "loading",
      loading: false,
      filter: {
        scale: "month",
        reservationData: "nightNumberUZS",
      },
      chartData: [
        "Jan 2024",
        "Feb 2024",
        "March 2024",
        "Apr 2024",
        "May 2024",
        "June 2024",
        "July 2024",
        "Aug 2024",
        "Sep 2024",
        "Oct 2024",
        "Nov 2024",
        "Dec 2024",
      ],

      monthNames: [
        "Jan",
        "Feb",
        "March",
        "Apr",
        "May",
        "June",
        "July",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
      ],

      chartDataSets: [
        {
          label: "Searchable period",
          data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          borderColor: "#3780FF",
          tension: 0.1,
          yAxisID: "y",
        },
      ],
      pieChartLabels: ["Red", "Blue", "Yellow"],
      pieChartData: [300, 50, 100],
      pieChartBgColors: ["rgb(255, 99, 132)", "rgb(54, 162, 235)", "rgb(255, 205, 86)"],
      searchFrom: new Date("01.02.2024").toISOString().substr(0, 10),
      searchTo: new Date("12.01.2024").toISOString().substr(0, 10),
      columns: this.state.columns || [],
    });
    onWillStart(() => {
      this.findWhichPeriod();
    });
  }

  updateFilter() {
    const start = new Date(this.state.searchFrom);
    const end = new Date(this.state.searchTo);
    const period = this.state.filter.scale; // 'day', 'week', 'month'

    const labels = [];
    const data = [];

    switch (period) {
      case "day":
        while (start <= end) {
          labels.push(
            `${start.getDate()} ${
              this.state.monthNames[start.getMonth()]
            } ${start.getFullYear()}`
          );
          data.push(0); // Initialize the count with 0
          start.setDate(start.getDate() + 1);
        }
        break;

      case "week":
        while (start <= end) {
          const weekStart = new Date(start);
          const weekEnd = new Date(start);
          weekEnd.setDate(weekStart.getDate() + 6);
          labels.push(
            `${weekStart.getDate()} ${
              this.state.monthNames[weekStart.getMonth()]
            } ${weekStart.getFullYear()} - ${weekEnd.getDate()} ${
              this.state.monthNames[weekEnd.getMonth()]
            } ${weekEnd.getFullYear()}`
          );
          data.push(0); // Initialize the count with 0
          start.setDate(start.getDate() + 7);
        }
        break;

      case "month":
      default:
        while (start <= end) {
          const month = this.state.monthNames[start.getMonth()];
          const year = start.getFullYear();
          labels.push(`${month} ${year}`);
          data.push(0); // Initialize the count with 0
          start.setMonth(start.getMonth() + 1);
        }
        break;
    }

    this.state.chartData = labels;
    this.state.chartDataSets[0].data = data;

    this.findWhichPeriod();
  }

  findWhichPeriod() {
    const period = this.state.filter.scale;

    this.props.list.records.forEach((item) => {
      const {year, month, day} = item.data.check_in_date.c;
      const date = new Date(year, month - 1, day);

      let periodLabel;

      switch (period) {
        case "day":
          periodLabel = `${date.getDate()} ${
            this.state.monthNames[date.getMonth()]
          } ${date.getFullYear()}`;
          break;

        case "week":
          const weekStart = new Date(date);
          const weekEnd = new Date(weekStart);
          weekStart.setDate(date.getDate() - date.getDay());
          weekEnd.setDate(weekStart.getDate() + 6);
          periodLabel = `${weekStart.getDate()} ${
            this.state.monthNames[weekStart.getMonth()]
          } ${weekStart.getFullYear()} - ${weekEnd.getDate()} ${
            this.state.monthNames[weekEnd.getMonth()]
          } ${weekEnd.getFullYear()}`;
          break;

        case "month":
        default:
          periodLabel = `${
            this.state.monthNames[date.getMonth()]
          } ${date.getFullYear()}`;
          break;
      }

      const index = this.state.chartData.findIndex((label) => {
        if (period === "week") {
          const [startLabel, endLabel] = label.split(" - ");
          const [startDay, startMonth, startYear] = startLabel.split(" ");
          const [endDay, endMonth, endYear] = endLabel.split(" ");

          const weekStartDate = new Date(
            parseInt(startYear),
            this.state.monthNames.indexOf(startMonth),
            parseInt(startDay)
          );
          const weekEndDate = new Date(
            parseInt(endYear),
            this.state.monthNames.indexOf(endMonth),
            parseInt(endDay)
          );

          return date >= weekStartDate && date <= weekEndDate;
        } else {
          return label === periodLabel;
        }
      });

      if (index !== -1) {
        if (this.state.filter.reservationData === "nightNumberPCS") {
          this.state.chartDataSets[0].data[index] += 1;
        } else if (this.state.filter.reservationData === "nightNumberUZS") {
          this.state.chartDataSets[0].data[index] += item._values.total;
        }
      }
    });
  }

  setActiveTab(tab) {
    this.state.activeTab = tab;
  }

  toggleHeader() {
    const el = document.getElementById("salesAndOccupancy");

    if (el) {
      el.classList.toggle("show");
    }
  }
}

SalesAndOccupancyViews.template = "hms_app.SalesAndOccupancyViews";
SalesAndOccupancyViews.components = {
  DropdownItem,
  Field,
  ViewButton,
  CheckBox,
  Dropdown,
  Pager,
  Widget,
  ChartRenderer,
};
