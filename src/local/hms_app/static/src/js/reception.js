/** @odoo-module */

import {ListRenderer} from "@web/views/list/list_renderer";
import {useState, onMounted, onWillStart, onWillUnmount} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class ReceptionRenderer extends ListRenderer {
  setup() {
    super.setup();
    this.actionService = useService("action");
    this.rpc = useService("rpc");
    this.orm = useService("orm");
    this.state = useState({
      records: this.props.list.records,
      columns: this.state.columns || [],
      defaultData: this.getDefaultData() || false,
      receptionData: this.getReceptionData() || [],
      filteredData: [],
      occupied: 0,
      total: 0,
      unclear: 0,
      clear: 0,
      checked: 0,
      period: 0,
      modify: 0,
      arrivals: 0,
      sameDayBookings: 0,
      departures: 0,
      occupiedRooms: 0,
      noShows: 0,
      isCheckInActive: false,
      isCheckOutActive: false,
      activeTab: "Arrivals",
      loading: false,
      todayDate: this.formatDate(new Date()),
      willSavedData: [],
      isViewModal: false,
      isChecked: JSON.parse(sessionStorage.getItem("isChecked")) || {
        bookingNumber: true,
        customer: true,
        guestFullName: true,
        roomNumber: true,
        checkInTime: true,
        checkOutTime: true,
        period: true,
        roomType: true,
        day: true,
        balance: true,
        tags: true,
        notes: true,
        nights: true,
        guestComment: true,
        status: true,
        action: true,
      },
      search: "",
      newFilteredData: [],
      xls_modal: false,
      selected_option: "All",
      selected_departure: "All",
    });
    this.checkInActive = this.checkInActive.bind(this);
    this.viewModal = this.viewModal.bind(this);
    this.searchFilter = this.searchFilter.bind(this);
    onMounted(() => {
      this.occupiedCount();
      this.sumOfOccupiedRooms();
      this.arrivalSameDayBookings();
      this.filterReceptionData();
      document.querySelector('input[type="date"]').addEventListener("change", () => {
        this.filterReceptionData();
        this.render();
      });
    });

    onWillStart(async () => {
      try {
        this.state.loading = true;

        let receptionData = await this.getReceptionData();
        let defaultData = await this.getDefaultData();
        this.state.defaultData = defaultData;
        this.state.receptionData = receptionData;
        this.renderData(defaultData);
      } catch (error) {
        console.error("Error fetching default data:", error);
      } finally {
        this.state.loading = false;
      }
    });
  }

  openXLS() {
    this.state.xls_modal = !this.state.xls_modal;
  }

  formatDate(date) {
    return date.toISOString().split("T")[0];
  }

  formatTime(date) {
    return date.toTimeString().slice(0, 5);
  }

  setDateTimeInputs() {
    const dateInput = document.getElementById("checkDate");
    const timeInput = document.getElementById("checkTime");

    const currentDate = new Date();

    dateInput.value = this.formatDate(currentDate);
    timeInput.value = this.formatTime(currentDate);
  }

  async getDefaultData() {
    try {
      const res = await this.rpc("/web/dataset/call_kw", {
        model: "room_inventory.housekeeping",
        method: "get_rooms_by_type",
        args: [],
        kwargs: {},
      });
      return res;
    } catch (error) {
      console.error("Error fetching rooms data by type:", error);
    }
  }

  async getReceptionData() {
    try {
      const res = await this.rpc("/web/dataset/call_kw", {
        model: "reception",
        method: "get_reception_data",
        args: [],
        kwargs: {},
      });
      return res;
    } catch (error) {
      console.error("Error fetching reception data:", error);
    }
  }

  renderData(roomsData) {
    roomsData.map((data, index) => {
      this.state.total += data.count;
      data.rooms.map((room, i) => {
        if (room.status === "Clean") {
          this.state.clear += 1;
        }
        if (room.status === "Need to Clean") {
          this.state.unclear += 1;
        }
        if (room.status === "Checked") {
          this.state.checked += 1;
        }
        if (room.status === "Out of Order") {
          this.state.modify += 1;
        }
      });
    });
  }

  statusChecking(status) {
    let statusCheck = "";
    if (status == "arrival") {
      statusCheck = "Arrival";
    } else if (status == "same_day_bookings") {
      statusCheck = "Same-day bookings";
    } else if (status == "checked_out") {
      statusCheck = "Checked Out";
    } else if (status == "waiting") {
      statusCheck = "Waiting";
    } else {
      statusCheck = status;
    }
    return statusCheck;
  }

  filterReceptionData() {
    const dateInput = document.querySelector('input[type="date"]').value;
    const today = new Date();
    const inputDate = new Date(dateInput);
    let filteredData = [];
    let totalNights = 0;

    if (this.state.activeTab === "Arrivals") {
      this.state.receptionData.forEach((entry) => {
        entry.data.forEach((data) => {
          if (data.check_in_date === dateInput) {
            if (!filteredData.some((item) => item.reception_id === data.reception_id)) {
              filteredData.push(data);
            }
          }
        });
      });
    } else if (this.state.activeTab === "Departures") {
      this.state.receptionData.forEach((entry) => {
        entry.data.forEach((data) => {
          if (data.check_out_date === dateInput) {
            if (!filteredData.some((item) => item.reception_id === data.reception_id)) {
              filteredData.push(data);
            }
          }
        });
      });
    } else if (this.state.activeTab === "Occupied") {
      this.state.receptionData.forEach((entry) => {
        entry.data.forEach((data) => {
          const checkInDate = new Date(data.check_in_date);
          const checkOutDate = new Date(data.check_out_date);
          if (inputDate >= checkInDate && inputDate <= checkOutDate) {
            const nightsOccupied = Math.floor(
              (today - checkInDate) / (1000 * 60 * 60 * 24)
            );
            data.daysOccupied = nightsOccupied;
            totalNights += nightsOccupied; // Accumulate total nights
            if (!filteredData.some((item) => item.reception_id === data.reception_id)) {
              filteredData.push(data);
            }
          }
        });
      });
    }
    this.state.filteredData = filteredData;
    this.state.period = totalNights;
    const {selected_option, selected_departure} = this.state;

    const newData = this.state.filteredData.filter((record) => {
      return (
        (selected_option === "All" ||
          this.statusChecking(record.arrival_status) === selected_option) &&
        (selected_departure === "All" ||
          this.statusChecking(record.departure_status) === selected_departure)
      );
    });
    this.state.filteredData = newData;

    this.render();
  }

  sumOfOccupiedRooms() {
    const dateInput = document.querySelector('input[type="date"]').value;
    const today = new Date();
    const inputDate = new Date(dateInput);
    let filteredData = [];
    let totalNights = 0;
    this.state.receptionData.forEach((entry) => {
      entry.data.forEach((data) => {
        const checkInDate = new Date(data.check_in_date);
        const checkOutDate = new Date(data.check_out_date);
        if (inputDate >= checkInDate && inputDate <= checkOutDate) {
          const nightsOccupied = Math.floor(
            (today - checkInDate) / (1000 * 60 * 60 * 24)
          );
          data.daysOccupied = nightsOccupied;
          totalNights += nightsOccupied;
          if (!filteredData.some((item) => item.reception_id === data.reception_id)) {
            filteredData.push(data);
          }
        }
      });
      this.state.occupiedRooms = filteredData.length;
    });
  }

  searchFilter(event) {
    const searchText = event.toLowerCase();
    this.state.search = searchText;
    if (!searchText) {
      this.state.newFilteredData = this.state.filteredData;
    } else {
      this.state.newFilteredData = this.state.filteredData.filter((record) =>
        Object.values(record).some((value) =>
          record.customer.toLowerCase().includes(searchText)
        )
      );
    }
    this.render();
  }
  arrivalSameDayBookings() {
    this.state.arrivals = 0;
    this.state.sameDayBookings = 0;
    // this.state.departures = 0;

    this.state.receptionData[0].data.forEach((record) => {
      if (record.check_in_date == this.state.todayDate) {
        if (record.arrival_status == "arrival") {
          this.state.arrivals += 1;
        } else {
          this.state.sameDayBookings += 1;
        }
      }
    });

    this.state.receptionData[1].data.forEach((record) => {
      if (record.check_out_date == this.state.todayDate) {
        if (record.departure_status == "checked_out") {
          this.state.departures += 1;
        }
      }
    });
  }

  getNightsOccupied(record) {
    const checkInDate = new Date(record.check_in_date);
    const checkOutDate = new Date(record.check_out_date);
    const today = new Date();

    const totalNights = Math.floor(
      (checkOutDate - checkInDate) / (1000 * 60 * 60 * 24)
    );
    const nightsOccupied = Math.floor((today - checkInDate) / (1000 * 60 * 60 * 24));
    const currentNights = Math.max(nightsOccupied, 0);

    return `${currentNights} of ${totalNights}`;
  }

  recordDate(date) {
    return `${date.year}-${String(date.month).padStart(2, "0")}-${String(
      date.day
    ).padStart(2, "0")}`;
  }

  recordCalendarDate(day) {
    return `${this.state.selectedMonth}-${String(day).padStart(2, "0")}`;
  }

  occupiedCount() {
    let today = new Date();
    let formattedDate = today.getDate();
    this.state.records.map((record, index) => {
      if (
        (this.recordDate(record.data.check_in_date.c) ===
          this.recordCalendarDate(formattedDate) ||
          (this.recordCalendarDate(formattedDate) >=
            this.recordDate(record.data.check_in_date.c) &&
            this.recordDate(record.data.check_out_date.c) >
              this.recordCalendarDate(formattedDate))) &&
        record.data.room_number
      ) {
        this.state.occupied += 1;
      }
    });
  }

  setActiveTab(tab) {
    this.state.activeTab = tab;
    this.filterReceptionData();
    this.render();
  }

  goBooking() {
    this.actionService
      .doAction(
        {
          type: "ir.actions.act_window",
          res_model: "booking",
          name: "Booking",
          target: "current",
          views: [[false, "form"]],
        },
        {clearBreadcrumbs: false}
      )
      .catch((error) => {
        console.error(`Action does not exist or failed:`, error);
        alert(`The action does not exist.`);
      });
  }

  goGroupBooking() {
    this.actionService
      .doAction(
        {
          type: "ir.actions.act_window",
          res_model: "group_booking",
          name: "Group Booking",
          target: "current",
          views: [[false, "form"]],
        },
        {clearBreadcrumbs: false}
      )
      .catch((error) => {
        console.error(`Action does not exist or failed:`, error);
        alert(`The action does not exist.`);
      });
  }

  checkInModal(data) {
    this.actionService
      .doAction(
        {
          type: "ir.actions.act_window",
          res_model: "reception.checkin",
          name: "Reception",
          target: "new",
          views: [[false, "form"]],
        },
        {clearBreadcrumbs: false}
      )
      .catch((error) => {
        console.error(`Action does not exist or failed:`, error);
        alert(`The action does not exist.`);
      });
  }

  receptionModal(data) {
    this.actionService
      .doAction(
        {
          type: "ir.actions.act_window",
          context: {
            create: false,
          },
          res_model: "reception",
          res_id: data.reception_id,
          name: "Reception",
          target: "current",
          views: [[false, "form"]],
          flags: {mode: "edit"},
        },
        {clearBreadcrumbs: false}
      )
      .catch((error) => {
        console.error(`Action does not exist or failed:`, error);
        alert(`The action does not exist.`);
      });
  }

  changeArrivalStatusName(name) {
    switch (name) {
      case "arrival":
        return "Arrival";
      case "waiting":
        return "Waiting";
      case "same_day_bookings":
        return "Same-day bookings";
      case "checked_out":
        return "Checked Out";

        break;
    }
  }

  checkInActive(record) {
    (document.getElementById("bookingNumber").innerText = record.booking_number),
      (document.getElementById("roomType").innerText = record.room_type),
      (document.getElementById("roomNumber").innerText = record.room_number),
      this.setDateTimeInputs();
    this.state.isCheckInActive = true;
    this.state.willSavedData = record;
  }

  viewModal() {
    this.state.isViewModal = true;
  }

  toggleCheck(field) {
    this.state.isChecked[field] = !this.state.isChecked[field];
    sessionStorage.setItem("isChecked", JSON.stringify(this.state.isChecked));
  }

  async saveData() {
    const updatedData = [
      {
        reception_id: this.state.willSavedData.reception_id,
        check_in_date: document.getElementById("checkDate").value,
        check_in_time: false,
      },
    ];
    const updatedDataOut = [
      {
        reception_id: this.state.willSavedData.reception_id,
        check_out_date: document.getElementById("checkDate").value,
        check_out_time: false,
      },
    ];

    if (this.state.activeTab == "Arrivals") {
      let specification = {
        check_in_date: {},
        check_in_time: {
          fields: {
            display_name: {},
          },
        },
        display_name: {},
        reception_id: {
          fields: {
            display_name: {},
          },
        },
        room_number: {
          fields: {
            display_name: {},
          },
        },
        room_type_id: {
          fields: {
            display_name: {},
          },
        },
        unique_id: {},
      };
      try {
        const res = await this.rpc("/web/dataset/call_kw", {
          model: "reception.checkin",
          method: "web_save",
          args: [[], updatedData],
          kwargs: {specification},
        });
        specification = {};
        return res;
      } catch (error) {
        console.error("Error fetching rule data:", error);
      } finally {
        this.state.isCheckInActive = false;
        window.location.reload();
      }
    } else {
      let specification = {
        check_out_date: {},
        check_out_time: {
          fields: {
            display_name: {},
          },
        },
        display_name: {},
        reception_id: {
          fields: {
            display_name: {},
          },
        },
        room_number: {
          fields: {
            display_name: {},
          },
        },
        room_type_id: {
          fields: {
            display_name: {},
          },
        },
        unique_id: {},
      };
      try {
        const res = await this.rpc("/web/dataset/call_kw", {
          model: "reception.checkout",
          method: "web_save",
          args: [[], updatedDataOut],
          kwargs: {specification},
        });
        return res;
      } catch (error) {
        console.error("Error fetching rule data:", error);
      } finally {
        this.state.isCheckInActive = false;
        window.location.reload();
      }
    }
  }
}

ReceptionRenderer.template = "hms_app.Reception";
