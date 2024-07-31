/** @odoo-module */

import {ListRenderer} from "@web/views/list/list_renderer";
import {useState, onWillStart, onMounted, onWillUnmount} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class FrontDeskRenderer extends ListRenderer {
  setup() {
    super.setup();
    this.actionService = useService("action");
    const now = new Date();
    const formattedMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(
      2,
      "0"
    )}`;
    this.rpc = useService("rpc");
    this.orm = useService("orm");
    this.state = useState({
      columns: this.state.columns || [],
      records: false,
      selectedMonth: formattedMonth,
      defaultData: this.getDefaultData() || false,
      ratePlanData: this.ratePlan() || false,
      checkInTime: this.checkTimes() || false,
      accommodation: [],
      guests: [],
      guestId: false,
      bookingId: 0,
      roomTypeId: false,
      roomId: false,
      accommodationId: false,
      calendar: this.generateCalendar(now.getFullYear(), now.getMonth()),
      roomVisibility: [],
      bookingMenu: false,
      occupied: 0,
      total: 0,
      unclear: 0,
      clear: 0,
      checked: 0,
      modify: 0,
      departure: 0,
      arrival: 0,
      same_day_booking: 0,
      selectedCells: new Set(),
      startCell: null,
      isSelecting: false,
      isDragging: false,
      loading: false,
      suggestions: [],
      lastName: "",
      isModal: false,
      displayedDataId: "",
      checkOutPayment: true,
      canCheckIn: false,
      canCheckInCancel: false,
      canCheckOutCancel: false,
      canMoveRoom: false,
      canPay: false,
      canNote: false,
      isCheckInActive: false,
      isNoteActive: false,
      isCheckInCancelActive: false,
      isCheckOutActive: false,
      isCheckOutCancelActive: false,
      isReasonEmpty: false,
      isReasonOutEmpty: false,
      noteTimeReadonly: true,
      noteData: [],
      charCounter: "1000 characters left",
      accUniqueId: false,
      willSavedData: [],
      country: [
        ["", ""],
        ["uzbekistan", "Uzbekistan"],
        ["afghanistan", "Afghanistan"],
        ["albania", "Albania"],
        ["algeria", "Algeria"],
        ["american_samoa", "American Samoa"],
        ["andorra", "Andorra"],
        ["angola", "Angola"],
        ["anguilla", "Anguilla"],
        ["antigua_and_barbuda", "Antigua and Barbuda"],
        ["argentina", "Argentina"],
        ["armenia", "Armenia"],
        ["aruba", "Aruba"],
        ["australia", "Australia"],
        ["austria", "Austria"],
        ["azerbaijan", "Azerbaijan"],
        ["bahamas", "Bahamas"],
        ["bahrain", "Bahrain"],
        ["bangladesh", "Bangladesh"],
        ["barbados", "Barbados"],
        ["belarus", "Belarus"],
        ["belgium", "Belgium"],
        ["belize", "Belize"],
        ["benin", "Benin"],
        ["bermuda", "Bermuda"],
        ["bhutan", "Bhutan"],
        ["bolivia", "Bolivia"],
        ["bosnia_and_herzegovina", "Bosnia and Herzegovina"],
        ["botswana", "Botswana"],
        ["brazil", "Brazil"],
        ["brunei", "Brunei"],
        ["bulgaria", "Bulgaria"],
        ["burkina_faso", "Burkina Faso"],
        ["burundi", "Burundi"],
        ["cambodia", "Cambodia"],
        ["cameroon", "Cameroon"],
        ["canada", "Canada"],
        ["cape_verde", "Cape Verde"],
        ["cayman_islands", "Cayman Islands"],
        ["central_african_republic", "Central African Republic"],
        ["chad", "Chad"],
        ["chile", "Chile"],
        ["china", "China"],
        ["colombia", "Colombia"],
        ["comoros", "Comoros"],
        ["congo", "Congo"],
        ["cook_islands", "Cook Islands"],
        ["costa_rica", "Costa Rica"],
        ["croatia", "Croatia"],
        ["cuba", "Cuba"],
        ["cyprus", "Cyprus"],
        ["czech_republic", "Czech Republic"],
        ["denmark", "Denmark"],
        ["djibouti", "Djibouti"],
        ["dominica", "Dominica"],
        ["dominican_republic", "Dominican Republic"],
        ["east_timor", "East Timor"],
        ["ecuador", "Ecuador"],
        ["egypt", "Egypt"],
        ["el_salvador", "El Salvador"],
        ["equatorial_guinea", "Equatorial Guinea"],
        ["eritrea", "Eritrea"],
        ["estonia", "Estonia"],
        ["eswatini", "Eswatini"],
        ["ethiopia", "Ethiopia"],
        ["fiji", "Fiji"],
        ["finland", "Finland"],
        ["france", "France"],
        ["gabon", "Gabon"],
        ["gambia", "Gambia"],
        ["georgia", "Georgia"],
        ["germany", "Germany"],
        ["ghana", "Ghana"],
        ["greece", "Greece"],
        ["greenland", "Greenland"],
        ["grenada", "Grenada"],
        ["guatemala", "Guatemala"],
        ["guinea", "Guinea"],
        ["guinea_bissau", "Guinea-Bissau"],
        ["guyana", "Guyana"],
        ["haiti", "Haiti"],
        ["honduras", "Honduras"],
        ["hungary", "Hungary"],
        ["iceland", "Iceland"],
        ["india", "India"],
        ["indonesia", "Indonesia"],
        ["iran", "Iran"],
        ["iraq", "Iraq"],
        ["ireland", "Ireland"],
        ["israel", "Israel"],
        ["italy", "Italy"],
        ["jamaica", "Jamaica"],
        ["japan", "Japan"],
        ["jordan", "Jordan"],
        ["kazakhstan", "Kazakhstan"],
        ["kenya", "Kenya"],
        ["kiribati", "Kiribati"],
        ["north_korea", "North Korea"],
        ["south_korea", "South Korea"],
        ["kosovo", "Kosovo"],
        ["kuwait", "Kuwait"],
        ["kyrgyzstan", "Kyrgyzstan"],
        ["laos", "Laos"],
        ["latvia", "Latvia"],
        ["lebanon", "Lebanon"],
        ["lesotho", "Lesotho"],
        ["liberia", "Liberia"],
        ["libya", "Libya"],
        ["liechtenstein", "Liechtenstein"],
        ["lithuania", "Lithuania"],
        ["luxembourg", "Luxembourg"],
        ["madagascar", "Madagascar"],
        ["malawi", "Malawi"],
        ["malaysia", "Malaysia"],
        ["maldives", "Maldives"],
        ["mali", "Mali"],
        ["malta", "Malta"],
        ["marshall_islands", "Marshall Islands"],
        ["mauritania", "Mauritania"],
        ["mauritius", "Mauritius"],
        ["mexico", "Mexico"],
        ["micronesia", "Micronesia"],
        ["moldova", "Moldova"],
        ["monaco", "Monaco"],
        ["mongolia", "Mongolia"],
        ["montenegro", "Montenegro"],
        ["morocco", "Morocco"],
        ["mozambique", "Mozambique"],
        ["myanmar", "Myanmar"],
        ["namibia", "Namibia"],
        ["nauru", "Nauru"],
        ["nepal", "Nepal"],
        ["netherlands", "Netherlands"],
        ["new_zealand", "New Zealand"],
        ["nicaragua", "Nicaragua"],
        ["niger", "Niger"],
        ["nigeria", "Nigeria"],
        ["north_macedonia", "North Macedonia"],
        ["norway", "Norway"],
        ["oman", "Oman"],
        ["pakistan", "Pakistan"],
        ["palau", "Palau"],
        ["panama", "Panama"],
        ["papua_new_guinea", "Papua New Guinea"],
        ["paraguay", "Paraguay"],
        ["peru", "Peru"],
        ["philippines", "Philippines"],
        ["poland", "Poland"],
        ["portugal", "Portugal"],
        ["qatar", "Qatar"],
        ["romania", "Romania"],
        ["russian_federation", "Russian Federation"],
        ["rwanda", "Rwanda"],
        ["saint_kitts_and_nevis", "Saint Kitts and Nevis"],
        ["saint_lucia", "Saint Lucia"],
        ["saint_vincent_and_the_grenadines", "Saint Vincent and the Grenadines"],
        ["samoa", "Samoa"],
        ["san_marino", "San Marino"],
        ["sao_tome_and_principe", "Sao Tome and Principe"],
        ["saudi_arabia", "Saudi Arabia"],
        ["senegal", "Senegal"],
        ["serbia", "Serbia"],
        ["seychelles", "Seychelles"],
        ["sierra_leone", "Sierra Leone"],
        ["singapore", "Singapore"],
        ["slovakia", "Slovakia"],
        ["slovenia", "Slovenia"],
        ["solomon_islands", "Solomon Islands"],
        ["somalia", "Somalia"],
        ["south_africa", "South Africa"],
        ["south_sudan", "South Sudan"],
        ["spain", "Spain"],
        ["sri_lanka", "Sri Lanka"],
        ["sudan", "Sudan"],
        ["suriname", "Suriname"],
        ["sweden", "Sweden"],
        ["switzerland", "Switzerland"],
        ["syria", "Syria"],
        ["taiwan", "Taiwan"],
        ["tajikistan", "Tajikistan"],
        ["tanzania", "Tanzania"],
        ["thailand", "Thailand"],
        ["togo", "Togo"],
        ["tonga", "Tonga"],
        ["trinidad_and_tobago", "Trinidad and Tobago"],
        ["tunisia", "Tunisia"],
        ["turkey", "Turkey"],
        ["turkmenistan", "Turkmenistan"],
        ["tuvalu", "Tuvalu"],
        ["uganda", "Uganda"],
        ["ukraine", "Ukraine"],
        ["united_arab_emirates", "United Arab Emirates"],
        ["united_kingdom", "United Kingdom"],
        ["united_states", "United States"],
        ["uruguay", "Uruguay"],
        ["vanuatu", "Vanuatu"],
        ["vatican_city", "Vatican City"],
        ["venezuela", "Venezuela"],
        ["vietnam", "Vietnam"],
        ["yemen", "Yemen"],
        ["zambia", "Zambia"],
        ["zimbabwe", "Zimbabwe"],
      ],
      pointOfSale: [
        ["front_desk", "Front Desk"],
        ["booking_engine", "Booking Engine"],
        ["via_phone", "via phone"],
        ["via_distribution_channel", "via distribution channel"],
        ["website", "Website"],
        ["fax", "Fax"],
        ["email", "Email"],
        ["mobile_version_of_site", "Mobile version of site"],
        ["facebook", "Facebook"],
        ["tripadvisor", "TripAdvisor"],
        ["extranet_booking", "Extranet booking"],
      ],
      marketSegment: [
        ["individual", "Individual"],
        ["corporate_individual", "Corporate individual"],
        ["corporate_group", "Corporate group"],
        ["travel_agency_individual", "Travel agency individual"],
        ["travel_agency_group", "Travel agency group"],
        ["online", "Online"],
        ["free_of_charge", "Free of charge"],
        ["service", "Service"],
      ],
      statusInformation: false,
    });
    this.toggleRoomVisibility = this.toggleRoomVisibility.bind(this);
    this.showSuggestions = this.showSuggestions.bind(this);
    this.selectSuggestion = this.selectSuggestion.bind(this);
    this.showBookingData = this.showBookingData.bind(this);
    this.editBooking = this.editBooking.bind(this);
    onMounted(() => {
      this.state.loading = true;
      this.getBookingData();
      this.occupiedCount();
      // this.actionService.doAction(this.sendCustomNotification());
      document.addEventListener("mousemove", this.handleMouseOver.bind(this));
      document.addEventListener("mouseup", this.endSelection.bind(this));
    });
    onWillUnmount(() => {
      document.removeEventListener("mousemove", this.handleMouseOver.bind(this));
      document.removeEventListener("mouseup", this.endSelection.bind(this));
    });
    onWillStart(async () => {
      try {
        this.state.loading = true;
        let guests = await this.getGuests();
        let ratePlanData = await this.ratePlan();
        let checkTimes = await this.checkTimes();
        let records = await this.getBookingRecords();
        this.state.guests = guests;
        this.state.checkInTime = checkTimes;
        this.state.ratePlanData = ratePlanData;
        this.state.records = records.records;
        let defaultData = await this.getDefaultData();
        this.state.defaultData = defaultData;
        this.renderData(defaultData);
        this.state.roomVisibility = [defaultData[0].room_type];
      } catch (error) {
        console.error("Error fetching default data:", error);
      } finally {
        this.state.loading = false;
      }
    });
  }

  async getDefaultData() {
    try {
      this.state.loading = true;

      const res = await this.rpc("/web/dataset/call_kw", {
        model: "room_inventory.housekeeping",
        method: "get_rooms_by_type",
        args: [],
        kwargs: {},
      });
      return res;
    } catch (error) {
      console.error("Error fetching rooms data by type:", error);
    } finally {
      this.state.loading = false;
    }
  }

  async getGuests() {
    try {
      this.state.loading = true;

      const res = await this.rpc("/web/dataset/call_kw", {
        model: "guest",
        method: "name_search",
        args: [],
        kwargs: {},
      });
      return res;
    } catch (error) {
      console.error("Error fetching rooms data by type:", error);
    } finally {
      this.state.loading = false;
    }
  }

  async getBookingRecords() {
    this.state.loading = true;
    const specification = {
      accommodation: {fields: {display_name: {}}},
      amount_paid: {},
      adults: {},
      arrival_status: {},
      agent_company_id: {fields: {display_name: {}}},
      check_in_date: {},
      check_out_date: {},
      children: {},
      citizenship: {},
      customer_company_id: {fields: {display_name: {}}},
      deposit: {},
      dont_move: {},
      email: {},
      first_name: {},
      gender: {},
      guest_comment: {},
      guest_id: {fields: {display_name: {}}},
      is_front_desk_booking: {},
      // is_front_desk_booking: {},
      is_check_in: {},
      is_paid: {},
      is_check_out: {},
      last_name: {},
      middle_name: {},
      must_pay: {},
      nights: {},
      phone: {},
      price_detail_ids: {fields: {}},
      price_detail_total: {},
      rate_plan: {fields: {display_name: {}}},
      room_number: {fields: {display_name: {}}},
      reception_id: {fields: {display_name: {}}},
      room_type_id: {fields: {display_name: {}}},
      residual: {},
      service_and_accommodation: {},
      status: {},
      total: {},
      unique_id: {},
      booking_status: {},
      total_services_front_desk: {},
      booking_condition: {},
    };

    try {
      const res = await this.orm.call("booking", "web_search_read", [], {
        count_limit: 10001,
        domain: [],
        limit: "",
        offset: 0,
        order: "",
        specification,
      });
      return res;
    } catch (error) {
      console.error(error);
    } finally {
      this.state.loading = false;
    }
  }

  async getRelatedAccommodation() {
    try {
      const res = await this.rpc("/web/dataset/call_kw", {
        model: "accommodation",
        method: "name_search",
        args: [],
        kwargs: {
          args: [
            "&",
            ["booking_unique", "=", this.state.accUniqueId],
            ["vacant", ">", 0],
          ],
          limit: 8,
          name: "",
          operator: "ilike",
        },
      });
      return res;
    } catch (error) {
      console.error("Error fetching accommodation data:", error);
      throw error;
    } finally {
    }
  }

  async ratePlan() {
    try {
      this.state.loading = true;

      const res = await this.orm.call("rate.plan", "name_search", []);
      return res;
    } catch (error) {
      console.error(error);
    } finally {
      this.state.loading = false;
    }
  }

  async checkTimes() {
    try {
      this.state.loading = true;

      const checkTime = await this.orm.call(
        "check.in.check.out.time",
        "name_search",
        []
      );
      return checkTime;
    } catch (error) {
      console.error(error);
    } finally {
      this.state.loading = false;
    }
  }

  async getBookingData() {
    try {
      this.state.loading = true;

      const res = await this.rpc("/web/dataset/call_kw", {
        model: "accommodation",
        method: "get_accommodation_data",
        args: [],
        kwargs: {},
      });
      return res;
    } catch (error) {
      console.error("Error fetching booking data:", error);
    } finally {
      this.state.loading = false;
    }
  }

  generateCalendar(year, month) {
    const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    let date = new Date(year, month, 1);
    const result = [];

    while (date.getMonth() === month) {
      result.push({
        date: date.getDate(),
        day: days[date.getDay() - 1] || "Sun",
      });
      date.setDate(date.getDate() + 1);
    }
    return result;
  }

  onMonthChange(event) {
    const newMonth = event.target.value;
    const [year, month] = newMonth.split("-").map(Number);
    this.state.selectedMonth = newMonth;
    this.state.calendar = this.generateCalendar(year, month - 1);
  }

  toggleRoomVisibility(type) {
    if (this.state.roomVisibility.includes(type)) {
      this.state.roomVisibility.splice(this.state.roomVisibility.indexOf(type), 1);
    } else {
      this.state.roomVisibility.push(type);
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

  recordDate(date) {
    return date;
  }

  recordCalendarDate(day) {
    return `${this.state.selectedMonth}-${String(day).padStart(2, "0")}`;
  }

  disabledCell(day) {
    let today = new Date();
    const [year, month] = this.state.selectedMonth.split("-");
    if (today.getFullYear() <= year && month < today.getMonth() + 1) {
      return true;
    } else if (
      today.getFullYear() >= year &&
      month == today.getMonth() + 1 &&
      day < today.getDate()
    ) {
      return true;
    }
    return false;
  }

  closeModal() {
    this.state.bookingMenu = false;
    this.unmark();
  }

  formatNumber(number) {
    return new Intl.NumberFormat("en-US", {
      style: "decimal",
      useGrouping: true,
      minimumFractionDigits: 0,
      maximumFractionDigits: 20,
    })
      .format(number)
      .replace(/,/g, " ");
  }

  formatTotal(number) {
    return new Intl.NumberFormat("en-US", {
      style: "decimal",
      useGrouping: true,
      minimumFractionDigits: 0,
      maximumFractionDigits: 20,
    }).format(number);
  }

  getTooltipContent(record) {
    const dateIn = new Date(record.check_in_date);
    const dayIn = dateIn.getDate();
    const monthIn = dateIn.toLocaleString("default", {month: "short"});

    const dateOut = new Date(record.check_out_date);
    const dayOut = dateOut.getDate();
    const monthOut = dateOut.toLocaleString("default", {month: "short"});

    return `
       Stay: ${dayIn} ${monthIn}(12:00)-${dayOut} ${monthOut}(14:00)
       Guest: ${record.first_name}
       Total: ${this.formatNumber(record.total)} sum
    `;
  }

  preventClose(event) {
    event.stopPropagation();
  }

  occupiedCount() {
    let today = new Date();
    let formattedDate = today.getDate();
    this.state.records.map((record, index) => {
      if (
        (this.recordDate(record.check_in_date) ==
          this.recordCalendarDate(formattedDate) ||
          (this.recordCalendarDate(formattedDate) >=
            this.recordDate(record.check_in_date) &&
            this.recordDate(record.check_out_date) >
              this.recordCalendarDate(formattedDate))) &&
        record.room_number &&
        record.status == "done"
      ) {
        this.state.occupied += 1;
      }
      if (
        record.arrival_status == "same_day_bookings" &&
        this.recordCalendarDate(formattedDate) == record.check_in_date &&
        record.accommodation &&
        record.status == "done"
      ) {
        this.state.same_day_booking += 1;
      }
      if (
        record.arrival_status == "arrival" &&
        this.recordCalendarDate(formattedDate) == record.check_in_date &&
        record.accommodation &&
        record.status == "done"
      ) {
        this.state.arrival += 1;
      }
      if (
        this.recordCalendarDate(formattedDate) == record.check_out_date &&
        record.accommodation &&
        record.status == "done"
      ) {
        this.state.departure += 1;
      }
    });
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

  startSelection(event) {
    if (event.button !== 0) return;
    this.state.isSelecting = true;
    this.state.isDragging = false;
    const cell = event.currentTarget;
    this.state.startCell = cell;
    this.state.selectedCells.clear();
    this.toggleCellSelection(cell, true);
    event.preventDefault();
    document.addEventListener("mousemove", this.handleMouseOver.bind(this));
  }

  handleMouseOver(event) {
    if (!this.state.isSelecting) return;
    if (!this.state.isDragging) {
      this.state.isDragging = true;
    }
    const target = event.target.closest(".data-container-cell");
    if (target && this.isSameRow(this.state.startCell, target)) {
      this.selectRange(this.state.startCell, target, true);
    }
  }

  endSelection(event) {
    if (this.state.isSelecting) {
      this.state.isSelecting = false;
      if (this.state.selectedCells.size > 1) {
        document.removeEventListener("mousemove", this.handleMouseOver.bind(this));
        if (!this.state.isDragging) {
          this.state.selectedCells.clear();
          this.state.startCell.classList.remove("cell-select");
        } else {
          if (this.state.selectedCells.size > 0) {
            this.createData();
          }
        }
        this.state.isDragging = false;
      } else {
        this.unmark();
      }
    }
  }

  toggleCellSelection(cell, add = true) {
    const cellKey = cell.getAttribute("data-cell-key");
    if (this.state.selectedCells.has(cellKey)) {
      if (!add) {
        this.state.selectedCells.delete(cellKey);
        cell.classList.remove("cell-select");
      }
    } else {
      if (add) {
        this.state.selectedCells.add(cellKey);
        cell.classList.add("cell-select");
      }
    }
  }

  selectRange(startCell, endCell, add = true) {
    const startDate = new Date(startCell.getAttribute("data-day"));
    const endDate = new Date(endCell.getAttribute("data-day"));
    const cells = document.querySelectorAll(".data-container-cell");

    const minDate = startDate < endDate ? startDate : endDate;
    const maxDate = startDate > endDate ? startDate : endDate;

    cells.forEach((cell) => {
      const cellDate = new Date(cell.getAttribute("data-day"));
      if (this.isSameRow(startCell, cell)) {
        this.toggleCellSelection(cell, false);
      }
    });

    // Select new range
    cells.forEach((cell) => {
      const cellDate = new Date(cell.getAttribute("data-day"));
      if (
        cellDate >= minDate &&
        cellDate <= maxDate &&
        this.isSameRow(startCell, cell)
      ) {
        this.toggleCellSelection(cell, add);
      }
    });
  }

  isSameRow(cell1, cell2) {
    return cell1.closest("tr") === cell2.closest("tr");
  }

  unmark() {
    const selectedCells = document.querySelectorAll(".cell-select");
    selectedCells.forEach((cell) => {
      cell.classList.remove("cell-select");
    });
    this.state.selectedCells.clear();
    this.state.bookingMenu = false;
  }

  updateCheckInCheckOutDates() {
    const selectedCells = Array.from(document.querySelectorAll(".cell-select"));
    if (selectedCells.length > 1) {
      const checkInDate = selectedCells[0].getAttribute("data-day");
      const checkOutDate =
        selectedCells[selectedCells.length - 1].getAttribute("data-day");

      document.getElementById("check-in-date").value = checkInDate;
      document.getElementById("check-out-date").value = checkOutDate;
      const checkIn = new Date(checkInDate);
      const checkOut = new Date(checkOutDate);
      const nights = Math.floor((checkOut - checkIn) / (1000 * 60 * 60 * 24));
      document.getElementById("nights").value = nights;

      const roomType = selectedCells[0].getAttribute("room-type");
      const roomNumber = selectedCells[0]
        .closest("tr")
        .querySelector(".room-number").textContent;

      const roomTypeSelect = document.getElementById("room-type");
      roomTypeSelect.value = roomType;
      this.state.defaultData.map((data, index) => {
        data?.rooms?.map((room, roomIndex) => {
          if (room.number == roomNumber) {
            this.state.roomId = room.housekeeping_id;
            this.state.roomTypeId = room.room_type_id;
          }
        });
      });
      document.getElementById("room-number").value = roomNumber;
      if (this.state.accommodation.length > 0) {
        let data = this.state.accommodation.find((item) => item[1].includes(roomType));
        if (data != undefined && +data[0] > 0) {
          document.getElementById("accommodation").value = data[1];
          this.state.accommodationId = data[0];
          this.state.bookingMenu = true;
        } else {
          alert("No any accommodation for this room type");
          this.unmark();
        }
        // for (
        //   let i = this.state.accommodation.length - 1;
        //   i > this.state.accommodation.length - (this.state.defaultData.length + 1);
        //   i--
        // ) {
        //   if (this.state.accommodation[i][1].includes(roomType)) {
        //     document.getElementById("accommodation").value =
        //       this.state.accommodation[i][1];
        //     this.state.accommodationId = this.state.accommodation[i][0];
        //   }
        // }
      }
    }
  }

  sendCustomNotification() {
    return {
      type: "ir.actions.client",
      tag: "display_notification",
      params: {
        type: "info",
        message: `You can create a new booking by selecting at least 2 date slots.`,
      },
    };
  }

  async createData() {
    this.state.loading = true;
    const selectedCells = Array.from(document.querySelectorAll(".cell-select"));
    const roomType = selectedCells[0].getAttribute("room-type-data");
    const recordsToCreate = {
      accommodation: false,
      adults: "1",
      agent_company_id: false,
      check_in_date: selectedCells[0].getAttribute("data-day"),
      check_in_time:
        this.state.checkInTime.length > 0 ? this.state.checkInTime[0][0] : false,
      check_out_date: selectedCells[selectedCells.length - 1].getAttribute("data-day"),
      checkout_time:
        this.state.checkInTime.length > 0 ? this.state.checkInTime[1][0] : false,
      children: "0",
      customer_company_id: false,
      customer_language: false,
      deposit: 0,
      dont_move: false,
      guarantee_method: false,
      guest_comment: false,
      guest_id: false,
      guest_status: false,
      market_segment: false,
      payment_method: false,
      point_of_sale: false,
      price_detail_ids: [],
      purpose_of_visit: false,
      rate_plan: 1,
      room_number: false,
      room_service_ids: [],
      room_type_id: false,
      staff: false,
      status: "created",
      total: 0,
      is_front_desk_booking: false,
    };
    const specification = {
      accommodation: {fields: {display_name: {}}},
      adults: {},
      agent_company_id: {fields: {display_name: {}}},
      available_room_ids: {},
      check_in_date: {},
      check_in_time: {fields: {display_name: {}}},
      check_out_date: {},
      checkout_time: {fields: {display_name: {}}},
      children: {},
      customer_company_id: {fields: {display_name: {}}},
      customer_language: {},
      deposit: {},
      display_name: {},
      dont_move: {},
      guarantee_method: {},
      guest_comment: {},
      guest_id: {fields: {display_name: {}}},
      guest_status: {fields: {display_name: {}}},
      is_front_desk_booking: {},
      market_segment: {fields: {display_name: {}}},
      nights: {},
      payment_method: {fields: {display_name: {}}},
      point_of_sale: {fields: {display_name: {}}},
      price_detail_ids: {
        fields: {
          active: {},
          amount: {},
          date: {},
          discount_id: {fields: {display_name: {}}},
          price: {},
          rate_plan_id: {fields: {display_name: {}}},
        },
        limit: 40,
        order: "",
      },
      purpose_of_visit: {fields: {display_name: {}}},
      rate_plan: {fields: {display_name: {}}},
      room_number: {fields: {display_name: {}}},
      room_service_ids: {
        fields: {
          amount: {},
          included_or_extra: {},
          delivery_date: {},
          price: {},
          quantity: {},
          service_name: {fields: {display_name: {}}},
          service_type: {},
        },
        limit: 40,
        order: "",
      },
      room_type_id: {fields: {}},
      staff: {fields: {display_name: {}}},
      status: {},
      total: {},
      total_services: {},
      total_summary: {},
      unique_id: {},
    };

    try {
      this.orm
        .call("booking", "web_save", [[], recordsToCreate], {specification})
        .then(async (result) => {
          this.state.bookingId = result[0].id;
          this.state.accUniqueId = result[0].unique_id;
          let accommodation = await this.getRelatedAccommodation();
          this.state.accommodation = accommodation;
          this.updateCheckInCheckOutDates();
        });
    } catch (error) {
      console.error("Error creating data: ", error);
    } finally {
      this.state.loading = false;
    }
  }

  async saveData() {
    this.findRoomId(+document.getElementById("room-number").value);
    const selectedCells = Array.from(document.querySelectorAll(".cell-select"));
    const recordsToCreate = {
      accommodation: this.state.accommodationId,
      adults: "1",
      agent_company_id: false,
      check_in_date: selectedCells[0].getAttribute("data-day") || false,
      check_in_time: document.getElementById("checkIn-Time").value || false,
      check_out_date:
        selectedCells[selectedCells.length - 1].getAttribute("data-day") || false,
      checkout_time: document.getElementById("checkOut-Time").value || false,
      children: "0",
      customer_company_id: false,
      customer_language: false,
      deposit: 0,
      dont_move: false,
      guarantee_method: false,
      guest_id: this.state.guestId || false,
      guest_comment: document.getElementById("customerComment").value || false,
      guest_status: false,
      market_segment: false,
      payment_method: false,
      point_of_sale: false,
      email: document.getElementById("email").value || false,
      first_name: document.getElementById("firstName").value || false,
      last_name: document.getElementById("last-name").value || false,
      middle_name: document.getElementById("middleName").value || false,
      phone: document.getElementById("phone").value || false,
      citizenship: document.getElementById("citizenship").value || "uzbekistan",
      price_detail_ids: [],
      purpose_of_visit: false,
      rate_plan: document.getElementById("ratePlan").value || false,
      room_number:
        this.findRoomId(+document.getElementById("room-number").value) || false,
      room_service_ids: [],
      room_type_id: this.state.roomTypeId || false,
      staff: false,
      status: "created",
      total: 0,
      is_front_desk_booking: "front_desk",
    };

    const specification = {
      accommodation: {fields: {display_name: {}}},
      adults: {},
      agent_company_id: {fields: {display_name: {}}},
      available_room_ids: {
        fields: {
          building_id: {fields: {display_name: {}}},
          floor_id: {fields: {display_name: {}}},
          beds_in_room: {},
          comment: {},
          ignore_in_statistics: {},
          number: {},
          room_type: {fields: {display_name: {}}},
        },
        limit: 40,
        order: "",
      },
      check_in_date: {},
      check_in_times: {},
      check_out_date: {},
      check_out_times: {},
      children: {},
      customer_company_id: {fields: {display_name: {}}},
      customer_language: {},
      deposit: {},
      display_name: {},
      dont_move: {},
      guarantee_method: {},
      guest_comment: {},
      guest_id: {fields: {display_name: {}}},
      guest_status: {fields: {display_name: {}}},
      is_front_desk_booking: {},
      market_segment: {fields: {display_name: {}}},
      nights: {},
      payment_method: {fields: {display_name: {}}},
      point_of_sale: {fields: {display_name: {}}},
      price_detail_ids: {
        fields: {
          active: {},
          amount: {},
          date: {},
          discount_id: {fields: {display_name: {}}},
          price: {},
          rate_plan_id: {fields: {display_name: {}}},
        },
        limit: 40,
        order: "",
      },
      purpose_of_visit: {fields: {display_name: {}}},
      rate_plan: {fields: {display_name: {}}},
      room_number: {fields: {display_name: {}}},
      room_service_ids: {
        fields: {
          amount: {},
          included_or_extra: {},
          delivery_date: {},
          price: {},
          quantity: {},
          service_name: {fields: {display_name: {}}},
          service_type: {},
        },
        limit: 40,
        order: "",
      },
      room_type_id: {fields: {}},
      staff: {fields: {display_name: {}}},
      status: {},
      total: {},
      total_services: {},
      total_summary: {},
      unique_id: {},
    };
    try {
      this.state.loading = true;

      const result = await this.orm.call(
        "booking",
        "web_save",
        [[this.state.bookingId], recordsToCreate],
        {specification}
      );
    } catch (error) {
      console.error("Error while creating data: ", error);
    } finally {
      this.saveStatus();
    }
  }

  async saveStatus() {
    const recordsToCreate = {
      status: "done",
    };

    const specification = {
      accommodation: {fields: {display_name: {}}},
      adults: {},
      agent_company_id: {fields: {display_name: {}}},
      available_room_ids: {},
      check_in_date: {},
      check_in_time: {fields: {display_name: {}}},
      check_out_date: {},
      checkout_time: {fields: {display_name: {}}},
      children: {},
      customer_company_id: {fields: {display_name: {}}},
      customer_language: {},
      deposit: {},
      display_name: {},
      dont_move: {},
      guarantee_method: {},
      guest_comment: {},
      guest_id: {fields: {display_name: {}}},
      guest_status: {fields: {display_name: {}}},
      is_front_desk_booking: {},
      market_segment: {fields: {display_name: {}}},
      nights: {},
      payment_method: {fields: {display_name: {}}},
      point_of_sale: {fields: {display_name: {}}},
      price_detail_ids: {
        fields: {
          active: {},
          amount: {},
          date: {},
          discount_id: {fields: {display_name: {}}},
          price: {},
          rate_plan_id: {fields: {display_name: {}}},
        },
        limit: 40,
        order: "",
      },
      purpose_of_visit: {fields: {display_name: {}}},
      rate_plan: {fields: {display_name: {}}},
      room_number: {fields: {display_name: {}}},
      room_service_ids: {
        fields: {
          amount: {},
          included_or_extra: {},
          delivery_date: {},
          price: {},
          quantity: {},
          service_name: {fields: {display_name: {}}},
          service_type: {},
        },
        limit: 40,
        order: "",
      },
      room_type_id: {fields: {}},
      staff: {fields: {display_name: {}}},
      status: {},
      total: {},
      total_services: {},
      total_summary: {},
      unique_id: {},
    };
    try {
      this.state.loading = true;

      const result = await this.orm.call(
        "booking",
        "web_save",
        [[this.state.bookingId], recordsToCreate],
        {specification}
      );
    } catch (error) {
      console.error("Error while creating data: ", error);
    } finally {
      let records = await this.getBookingRecords();
      this.state.records = records.records;
      this.state.bookingMenu = false;
      this.state.suggestions = [];
      document.getElementById("firstName").value = "";
      document.getElementById("last-name").value = "";
      document.getElementById("email").value = "";
      this.unmark();
    }
  }

  showSuggestions(value) {
    if (value.length === 0) {
      this.state.suggestions = [];
      return;
    }

    const filteredGuests = this.state.guests.filter((guest) =>
      guest[1].toLowerCase().includes(value.toLowerCase())
    );

    this.state.suggestions = filteredGuests.map((guest) => guest);
  }

  selectSuggestion(suggestion) {
    this.state.guestId = suggestion[0];
    const [firstName, lastName] = suggestion[1].split(" ");
    document.getElementById("firstName").value = firstName;
    document.getElementById("last-name").value = lastName;
    this.state.suggestions = [];
  }

  async closeModalBooking() {
    this.state.isModal = false;
    let records = await this.getBookingRecords();
    this.state.records = records.records;
  }

  async checkGuest() {
    const personData = {
      apartment: false,
      birthday: false,
      birthday_country: false,
      citizenship: document.getElementById("citizenship").value || false,
      city: false,
      comment_for_guest: false,
      // corpus: false,
      country_id: false,
      district: false,
      document: false,
      email: document.getElementById("email").value || false,
      email_ids: [],
      first_name: document.getElementById("firstName").value,
      guest_company_id: false,
      home: false,
      last_name: document.getElementById("last-name").value || false,
      legal_representative_id: [],
      middle_name: document.getElementById("middleName").value || false,
      phone: document.getElementById("phone").value || false,
      phone_ids: [],
      region: false,
      settlement: false,
      sex: false,
      street: false,
      zip_code: 0,
    };

    const specification = {
      apartment: {},
      birthday: {},
      birthday_country: {
        fields: {
          display_name: {},
        },
      },
      citizenship: {},
      city: {},
      comment_for_guest: {},
      // corpus: {},
      country_id: {
        fields: {
          display_name: {},
        },
      },
      display_name: {},
      district: {},
      document: {},
      email: {},
      email_ids: {
        fields: {
          email: {},
        },
        limit: 40,
        order: "",
      },
      first_name: {},
      full_name: {},
      guest_company_id: {
        fields: {
          display_name: {},
        },
      },
      home: {},
      last_name: {},
      legal_representative_id: {
        fields: {
          last_name: {},
          first_name: {},
          middle_name: {},
          sex: {},
          birthday: {},
          citizenship: {},
          degree_of_kinship: {},
        },
        limit: 40,
        order: "",
      },
      middle_name: {},
      phone: {},
      phone_ids: {
        fields: {
          guest_id: {
            fields: {
              display_name: {},
            },
          },
          phone: {},
        },
        limit: 40,
        order: "",
      },
      region: {},
      settlement: {},
      sex: {},
      // status: {},
      street: {},
      zip_code: {},
    };

    if (personData.last_name === "" || personData.first_name === "") {
      return;
    }

    if (this.state.guestId !== false) {
      this.saveData();
    }
    if (this.state.guestId == false) {
      try {
        this.state.loading = true;

        const res = await this.rpc("/web/dataset/call_kw", {
          model: "guest",
          method: "web_save",
          args: [[], personData],
          kwargs: {specification},
        });
        this.state.guestId = res[0].id;
        this.saveData();
      } catch (error) {
        console.error("Error fetching rooms data by type:", error);
      } finally {
        this.state.loading = false;
      }
    }
  }

  showBookingData(data) {
    this.state.displayedDataId = data.id;
    let booking_status = "";
    switch (data.booking_condition) {
      case "new_booking":
        booking_status = "New Booking";
        break;
      case "without_room":
        booking_status = "Without Room";
        break;
      case "checked_in":
        booking_status = "Checked In";
        break;
      case "checked_out":
        booking_status = "Checked Out";
        break;
      case "did_not_go":
        booking_status = "Did Not Go";
        break;
      case "checkout_expired":
        booking_status = "Checkout Expired";
        break;
      case "late":
        booking_status = "Late";
        break;
      default:
        booking_status = "";
    }

    switch (data.booking_condition) {
      case "without_room":
        document.getElementById("bookStatus").className = "book_without_room_status";
        break;
      case "checked_in":
        document.getElementById("bookStatus").className = "checked_in_status";
        break;
      case "checked_out":
        document.getElementById("bookStatus").className = "departured_status";
        break;
      case "checkout_expired":
        document.getElementById("bookStatus").className = "";
        break;
      case "did_not_go":
        document.getElementById("bookStatus").className = "do_not_come_status";
        break;
      case "late":
        document.getElementById("bookStatus").className = "do_not_come_status";
        break;
      case "new_booking":
        document.getElementById("bookStatus").className = "new_booking_status";
        break;
      default:
        document.getElementById("bookStatus").className = "booking-status-p";
        break;
    }
    document.getElementById("bookStatus").innerText = booking_status || " ";
    document.getElementById("bookName").innerText = data.guest_id.display_name || " ";
    document.getElementById("bookNumber").innerText = data.unique_id;
    document.getElementById("bookPhone").innerText = data.phone || " ";
    document.getElementById("guestComment").innerText = data.guest_comment || " ";
    document.getElementById("bookCheckIn").innerText = data.check_in_date;
    document.getElementById("bookCheckOut").innerText = data.check_out_date;
    document.getElementById("bookNights").innerText = data.nights || " ";
    document.getElementById("bookRatePlan").innerText =
      data.rate_plan.display_name || document.getElementById("ratePlan").value;
    // document.getElementById("bookGuest").innerText = data.guest_id.display_name || " ";
    document.getElementById("bookRoomType2").innerText =
      data.room_type_id.display_name || " ";
    document.getElementById("bookRoomNumber").innerText = data.room_number.display_name;
    document.getElementById("bookAdults").innerText = data.adults;
    document.getElementById("bookChildren").innerText = data.children;
    if ((data.is_front_desk_booking = "front_desk")) {
      let front_desk_booking = "via front desk";
      document.getElementById("bookSale").innerText = front_desk_booking;
    }
    if (data.is_paid) {
      document.getElementById("bookPaymentStatus").innerText = "Paid";
      document.getElementById("bookPaymentStatus").className = "booking-status-p";
    } else {
      document.getElementById("bookPaymentStatus").innerText = "Not paid";
      document.getElementById("bookPaymentStatus").className =
        "booking-status-warning-p";
    }
    document.getElementById("bookTotal").innerText = `${this.formatTotal(
      data.total
    )} UZS`;
    document.getElementById("bookPaid").innerText = `${data.amount_paid} UZS`;
    document.getElementById("bookAccommodation").innerText = `${this.formatTotal(
      data.total
    )} UZS`;
    let outstanding = data.total - data.amount_paid;
    document.getElementById("bookBalance").innerText = `${outstanding} UZS`;
    document.getElementById(
      "bookServices"
    ).innerText = `${data.total_services_front_desk} UZS`;

    document
      .getElementById("copy-booking-number")
      .addEventListener("click", function () {
        const bookingNumberText = document.getElementById("bookNumber").textContent;
        const tempInput = document.createElement("input");
        tempInput.value = bookingNumberText;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand("copy");
        document.body.removeChild(tempInput);
        alert("Booking number copied to clipboard: " + bookingNumberText);
      });

    this.checkInActive(data);

    this.state.isModal = true;
    document.getElementById("bookNumber").addEventListener("click", () => {
      this.receptionModal(data);
    });
  }

  setCheckInTime() {
    if (this.state.checkInTime.length > 0) {
      return this.state.checkInTime[0][1];
    }
    return "14:00";
  }

  setCheckOutTime() {
    if (this.state.checkInTime.length > 0) {
      return this.state.checkInTime[1][1];
    }
    return "12:00";
  }

  checkVacantRoom(day, room) {
    const totalRooms = room.count;
    const bookedRooms = this.state.records.filter((record) => {
      return (
        (this.recordDate(record.check_in_date) == this.recordCalendarDate(day.date) ||
          (this.recordCalendarDate(day.date) >= this.recordDate(record.check_in_date) &&
            this.recordDate(record.check_out_date) >
              this.recordCalendarDate(day.date))) &&
        record.room_type_id.display_name == room.room_type &&
        record.status == "done"
      );
    }).length;
    return totalRooms - bookedRooms;
  }

  editBooking() {
    this.actionService
      .doAction(
        {
          type: "ir.actions.act_window",
          context: {
            create: false,
          },
          res_model: "booking",
          res_id: this.state.displayedDataId,
          name: "Booking",
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

  checkInActive(record) {
    this.state.canCheckInCancel = false;
    this.state.canCheckOutCancel = false;
    this.state.canCheckIn = false;
    this.state.canCheckOut = false;
    this.state.canPay = false;
    this.state.canNote = true;
    this.state.canMoveRoom = false;
    if (
      new Date() >= new Date(record.check_in_date) &&
      record.booking_condition != "checked_in" &&
      record.booking_condition != "checked_out" &&
      record.booking_condition != "did_not_go"
    ) {
      (document.getElementById("bookingNumber").innerText = record.unique_id),
        (document.getElementById("roomType").innerText =
          record.room_type_id.display_name),
        (document.getElementById("roomNumber").innerText =
          record.room_number.display_name),
        this.setDateTimeInputs();
      this.state.willSavedData = record;
      this.state.canCheckIn = true;
    }
    if (
      new Date() >= new Date(record.check_in_date) &&
      record.booking_condition === "checked_in"
    ) {
      (document.getElementById(
        "bookingNumberCancel"
      ).innerText = `Booking No.${record.unique_id}`),
        (this.state.willSavedData = record);
      this.state.canCheckInCancel = true;
    }
    if (
      new Date() >= new Date(record.check_out_date) &&
      record.booking_condition === "checked_out"
    ) {
      (document.getElementById(
        "bookingNumberCancelOut"
      ).innerText = `Booking No.${record.unique_id}`),
        (this.state.willSavedData = record);
      this.state.canCheckOutCancel = true;
    }
    if (
      new Date(record.check_out_date) <= new Date() &&
      record.booking_condition != "checked_out" &&
      record.booking_condition != "new_booking" &&
      record.is_check_in
    ) {
      (document.getElementById("bookingNumberOut").innerText = record.unique_id),
        (document.getElementById("roomTypeOut").innerText =
          record.room_type_id.display_name),
        (document.getElementById("roomNumberOut").innerText =
          record.room_number.display_name),
        this.setDateOutTimeInputs();
      this.state.willSavedData = record;
      this.state.checkOutPayment = record.is_paid;
      this.state.canCheckOut = true;
    }
    if (new Date(record.check_out_date) >= new Date() && !record.dont_move) {
      this.state.canMoveRoom = true;
    }
    if (!record.is_paid) {
      this.state.canPay = true;
    }
    this.setNoteTimeInputs();
    this.state.noteData = record;
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

  setDateOutTimeInputs() {
    const dateInput = document.getElementById("checkDateOut");
    const timeInput = document.getElementById("checkTimeOut");

    const currentDate = new Date();

    dateInput.value = this.formatDate(currentDate);
    timeInput.value = this.formatTime(currentDate);
  }

  setNoteTimeInputs() {
    const dateInput = document.getElementById("noteDate");
    const timeInput = document.getElementById("noteTime");

    const currentDate = new Date();

    dateInput.value = this.formatDate(currentDate);
    timeInput.value = this.formatTime(currentDate);
  }

  async saveCheckInData() {
    const updatedData = [
      {
        booking_id: this.state.willSavedData.id,
        check_in_date: document.getElementById("checkDate").value,
        check_in_time: false,
      },
    ];

    let specification = {
      check_in_date: {},
      check_in_time: {
        fields: {
          display_name: {},
        },
      },
      display_name: {},
      booking_id: {
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
        model: "booking.check_in",
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
      this.state.isModal = false;
      let records = await this.getBookingRecords();
      this.state.records = records.records;
    }
  }

  async saveCheckOutData() {
    const updatedData = [
      {
        booking_id: this.state.willSavedData.id,
        check_out_date: document.getElementById("checkDateOut").value,
      },
    ];

    let specification = {
      check_out_date: {},
      check_out_times: {},
      display_name: {},
      booking_id: {
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
        model: "booking.check_out",
        method: "web_save",
        args: [[], updatedData],
        kwargs: {specification},
      });
      return res;
    } catch (error) {
      console.error("Error fetching rule data:", error);
    } finally {
      this.state.isCheckOutActive = false;
      let records = await this.getBookingRecords();
      this.state.records = records.records;
      this.state.isModal = false;
    }
  }

  async moveRoom() {
    let action_id = 0;
    try {
      const res = await this.rpc("/web/dataset/call_button", {
        model: "booking",
        method: "action_move_room",
        args: [[this.state.displayedDataId]],
        kwargs: {},
      });
      action_id = res.res_id;
      return res;
    } catch (error) {
      console.error("Error moving data:", error);
    } finally {
      this.openMoveModel(action_id);
    }
  }

  async cancelBooking() {
    let action_id = 0;
    try {
      const res = await this.rpc("/web/dataset/call_button", {
        model: "booking",
        method: "action_cancel",
        args: [[this.state.displayedDataId]],
        kwargs: {},
      });
      action_id = res.res_id;
      return res;
    } catch (error) {
      console.error("Error moving data:", error);
    } finally {
      this.openCancelModel(action_id);
    }
  }

  async savePayment() {
    let action_id = 0;
    try {
      const res = await this.rpc("/web/dataset/call_button", {
        model: "booking",
        method: "action_pay",
        args: [[this.state.displayedDataId]],
        kwargs: {},
      });
      action_id = res.res_id;
      return res;
    } catch (error) {
      console.error("Error moving data:", error);
    } finally {
      this.openPaymentModel(action_id);
    }
  }

  async saveNote() {
    let time = document.getElementById("noteTime").value;
    let date = document.getElementById("noteDate").value;
    let specification = {
      booking_id: {fields: {display_name: {}}},
      reception_id: {fields: {display_name: {}}},
      text: {},
      status: {},
      scheduled: {},
      status: {},
      text: {},
    };
    let updatedData = [];
    if (document.getElementById("noteSelection").value == "scheduled") {
      updatedData = [
        {
          booking_id: this.state.noteData.id,
          reception_id: false,
          status: document.getElementById("noteSelection").value,
          text: document.getElementById("noteArea").value.trim(),
          scheduled: `${date} ${time}`,
        },
      ];
    } else {
      updatedData = [
        {
          booking_id: this.state.noteData.id,
          reception_id: false,
          status: document.getElementById("noteSelection").value,
          text: document.getElementById("noteArea").value.trim(),
        },
      ];
    }
    try {
      const res = await this.rpc("/web/dataset/call_kw", {
        model: "notes_and_instructions",
        method: "web_save",
        args: [[], updatedData],
        kwargs: {specification},
      });
      return res;
    } catch (error) {
      console.error("Error moving data:", error);
    } finally {
      this.closeNoteModal();
      let records = await this.getBookingRecords();
      this.state.records = records.records;
      this.state.isModal = false;
    }
  }

  async openMoveModel(id) {
    this.actionService
      .doAction(
        {
          type: "ir.actions.act_window",
          context: {
            create: false,
          },
          res_model: "front_desk.move_room",
          res_id: id,
          name: "Booking",
          target: "new",
          views: [[false, "form"]],
          flags: {mode: "edit"},
        },
        {clearBreadcrumbs: false}
      )
      .catch((error) => {
        console.error(`Action does not exist or failed:`, error);
      });
  }

  async openCancelModel(id) {
    this.actionService
      .doAction(
        {
          type: "ir.actions.act_window",
          context: {
            create: false,
          },
          res_model: "front_desk.cancel_booking",
          res_id: id,
          name: "Booking",
          target: "new",
          views: [[false, "form"]],
          flags: {mode: "edit"},
        },
        {clearBreadcrumbs: false}
      )
      .catch((error) => {
        console.error(`Action does not exist or failed:`, error);
      });
  }

  async openPaymentModel(id) {
    this.actionService
      .doAction(
        {
          type: "ir.actions.act_window",
          context: {
            create: false,
          },
          res_model: "reception.payment",
          res_id: id,
          name: "Payment",
          target: "new",
          views: [[false, "form"]],
          flags: {mode: "edit"},
        },
        {clearBreadcrumbs: false}
      )
      .catch((error) => {
        console.error(`Action does not exist or failed:`, error);
      });
  }

  async cancelCheckIn() {
    if (!(document.getElementById("cancelCheckInArea").value.trim().length > 0)) {
      this.state.isReasonEmpty = true;
    } else {
      this.state.isReasonEmpty = false;
      const updatedData = [
        {
          booking_id: this.state.willSavedData.id,
          reason: document.getElementById("cancelCheckInArea").value.trim(),
        },
      ];

      let specification = {
        booking_id: {fields: {display_name: {}}},
        reason: {},
        display_name: {},
      };
      try {
        const res = await this.rpc("/web/dataset/call_kw", {
          model: "front_desk.cancel_checkin",
          method: "web_save",
          args: [[], updatedData],
          kwargs: {specification},
        });
        specification = {};
        return res;
      } catch (error) {
        console.error("Error fetching rule data:", error);
      } finally {
        let records = await this.getBookingRecords();
        this.state.records = records.records;
        this.state.isCheckInCancelActive = false;
        this.state.isModal = false;
      }
    }
  }

  async cancelCheckOut() {
    if (!(document.getElementById("cancelCheckOutArea").value.trim().length > 0)) {
      this.state.isReasonOutEmpty = true;
    } else {
      this.state.isReasonOutEmpty = false;
      const updatedData = [
        {
          booking_id: this.state.willSavedData.id,
          reason: document.getElementById("cancelCheckOutArea").value.trim(),
        },
      ];

      let specification = {
        booking_id: {fields: {display_name: {}}},
        reason: {},
        display_name: {},
      };
      try {
        const res = await this.rpc("/web/dataset/call_kw", {
          model: "front_desk.cancel_checkout",
          method: "web_save",
          args: [[], updatedData],
          kwargs: {specification},
        });
        return res;
      } catch (error) {
        console.error("Error cancelling check-out data:", error);
      } finally {
        let records = await this.getBookingRecords();
        this.state.records = records.records;
        this.state.isCheckOutCancelActive = false;
        this.state.isModal = false;
      }
    }
  }

  checkCharacters(e) {
    e.preventDefault();
    let maxLength = 1000;
    const textArea = document.getElementById("noteArea");
    // const remainingChars = maxLength - e.target.value.trim().length;
    this.state.charCounter = `${
      maxLength - textArea.value.trim().length
    } characters left`;
  }

  closeNoteModal() {
    const textArea = document.getElementById("noteArea");
    textArea.value = "";
    this.state.charCounter = "1000 characters left";
    this.state.isNoteActive = false;
  }

  noteSelection(e) {
    e.preventDefault();
    if (e.target.value == "scheduled") {
      this.state.noteTimeReadonly = false;
    } else {
      this.state.noteTimeReadonly = true;
    }
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
          res_id: data.reception_id?.id,
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

  findRoomId(roomValue) {
    let roomId;
    this.state.defaultData.map((data) => {
      data.rooms.map((room) => {
        if (room.number == roomValue) {
          roomId = +room.housekeeping_id;
        }
      });
    });

    return roomId;
  }
}

FrontDeskRenderer.template = "hms_app.FrontDesk";
