/** @odoo-module **/

import {ListRenderer} from "@web/views/list/list_renderer";
import {useState, onMounted, onWillUnmount, onWillStart} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class DetailedRenderer extends ListRenderer {
  setup() {
    super.setup();
    this.state = useState({
      columns: this.state.columns,
      records: this.props.list.records,
      monthlyData: [],
      month: sessionStorage.getItem("selectedMonth") || "July",
      allMonths: [
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
      ],
      untilField: false,
      resetButton: false,
    });
    onMounted(() => {
      this.filterDataByMonth();
    });
    this.filterDataByCalendar = this.filterDataByCalendar.bind(this);
  }
  recordDate(date) {
    return `${String(date.day).padStart(2, "0")}/${String(date.month).padStart(
      2,
      "0"
    )}/${date.year}`;
  }
  filterDataByMonth() {
    this.state.monthlyData = [];
    this.state.records.map((record, index) => {
      if (
        record.data.check_in_date.c.month - 1 ==
        this.state.allMonths.indexOf(this.state.month)
      ) {
        this.state.monthlyData.push(record);
      }
    });
  }
  filterCount() {
    let count = 0;
    this.state.records.map((record, index) => {
      if (
        record.data.check_in_date.c.month - 1 ==
        this.state.allMonths.indexOf(this.state.month)
      ) {
        count += 1;
      }
    });
    return count;
  }
  filterTotal() {
    let total = 0;
    this.state.records.map((record, index) => {
      if (
        record.data.check_in_date.c.month - 1 ==
        this.state.allMonths.indexOf(this.state.month)
      ) {
        total += record.data.total;
      }
    });
    return `${this.formatNumber(total)} UZS`;
  }
  filterNewData(e) {
    e.preventDefault();
    this.state.month = e.target.value;
    document.getElementById("from-date").value = "";
    document.getElementById("to-date").value = "";
    this.state.untilField = false;
    this.state.resetButton = false;
    this.filterDataByMonth();
  }
  resetFields() {
    document.getElementById("from-date").value = "";
    document.getElementById("to-date").value = "";
    this.state.untilField = false;
    this.state.resetButton = false;
    this.filterDataByMonth();
  }
  formatNumber(number) {
    return new Intl.NumberFormat().format(number);
  }
  setMin() {
    let year = new Date().getFullYear();
    return `${year}-${String(
      this.state.allMonths.indexOf(this.state.month) + 1
    ).padStart(2, "0")}-01`;
  }
  setMax() {
    let year = new Date().getFullYear();
    let last = new Date(
      year,
      this.state.allMonths.indexOf(this.state.month) + 1,
      0
    ).getDate();
    return `${year}-${String(
      this.state.allMonths.indexOf(this.state.month) + 1
    ).padStart(2, "0")}-${String(last)}`;
  }

  startSelected(e) {
    e.preventDefault();
    document.getElementById("to-date").min = e.target.value;
    this.state.untilField = true;
  }
  filterDataByCalendar(e) {
    e.preventDefault();
    this.state.resetButton = true;
    const fromDateInput = document.getElementById("from-date").value;
    const toDateInput = document.getElementById("to-date").value;

    const fromDate = new Date(fromDateInput);
    const toDate = new Date(toDateInput);

    const filteredData = this.state.monthlyData.filter((item) => {
      const {year, month, day} = item.data.check_out_date.c;
      const checkOutDate = new Date(year, month - 1, day);
      return checkOutDate >= fromDate && checkOutDate <= toDate;
    });
    this.state.monthlyData = filteredData;
  }
}
DetailedRenderer.template = "hms_app.DetailedView";
