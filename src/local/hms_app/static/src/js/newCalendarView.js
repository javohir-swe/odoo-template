/** @odoo-module */

import {CalendarRenderer} from "@web/views/calendar/calendar_renderer";
import {onMounted, useState, onWillStart, onWillUnmount} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class CustomCalendarRenderer extends CalendarRenderer {
  setup() {
    super.setup();
    this.orm = useService("orm");
    this.rpc = useService("rpc");
    this.state = useState({
      monthRestriction: 0,
      selectedDate: this.formatDate(new Date()),
      records: this.props.model.data.records,
      defaultData: this.getDefaultData() || [],
      activeTab: "calendar",
      uniqueRoomNames: this.getUniqueRoomNames(this.props.model.data.records),
      activeRoom: this.getUniqueRoomNames(this.props.model.data.records)[0] || null,
      currentMonth: new Date(),
      monthName: this.getMonthNames(new Date(), 0, 0),
      loading: false,
      isModal: false,
      willChangedDate: "",
      willChangedData: [],
      weekdays: [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
      ],
      calendar: this.generateCalendar(new Date()),
    });

    onMounted(() => {
      document.querySelector(".o_calendar_header").classList.add("d-none");
      document.querySelector(".o_control_panel").classList.add("d-none");
      document.querySelector(".o_calendar_header").innerHTML = "";
      document.querySelector(".o_calendar_sidebar_container").classList.add("d-none");
      document.querySelector(".o_calendar_sidebar_container").innerHTML = "";
      // this.state.defaultData = Array.from(this.state.defaultData);
      this.setDefaultDates();
      this.addDateChangeListeners();
    });
    onWillStart(async () => {
      try {
        this.state.loading = true;
        let defaultData = await this.getDefaultData();
        this.state.defaultData = defaultData;
      } catch (error) {
        console.error("Error fetching default data:", error);
      } finally {
        this.state.loading = false;
      }
    });
    onWillUnmount(() => {
      document.querySelector(".o_control_panel").classList.remove("d-none");
    });
  }

  async getDefaultData() {
    try {
      const res = await this.rpc("/web/dataset/call_kw", {
        model: "default.availability",
        method: "get_all_default_data_fields",
        args: [1],
        kwargs: {},
      });
      return Array.from(res.default_data);
    } catch (error) {
      console.error("Error fetching default data:", error);
    }
  }

  generateCalendar(date) {
    const firstDayOfMonth =
      (new Date(date.getFullYear(), date.getMonth(), 1).getDay() + 6) % 7; // Adjust for Monday start
    const daysInMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
    const daysInPrevMonth = new Date(date.getFullYear(), date.getMonth(), 0).getDate();

    const calendar = [];
    let week = [];
    let day = 1;
    let prevMonthDay = daysInPrevMonth - firstDayOfMonth + 1;
    let nextMonthDay = 1;
    let hasCurrentMonthDay = false;

    for (let i = 0; i < 6; i++) {
      week = new Array(7).fill(null);
      hasCurrentMonthDay = false;
      for (let j = 0; j < 7; j++) {
        if (i === 0 && j < firstDayOfMonth) {
          week[j] = {day: prevMonthDay++, type: "prev"};
        } else if (day > daysInMonth) {
          week[j] = {day: nextMonthDay++, type: "next"};
        } else {
          week[j] = {day: day++, type: "current"};
          hasCurrentMonthDay = true;
        }
      }

      if (hasCurrentMonthDay || i < 5) {
        calendar.push(week);
      }
    }

    return calendar;
  }

  validateInput(event) {
    let value = event.target.value;

    // If the value is empty or less than 0, set it to 0
    if (value === "" || isNaN(value) || value < 0) {
      value = 0;
    } else {
      // Convert the value to a number and remove leading zeros
      value = parseInt(value, 10);
    }

    // Update the input value
    event.target.value = value;
  }

  getUniqueRoomNames(recordRoom) {
    const uniqueNames = [];
    Object.keys(recordRoom).forEach((index) => {
      const roomName = recordRoom[index].rawRecord.room_type[1];
      if (!uniqueNames.includes(roomName)) {
        uniqueNames.push(roomName);
      }
    });
    return uniqueNames;
  }

  setDefaultDates() {
    const today = new Date();

    const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 2);
    const lastDayOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 1);

    const formatDate = (date) => date.toISOString().split("T")[0];

    const startDateInput = document.getElementById("start_date");
    const endDateInput = document.getElementById("end_date");

    if (startDateInput && endDateInput) {
      startDateInput.value = formatDate(firstDayOfMonth);
      endDateInput.value = formatDate(lastDayOfMonth);
    }
  }

  addDateChangeListeners() {
    const startDateInput = document.getElementById("start_date");
    const endDateInput = document.getElementById("end_date");

    if (startDateInput && endDateInput) {
      startDateInput.addEventListener("change", () => this.logDates());
      endDateInput.addEventListener("change", () => this.logDates());
    }
  }

  logDates() {
    const startDate = document.getElementById("start_date")?.value || "";
    const endDate = document.getElementById("end_date")?.value || "";
  }

  formatDate(timestamp) {
    const day = String(timestamp.getDate()).padStart(2, "0");
    const month = String(timestamp.getMonth() + 1).padStart(2, "0");
    const year = timestamp.getFullYear();
    const selectedDate = `${year}-${month}-${day}`;
    return selectedDate;
  }

  handleDateClick(day, monthYear) {
    const [monthName, year] = monthYear.split(" ");
    const monthNames = [
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
    const month = monthNames.indexOf(monthName) + 1;
    const dayFormatted = String(day).padStart(2, "0");
    const monthFormatted = String(month).padStart(2, "0");
    const userSelectDate = `${year}-${monthFormatted}-${dayFormatted}`;
    return userSelectDate;
  }

  setActiveTab(tabName) {
    this.state.activeTab = tabName;
  }

  setActiveRoom(roomName) {
    this.state.activeRoom = roomName;
  }

  getMonthNames(month, inc, dec) {
    let number = month.getMonth() + inc - dec;
    if (number < 0) {
      number += 12;
      month.setFullYear(month.getFullYear() - 1);
    }
    if (number > 11) {
      number -= 12;
      month.setFullYear(month.getFullYear() + 1);
    }
    const months = [
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
    const selectedMonth = months[number];
    return `${selectedMonth} ${month.getFullYear()}`;
  }

  prevMonth() {
    this.state.monthRestriction -= 1;
    const newMonth = new Date(this.state.currentMonth);
    newMonth.setMonth(newMonth.getMonth() - 1);
    this.state.currentMonth = newMonth;
    this.state.monthName = this.getMonthNames(newMonth, 0, 0);
    this.state.calendar = this.generateCalendar(newMonth);
  }

  nextMonth() {
    this.state.monthRestriction += 1;
    const newMonth = new Date(this.state.currentMonth);
    newMonth.setMonth(newMonth.getMonth() + 1);
    this.state.currentMonth = newMonth;
    this.state.monthName = this.getMonthNames(newMonth, 0, 0);
    this.state.calendar = this.generateCalendar(newMonth);
  }

  async saveDataDefault() {
    const specification = {
      default_data: {
        fields: {
          room_type: {
            fields: {
              display_name: {},
            },
          },
          number: {},
        },
        limit: 40,
        order: "",
      },
      display_name: [],
    };
    let default_data = [];
    this.state.defaultData.map((data, index) => {
      default_data.push([4, data[0].id]);
    });
    this.state.defaultData.map((data, index) => {
      data[0].number = +document.getElementById(data[0].room_type[1]).value;
      default_data.push([
        1,
        data[0].id,
        {number: +document.getElementById(data[0].room_type[1]).value},
      ]);
    });
    try {
      this.state.loading = true;

      const result = await this.orm.call(
        "default.availability",
        "web_save",
        [[], {default_data}],
        {specification}
      );
      // this.state.activeTab = "calendar";
    } catch (err) {
      console.error("Error while saving data: ", err);
    } finally {
      window.location.reload();
      this.state.loading = false;
    }
  }

  updateStatus = (info) => {
    info.close_open = !info.close_open;

    const obj = {
      close_open: info.close_open,
      room_type: info.room_type[0],
      bookings: info.bookings,
      cancellations: info.cancellations,
      date: info.date,
      default: info.default,
      display_name: info.display_name,
      front_desk: info.front_desk,
      id: info.id,
      online: info.online,
    };

    this.state.loading = true;

    this.orm.call("main.availability", "create", [obj]).then((result) => {
      // window.location.reload();
      this.state.loading = false;
    });
  };

  closeModal() {
    this.state.isModal = false;
  }

  onCellClick(dayObj) {
    if (dayObj.type === "current") {
      const clickedDate = this.handleDateClick(dayObj.day, this.state.monthName);
      const dayRecords = Object.keys(this.state.records).filter(
        (record) => this.state.records[record].rawRecord.date === clickedDate
      );

      // Clear existing table body content
      const tbody = document.getElementById("av-tbody");
      tbody.innerHTML = "";
      this.state.willChangedData = [];
      // this.state.willChangedData = dayRecords;
      dayRecords.forEach((record) => {
        this.state.willChangedData.push(this.state.records[record].rawRecord);
        const tr = document.createElement("tr");

        const roomTypeTd = document.createElement("td");
        roomTypeTd.textContent = this.state.records[record].rawRecord.room_type[1];
        tr.appendChild(roomTypeTd);

        const defaultTd = document.createElement("td");
        const defaultInput = document.createElement("input");
        defaultInput.type = "number"; // Use 'number' or 'text' depending on your data type
        defaultInput.min = 0;
        defaultInput.value = this.state.records[record].rawRecord.default;
        defaultInput.className = "av-modal-default";
        defaultInput.id = `default-${this.state.records[record].rawRecord.room_type[1]}`;
        defaultTd.appendChild(defaultInput);
        tr.appendChild(defaultTd);

        defaultInput.addEventListener("input", (event) => this.validateInput(event));
        defaultInput.addEventListener("blur", (event) => this.validateInput(event));

        const frontDeskTd = document.createElement("td");
        frontDeskTd.textContent = this.state.records[record].rawRecord.front_desk;
        tr.appendChild(frontDeskTd);

        const onlineTd = document.createElement("td");
        onlineTd.textContent = this.state.records[record].rawRecord.online;
        tr.appendChild(onlineTd);

        const bookingsTd = document.createElement("td");
        bookingsTd.textContent = this.state.records[record].rawRecord.bookings;
        tr.appendChild(bookingsTd);

        const cancellationsTd = document.createElement("td");
        cancellationsTd.textContent =
          this.state.records[record].rawRecord.cancellations;
        tr.appendChild(cancellationsTd);

        tbody.appendChild(tr);
        const formattedDate = this.formatDateToLong(
          this.state.records[record].rawRecord.date
        );
        document.getElementById("avModalDataDate").textContent = formattedDate;
      });

      this.state.isModal = true;
    }
  }
  formatDateToLong(date) {
    this.state.willChangedDate = date;
    let format = new Date(date);
    const options = {day: "numeric", month: "long", year: "numeric"};
    return new Intl.DateTimeFormat("en-US", options).format(format);
  }

  async saveData() {
    const specification = {
      close_open: {},
      front_desk: {},
      default: {},
      online: {},
      room_type: {
        fields: {
          display_name: {},
        },
      },
      date: {},
      display_name: {},
    };
    Object.keys(this.state.willChangedData).forEach(async (data) => {
      let updatedData = {
        default: +document.getElementById(
          `default-${this.state.willChangedData[data].room_type[1]}`
        ).value,
      };
      try {
        const res = await this.orm.call(
          "main.availability",
          "web_save",
          [[this.state.willChangedData[data].id], updatedData],
          {specification}
        );
        return res;
      } catch (error) {
        console.error("Error fetching rule data:", error);
      }
    });
    // window.location.reload();
  }
}

CustomCalendarRenderer.template = "hms_app.CalendarRenderer";
