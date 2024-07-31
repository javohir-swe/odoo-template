/* @odoo-module */

import {Component, useState, onMounted, onWillStart, onWillUnmount} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {standardFieldProps} from "@web/views/fields/standard_field_props";

class DayPilotScheduler extends Component {
  static props = {
    ...standardFieldProps,
  };

  setup() {
    this.orm = useService("orm");
    this.rpc = useService("rpc");
    this.action = useService("action");
    const savedYears = JSON.parse(localStorage.getItem("selectedYears")) || ["2024"];
    const {days, maxWeeks} = this.generateCalendar("2024");
    this.state = useState({
      paymentMethods: {},
      checkedMethods: {},
      timeMethods: {},
      methodsVisible: false,
      timesVisible: false,
      activeTab: "menu3",
      activeYear: "2024",
      activeMonth: new Date().getMonth(),
      selectedYears: savedYears,
      roomtypes: [],
      days: days,
      maxWeeks: maxWeeks,
      dayss: this.generateCalendarRoom("2024", new Date().getMonth()),
      statusMap: {},
      ctaMap: {},
      ctdMap: {},
      minlosMap: {},
      minAdvBookingMap: {},
      minlosArrivalMap: {},
      maxlosArrivalMap: {},
      maxlosMap: {},
      priceMap: {},
      stayMap: {},
      fullLosMap: {},
      showLegend: false,
      hidePreviousMonths:
        JSON.parse(localStorage.getItem("hidePreviousMonths")) || false,
      form: {
        roomType: "",
        date: "",
        status: "close",
        ratePlanId: this.env.model.config.resId,
        closeId: this.env.model.config.resId,
        isVisible: false,
        roomTypeData: [],
      },
      ctaForm: {
        roomType: "",
        date: "",
        status: "close",
        ratePlanId: this.env.model.config.resId,
        filterId: this.env.model.config.resId,
        isVisible: false,
        roomTypeData: [],
      },
      ctdForm: {
        roomType: "",
        date: "",
        status: "close",
        ratePlanId: this.env.model.config.resId,
        filterId: this.env.model.config.resId,
        isVisible: false,
        roomTypeData: [],
      },
      minlosForm: {
        roomType: "",
        roomTypeName: "",
        date: "",
        minlos: 1,
        ratePlanId: this.env.model.config.resId,
        filterId: this.env.model.config.resId,
        isVisible: false,
      },
      minAdvBookingForm: {
        roomType: "",
        roomTypeName: "",
        date: "",
        minAdvBooking: 1,
        ratePlanId: this.env.model.config.resId,
        filterId: this.env.model.config.resId,
        isVisible: false,
      },
      maxAdvBookingForm: {
        roomType: "",
        roomTypeName: "",
        date: "",
        maxAdvBooking: 1,
        ratePlanId: this.env.model.config.resId,
        filterId: this.env.model.config.resId,
        isVisible: false,
      },
      minlosArrivalForm: {
        roomType: "",
        roomTypeName: "",
        date: "",
        minlosArrival: 1,
        ratePlanId: this.env.model.config.resId,
        filterId: this.env.model.config.resId,
        isVisible: false,
      },
      maxlosArrivalForm: {
        roomType: "",
        roomTypeName: "",
        date: "",
        maxlosArrival: 1,
        ratePlanId: this.env.model.config.resId,
        filterId: this.env.model.config.resId,
        isVisible: false,
      },
      maxlosForm: {
        roomType: "",
        roomTypeName: "",
        date: "",
        maxlos: null,
        ratePlanId: this.env.model.config.resId,
        filterId: this.env.model.config.resId,
        isVisible: false,
      },
      priceForm: {
        roomType: "",
        roomTypeName: "",
        date: "",
        price: 0,
        ratePlanId: this.env.model.config.resId,
        filterId: this.env.model.config.resId,
        isVisible: false,
      },
      fullLosForm: {
        roomType: "",
        roomTypeName: "",
        date: "",
        long_of_stay: [],
        ratePlanId: this.env.model.config.resId,
        filterId: this.env.model.config.resId,
        isVisible: false,
      },
      stayForm: {
        roomType: "",
        roomTypeName: "",
        date: "",
        status: false,
        ratePlanId: this.env.model.config.resId,
        filterId: this.env.model.config.resId,
        isVisible: false,
      },
      paymentForm: {
        roomType: "",
        roomTypeName: "",
        date: "",
        status: false,
        ratePlanId: this.env.model.config.resId,
        filterId: this.env.model.config.resId,
        isVisible: false,
      },
      checkForm: {
        roomType: "",
        roomTypeName: "",
        date: "",
        ratePlanId: this.env.model.config.resId,
        filterId: this.env.model.config.resId,
        isVisible: false,
      },
      selectedCells: new Set(),
      startCell: null,
      endCell: null,
      showType: "by_months",
      activeRoomType: null,
      loading: false,
    });
    this.ratePlanId = this.env.model.config.resId;
    this.openActivity = this.openActivity.bind(this);
    this.discardForm = this.discardForm.bind(this);
    // this.openMinlosActivity = this.openMinlosActivity.bind(this);
    this.discardMinlosForm = this.discardMinlosForm.bind(this);
    this.switchTab = this.switchTab.bind(this);
    this.toggleYear = this.toggleYear.bind(this);
    this.switchMonth = this.switchMonth.bind(this);
    this.toggleHidePreviousMonths = this.toggleHidePreviousMonths.bind(this);
    this.selectCell = this.selectCell.bind(this);
    this.unmarkCells = this.unmarkCells.bind(this);
    this.changeValue = this.changeValue.bind(this);
    this.saveStatus = this.saveStatus.bind(this);
    this.discardForm = this.discardForm.bind(this);
    this.closeMethodsMenu = this.closeMethodsMenu.bind(this);
    this.isSelecting = false;
    this.startSelection = this.startSelection.bind(this);
    this.handleMouseOver = this.handleMouseOver.bind(this);
    this.endSelection = this.endSelection.bind(this);
    onMounted(async () => {
      this.state.loading = true;
      await this.fetchRatePlanFields();
      this.state.loading = false;
      this.state.activeRoomType =
        this.state.roomtypes.length > 0 ? this.state.roomtypes[0].id : null;
    });
    onWillStart(async () => {
      try {
        let methods = await this.getMethods();
        let times = await this.getTimes();
        this.state.paymentMethods = methods;
        this.state.timeMethods = times;
      } catch (error) {
        console.error("Error fetching default data:", error);
      }
    });
  }

  getPaymentDataLength(status_key) {
    const paymentEntry = this.state.paymentMap.find(
      (payment) => payment.key === status_key
    );
    return paymentEntry ? paymentEntry.data.length : "0";
  }
  getCheckTimeLength(status_key) {
    // if(this.state.checkMap.length > 0){
    //   this.state.checkMap.map((data, index) => {
    //     if(data.relevant_date == status_key){
    //       return "1"
    //     }
    //   });
    // }

    return "0";
  }

  async getMethods() {
    try {
      this.state.loading = true;

      const res = await this.rpc("/web/dataset/call_kw", {
        model: "payment.methods.for.guests",
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
  async getTimes() {
    try {
      this.state.loading = true;

      const res = await this.rpc("/web/dataset/call_kw", {
        model: "check.in.check.out.roles",
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

  setActiveRoomType(event) {
    event.preventDefault();
    const roomTypeId = event.currentTarget.dataset.roomTypeId;
    this.state.activeRoomType = roomTypeId;
  }
  toggleLegend() {
    this.state.showLegend = !this.state.showLegend;
  }
  handleClickOverlay(event) {
    if (this.state.showLegend) {
      this.toggleLegend();
    }
  }

  startSelection(event) {
    if (event.button !== 0) return; // Only proceed if left mouse button is clicked
    this.isSelecting = true;
    this.isDeselecting = false; // Track if we are in deselection mode
    const cell = event.currentTarget;
    this.state.startCell = cell; // Track the starting cell
    this.state.initiallySelectedCells = new Set(this.state.selectedCells); // Save the initial state of selected cells
    this.toggleCellSelection(cell);
    event.preventDefault(); // Prevent text selection
  }
  endSelection() {
    this.isSelecting = false;
  }
  handleMouseOver(event) {
    const target = event.currentTarget;
    if (target.tagName.toLowerCase() === "td" && this.isSelecting) {
      this.state.endCell = target; // Track the ending cell
      this.selectRange(this.state.startCell, this.state.endCell); // Select range of cells
    }
  }
  selectRange(startCell, endCell) {
    if (!startCell || !endCell) return;

    const startRow = startCell.parentElement;
    const endRow = endCell.parentElement;
    const startRowIndex = Array.from(startRow.parentElement.children).indexOf(startRow);
    const endRowIndex = Array.from(endRow.parentElement.children).indexOf(endRow);
    const startColIndex = Array.from(startRow.children).indexOf(startCell);
    const endColIndex = Array.from(endRow.children).indexOf(endCell);

    const minRowIndex = Math.min(startRowIndex, endRowIndex);
    const maxRowIndex = Math.max(startRowIndex, endRowIndex);
    const minColIndex = Math.min(startColIndex, endColIndex);
    const maxColIndex = Math.max(startColIndex, endColIndex);

    // Restore initial selection state before applying the new range
    this.state.selectedCells = new Set(this.state.initiallySelectedCells);

    for (let rowIndex = minRowIndex; rowIndex <= maxRowIndex; rowIndex++) {
      for (let colIndex = minColIndex; colIndex <= maxColIndex; colIndex++) {
        const cell = startRow.parentElement.children[rowIndex].children[colIndex];
        const cellDate = new Date(cell.getAttribute("data-day"));
        if (!this.isPastDate(cellDate)) {
          this.toggleCellSelection(cell, true);
        }
      }
    }

    // Apply the changes to the DOM
    this.applySelectionToDOM();
  }
  clearHighlight() {
    // This method can be used when you explicitly need to clear all selections
    document.querySelectorAll(".selected").forEach((cell) => {
      cell.classList.remove("selected");
    });
    this.state.selectedCells.clear();
  }
  toggleCellSelection(cell, multiSelect = false) {
    const day = cell.getAttribute("data-day");
    const roomTypeId = cell.getAttribute("data-room-type-id");
    if (day && roomTypeId) {
      const cellKey = `${day}-${roomTypeId}`;
      const cellDate = new Date(day);
      if (this.isPastDate(cellDate)) {
        if (!multiSelect && this.state.selectedCells.has(cellKey)) {
          // Allow deselection of past dates only in single selection mode
          this.state.selectedCells.delete(cellKey);
        }
        return; // Prevent any further action on past dates
      }
      if (this.state.selectedCells.has(cellKey)) {
        if (!this.isDeselecting) {
          this.isDeselecting = true;
        }
        this.state.selectedCells.delete(cellKey);
      } else {
        if (this.isDeselecting) {
          this.isDeselecting = false;
        }
        this.state.selectedCells.add(cellKey);
      }
    }
  }
  applySelectionToDOM() {
    document.querySelectorAll(".day-cell").forEach((cell) => {
      const day = cell.getAttribute("data-day");
      const roomTypeId = cell.getAttribute("data-room-type-id");
      const cellKey = `${day}-${roomTypeId}`;
      if (this.state.selectedCells.has(cellKey)) {
        cell.classList.add("selected");
      } else {
        cell.classList.remove("selected");
      }
    });
  }
  selectCell(cell) {
    const day = cell.getAttribute("data-day");
    const roomTypeId = cell.getAttribute("data-room-type-id");
    if (day && roomTypeId) {
      const cellKey = `${day}-${roomTypeId}`;
      if (this.state.selectedCells.has(cellKey)) {
        this.state.selectedCells.delete(cellKey);
        cell.classList.remove("selected");
      } else {
        this.state.selectedCells.add(cellKey);
        cell.classList.add("selected");
      }
    }
  }
  unmarkCells() {
    this.state.selectedCells.forEach((cellKey) => {
      const cell = document.querySelector(`[data-cell-key="${cellKey}"]`);
      if (cell) {
        cell.classList.remove("selected");
      }
    });
    this.state.selectedCells.clear();
  }

  changeValue() {
    const roomTypeStatusMap = {};
    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const key = `${year}-${month}-${day}-${roomTypeId}`;
      const status = this.state.statusMap[key];
      if (!roomTypeStatusMap[roomTypeId]) {
        roomTypeStatusMap[roomTypeId] = new Set();
      }
      if (status) {
        roomTypeStatusMap[roomTypeId].add(status);
      }
    });

    this.state.form.statusMap = {};
    for (const roomTypeId in roomTypeStatusMap) {
      const statuses = roomTypeStatusMap[roomTypeId];
      if (statuses.size === 1) {
        this.state.form.statusMap[roomTypeId] = [...statuses][0];
      } else {
        this.state.form.statusMap[roomTypeId] = "";
      }
    }

    this.state.form.isVisible = true;
  }
  changeCtaValue() {
    const roomTypeCtaMap = {};
    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const key = `${year}-${month}-${day}-${roomTypeId}`;
      const status = this.state.ctaMap[key];
      if (!roomTypeCtaMap[roomTypeId]) {
        roomTypeCtaMap[roomTypeId] = new Set();
      }
      if (status) {
        roomTypeCtaMap[roomTypeId].add(status);
      }
    });

    this.state.ctaForm.ctaMap = {};
    for (const roomTypeId in roomTypeCtaMap) {
      const statuses = roomTypeCtaMap[roomTypeId];
      if (statuses.size === 1) {
        this.state.ctaForm.ctaMap[roomTypeId] = [...statuses][0];
      } else {
        this.state.ctaForm.ctaMap[roomTypeId] = "";
      }
    }

    this.state.ctaForm.isVisible = true;
  }
  changeCtdValue() {
    const roomTypeCtdMap = {};
    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const key = `${year}-${month}-${day}-${roomTypeId}`;
      const status = this.state.ctdMap[key];
      if (!roomTypeCtdMap[roomTypeId]) {
        roomTypeCtdMap[roomTypeId] = new Set();
      }
      if (status) {
        roomTypeCtdMap[roomTypeId].add(status);
      }
    });

    this.state.ctdForm.ctdMap = {};
    for (const roomTypeId in roomTypeCtdMap) {
      const statuses = roomTypeCtdMap[roomTypeId];
      if (statuses.size === 1) {
        this.state.ctdForm.ctdMap[roomTypeId] = [...statuses][0];
      } else {
        this.state.ctdForm.ctdMap[roomTypeId] = "";
      }
    }

    this.state.ctdForm.isVisible = true;
  }
  changeMinLosValue() {
    const roomTypeMinlosMap = {};
    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const key = `${year}-${month}-${day}-${roomTypeId}`;
      const minlos = this.state.minlosMap[key];
      if (!roomTypeMinlosMap[roomTypeId]) {
        roomTypeMinlosMap[roomTypeId] = new Set();
      }
      if (minlos) {
        roomTypeMinlosMap[roomTypeId].add(minlos);
      }
    });

    this.state.minlosForm.minlosMap = {};
    for (const roomTypeId in roomTypeMinlosMap) {
      const minloses = roomTypeMinlosMap[roomTypeId];
      if (minloses.size === 1) {
        this.state.minlosForm.minlosMap[roomTypeId] = [...minloses][0];
      } else {
        this.state.minlosForm.minlosMap[roomTypeId] = "";
      }
    }

    this.state.minlosForm.isVisible = true;
  }
  changeMinAdvBookingValue() {
    const roomTypeMinAdvBookingMap = {};
    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const key = `${year}-${month}-${day}-${roomTypeId}`;
      const minAdvBooking = this.state.minAdvBookingMap[key];
      if (!roomTypeMinAdvBookingMap[roomTypeId]) {
        roomTypeMinAdvBookingMap[roomTypeId] = new Set();
      }
      if (minAdvBooking) {
        roomTypeMinAdvBookingMap[roomTypeId].add(minAdvBooking);
      }
    });

    this.state.minAdvBookingForm.minAdvBookingMap = {};
    for (const roomTypeId in roomTypeMinAdvBookingMap) {
      const minAdvBookings = roomTypeMinAdvBookingMap[roomTypeId];
      if (minAdvBookings.size === 1) {
        this.state.minAdvBookingForm.minAdvBookingMap[roomTypeId] = [
          ...minAdvBookings,
        ][0];
      } else {
        this.state.minAdvBookingForm.minAdvBookingMap[roomTypeId] = "";
      }
    }

    this.state.minAdvBookingForm.isVisible = true;
  }
  changeMaxAdvBookingValue() {
    const roomTypeMaxAdvBookingMap = {};
    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const key = `${year}-${month}-${day}-${roomTypeId}`;
      const maxAdvBooking = this.state.maxAdvBookingMap[key];
      if (!roomTypeMaxAdvBookingMap[roomTypeId]) {
        roomTypeMaxAdvBookingMap[roomTypeId] = new Set();
      }
      if (maxAdvBooking) {
        roomTypeMaxAdvBookingMap[roomTypeId].add(maxAdvBooking);
      }
    });

    this.state.maxAdvBookingForm.maxAdvBookingMap = {};
    for (const roomTypeId in roomTypeMaxAdvBookingMap) {
      const maxAdvBookings = roomTypeMaxAdvBookingMap[roomTypeId];
      if (maxAdvBookings.size === 1) {
        this.state.maxAdvBookingForm.maxAdvBookingMap[roomTypeId] = [
          ...maxAdvBookings,
        ][0];
      } else {
        this.state.maxAdvBookingForm.maxAdvBookingMap[roomTypeId] = "";
      }
    }

    this.state.maxAdvBookingForm.isVisible = true;
  }
  changeMinLosArrivalValue() {
    const roomTypeMinlosArrivalMap = {};
    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const key = `${year}-${month}-${day}-${roomTypeId}`;
      const minlosArrival = this.state.minlosArrivalMap[key];
      if (!roomTypeMinlosArrivalMap[roomTypeId]) {
        roomTypeMinlosArrivalMap[roomTypeId] = new Set();
      }
      if (minlosArrival) {
        roomTypeMinlosArrivalMap[roomTypeId].add(minlosArrival);
      }
    });

    this.state.minlosArrivalForm.minlosArrivalMap = {};
    for (const roomTypeId in roomTypeMinlosArrivalMap) {
      const minlosArrivales = roomTypeMinlosArrivalMap[roomTypeId];
      if (minlosArrivales.size === 1) {
        this.state.minlosArrivalForm.minlosArrivalMap[roomTypeId] = [
          ...minlosArrivales,
        ][0];
      } else {
        this.state.minlosArrivalForm.minlosArrivalMap[roomTypeId] = "";
      }
    }

    this.state.minlosArrivalForm.isVisible = true;
  }
  changeMaxLosArrivalValue() {
    const roomTypeMaxlosArrivalMap = {};
    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const key = `${year}-${month}-${day}-${roomTypeId}`;
      const maxlosArrival = this.state.maxlosArrivalMap[key];
      if (!roomTypeMaxlosArrivalMap[roomTypeId]) {
        roomTypeMaxlosArrivalMap[roomTypeId] = new Set();
      }
      if (maxlosArrival) {
        roomTypeMaxlosArrivalMap[roomTypeId].add(maxlosArrival);
      }
    });

    this.state.maxlosArrivalForm.maxlosArrivalMap = {};
    for (const roomTypeId in roomTypeMaxlosArrivalMap) {
      const maxlosArrivales = roomTypeMaxlosArrivalMap[roomTypeId];
      if (maxlosArrivales.size === 1) {
        this.state.maxlosArrivalForm.maxlosArrivalMap[roomTypeId] = [
          ...maxlosArrivales,
        ][0];
      } else {
        this.state.maxlosArrivalForm.maxlosArrivalMap[roomTypeId] = "";
      }
    }

    this.state.maxlosArrivalForm.isVisible = true;
  }
  changePaymentValue() {
    const roomTypePaymentMap = {};
    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const key = `${year}-${month}-${day}-${roomTypeId}`;
      const payment = this.state.paymentMap.find((payment) => payment.key === key);

      if (!roomTypePaymentMap[roomTypeId]) {
        roomTypePaymentMap[roomTypeId] = new Set();
      }
      if (payment) {
        roomTypePaymentMap[roomTypeId].add(payment);
      }
    });

    this.state.paymentForm.paymentMap = {};

    for (const roomTypeId in roomTypePaymentMap) {
      const payments = roomTypePaymentMap[roomTypeId];
      this.state.checkedMethods[roomTypeId] = [];

      if (payments.size > 0) {
        payments.forEach((payment) => {
          payment.data.forEach((data) => {
            if (data && !this.state.checkedMethods[roomTypeId].includes(data.name)) {
              this.state.checkedMethods[roomTypeId].push(data.name);
            }
          });
        });
        this.state.paymentForm.paymentMap[roomTypeId] = [...payments];
      } else {
        this.state.paymentForm.paymentMap[roomTypeId] = "";
      }
    }

    this.state.paymentForm.isVisible = true;
  }
  changeCheckTimeValue() {
    this.state.timeCheckedMethods = [];
    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const key = `${year}-${month}-${day}`;
      for (const roomTypeId in this.state.checkMap) {
        const checkTimes = this.state.checkMap[roomTypeId];
        if (
          checkTimes.checkin_checkout.length > 0 &&
          checkTimes.relevant_date === key
        ) {
          this.state.timeCheckedMethods = checkTimes.checkin_checkout[0].name;
        }
      }
    });

    //   this.state.checkForm.checkMap = {};

    // for (const roomTypeId in this.state.checkMap) {
    //   const checkTimes = this.state.checkMap[roomTypeId];
    //   this.state.timeCheckedMethods = [];
    //   if (checkTimes.checkin_checkout.length > 0) {
    //     this.state.timeCheckedMethods.push(checkTimes.checkin_checkout[0]);
    //   }
    // }
    this.state.checkForm.isVisible = true;
  }
  changeMaxLosValue() {
    const roomTypeMaxlosMap = {};
    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const key = `${year}-${month}-${day}-${roomTypeId}`;
      const maxlos = this.state.maxlosMap[key];
      if (!roomTypeMaxlosMap[roomTypeId]) {
        roomTypeMaxlosMap[roomTypeId] = new Set();
      }
      if (maxlos) {
        roomTypeMaxlosMap[roomTypeId].add(maxlos);
      }
    });

    this.state.maxlosForm.maxlosMap = {};
    for (const roomTypeId in roomTypeMaxlosMap) {
      const maxloses = roomTypeMaxlosMap[roomTypeId];
      if (maxloses.size === 1) {
        this.state.maxlosForm.maxlosMap[roomTypeId] = [...maxloses][0];
      } else {
        this.state.maxlosForm.maxlosMap[roomTypeId] = "";
      }
    }

    this.state.maxlosForm.isVisible = true;
  }
  // Done
  changePriceValue() {
    const roomTypePriceMap = {};

    // Loop through all selected cells
    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const key = `${year}-${month}-${day}-${roomTypeId}`;
      if (!roomTypePriceMap[roomTypeId]) {
        roomTypePriceMap[roomTypeId] = {};
      }

      const roomType = this.state.roomtypes.find((rt) => rt.id == roomTypeId);
      if (roomType) {
        // Add guest_ids first
        roomType.guest_ids.forEach((guest) => {
          const guestKey = `${key}-guest-${guest.id}`;
          const price = this.state.priceMap[guestKey] || 0;
          if (!roomTypePriceMap[roomTypeId][`guest-${guest.id}`]) {
            roomTypePriceMap[roomTypeId][`guest-${guest.id}`] = {
              id: guest.id,
              name: guest.name,
              price: price,
            };
          }
        });

        // Add child_aged_from second
        roomType.child_aged_from.forEach((child) => {
          const childKey = `${key}-child-${child.id}`;
          const price = this.state.priceMap[childKey] || 0;
          if (!roomTypePriceMap[roomTypeId][`child-${child.id}`]) {
            roomTypePriceMap[roomTypeId][`child-${child.id}`] = {
              id: child.id,
              name: child.name,
              price: price,
            };
          }
        });
      }
    });

    this.state.priceForm.priceMap = roomTypePriceMap;
    this.state.priceForm.isVisible = true;
  }
  changeStayValue() {
    const roomTypeStayMap = {};

    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const key = `${year}-${month}-${day}-${roomTypeId}`;
      if (!roomTypeStayMap[roomTypeId]) {
        roomTypeStayMap[roomTypeId] = {};
      }

      const roomType = this.state.roomtypes.find((rt) => rt.id == roomTypeId);
      if (roomType) {
        roomType.guest_ids.forEach((guest) => {
          const guestKey = `guest-${guest.id}`;
          const status = this.state.stayMap[`${key}-guest-${guest.id}`] || ""; // Default to empty string
          if (!roomTypeStayMap[roomTypeId][guestKey]) {
            roomTypeStayMap[roomTypeId][guestKey] = {
              id: guest.id,
              name: guest.name,
              status: status,
            };
          }
        });

        roomType.child_aged_from.forEach((child) => {
          const childKey = `child-${child.id}`;
          const status = this.state.stayMap[`${key}-child-${child.id}`] || ""; // Default to empty string
          if (!roomTypeStayMap[roomTypeId][childKey]) {
            roomTypeStayMap[roomTypeId][childKey] = {
              id: child.id,
              name: child.name,
              status: status,
            };
          }
        });
      }
    });

    this.state.stayForm.stayMap = roomTypeStayMap;
    this.state.stayForm.isVisible = true;
  }

  changeFullLosValue() {
    const roomTypeFullLosMap = {};
    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const key = `${year}-${month}-${day}-${roomTypeId}`;
      const fullLos = this.state.fullLosMap[key];
      if (!roomTypeFullLosMap[roomTypeId]) {
        roomTypeFullLosMap[roomTypeId] = new Set();
      }
      if (fullLos) {
        roomTypeFullLosMap[roomTypeId].add(fullLos);
      }
    });

    this.state.fullLosForm.fullLosMap = {};
    for (const roomTypeId in roomTypeFullLosMap) {
      const statuses = roomTypeFullLosMap[roomTypeId];
      if (statuses.size === 1) {
        this.state.fullLosForm.fullLosMap[roomTypeId] = [...statuses][0];
      } else {
        this.state.fullLosForm.fullLosMap[roomTypeId] = "";
      }
    }

    this.state.fullLosForm.isVisible = true;
  }

  updateStayStatus(event) {
    const select = event.target;
    const status = select.value;
    const roomTypeId = select.getAttribute("data-room-type-id");
    const guestOrChildKey = select.getAttribute("data-guest-or-child-key");

    if (roomTypeId && guestOrChildKey) {
      this.state.stayForm.stayMap[roomTypeId][guestOrChildKey].status = status;
    }
  }

  limitInputValue(event) {
    const input = event.target;
    const maxValue = 100000000;

    if (parseInt(input.value) > maxValue) {
      input.value = maxValue;
    }

    const guestOrChildKey = input.getAttribute("data-guest-or-child-key");
    const roomTypeId = Object.keys(this.state.priceForm.priceMap).find((roomTypeId) =>
      Object.keys(this.state.priceForm.priceMap[roomTypeId]).includes(guestOrChildKey)
    );

    if (roomTypeId) {
      this.state.priceForm.priceMap[roomTypeId][guestOrChildKey].price = parseInt(
        input.value
      );
    }
  }

  limitAndFormatInputValue(event) {
    const input = event.target;
    const maxValue = 100000000;
    let value = parseInt(input.value.replace(/[\s\u00A0,]/g, ""));

    if (isNaN(value) || value <= 0) {
      value = "";
    } else if (value > maxValue) {
      value = maxValue;
    }

    input.value = value ? value.toLocaleString() : "";

    const roomTypeId = input.getAttribute("data-room-type-id");
    const guestOrChildKey = input.getAttribute("data-guest-or-child-key");

    if (roomTypeId && guestOrChildKey) {
      this.state.priceForm.priceMap[roomTypeId][guestOrChildKey].price = value
        ? value
        : 0;
    }
  }

  updateStayValue(event) {
    const select = event.target;
    const status = select.value;
    const roomTypeId = select.getAttribute("data-room-type-id");
    const guestOrChildKey = select.getAttribute("data-guest-or-child-key");

    if (roomTypeId && guestOrChildKey) {
      this.state.stayForm.stayMap[roomTypeId][guestOrChildKey].status = status;
    }
  }

  async savePrice(event) {
    event.preventDefault();
    const priceUpdates = [];

    // Loop through all selected cells
    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const date = `${year}-${month}-${day}`;
      const prices = this.state.priceForm.priceMap[roomTypeId];

      for (const guestOrChildKey in prices) {
        const guestOrChild = prices[guestOrChildKey];
        if (guestOrChild.price > 0) {
          // Check if the price is greater than 0
          const priceUpdate = {
            relevant_date: date,
            room_type_id: parseInt(roomTypeId),
            price: guestOrChild.price,
            rate_plan_id: this.state.form.ratePlanId,
          };

          if (guestOrChildKey.startsWith("guest")) {
            priceUpdate.guest_id = parseInt(guestOrChild.id);
          } else {
            priceUpdate.child_age_range = parseInt(guestOrChild.id);
          }

          priceUpdates.push(priceUpdate);
        }
      }
    });

    this.state.priceForm.isVisible = false;
    this.state.loading = true;
    for (const update of priceUpdates) {
      await this.orm.call("rate_plan.price", "create", [update]);
    }
    this.state.loading = false;
    this.state.selectedCells.clear();
    await this.fetchRatePlanFields();
  }

  async saveStay(event) {
    event.preventDefault();
    const stayUpdates = [];

    this.state.selectedCells.forEach((cellKey) => {
      const [year, month, day, roomTypeId] = cellKey.split("-");
      const date = `${year}-${month}-${day}`;
      const stays = this.state.stayForm.stayMap[roomTypeId];

      for (const guestOrChildKey in stays) {
        const guestOrChild = stays[guestOrChildKey];
        if (guestOrChild.status) {
          // Only save if status is not empty
          const stayUpdate = {
            relevant_date: date,
            room_type_id: parseInt(roomTypeId),
            status: guestOrChild.status,
            rate_plan_id: this.state.form.ratePlanId,
          };

          if (guestOrChildKey.startsWith("guest")) {
            stayUpdate.guest_id = parseInt(guestOrChild.id);
          } else {
            stayUpdate.child_age_range = parseInt(guestOrChild.id);
          }

          stayUpdates.push(stayUpdate);
        }
      }
    });

    this.state.stayForm.isVisible = false;
    this.state.loading = true;
    try {
      for (const update of stayUpdates) {
        await this.orm.call("rate_plan.stay_controls", "create", [update]);
      }
    } catch (error) {
      console.error("Error saving stay updates:", error);
    }
    this.state.loading = false;
    this.state.selectedCells.clear();
    await this.fetchRatePlanFields();
  }

  async fetchRatePlanFields() {
    try {
      const ratePlanFields = await this.orm.call("rate.plan", "get_all_fields", [
        this.state.form.ratePlanId,
      ]);
      this.state.ratePlanFields = ratePlanFields;
      this.state.roomtypes = ratePlanFields.room_types;
      this.state.roomtypes.forEach((roomType) => {
        roomType.guest_ids = roomType.guest_ids || [];
        roomType.child_aged_from = roomType.child_aged_from || [];
      });
      this.state.timeData = ratePlanFields.filter_checkincheckout;
      this.updateStatusMap(ratePlanFields.filter_closed);
      this.updateCtaMap(ratePlanFields.filter_cta);
      this.updateCtdMap(ratePlanFields.filter_ctd);
      this.updateMinlosMap(ratePlanFields.filter_minlos);
      this.updateMinAdvBookingMap(ratePlanFields.filter_minadvbooking);
      this.updateMaxAdvBookingMap(ratePlanFields.filter_maxadvbooking);
      this.updateMinlosArrivalMap(ratePlanFields.filter_minlosarrival);
      this.updateMaxlosArrivalMap(ratePlanFields.filter_maxlosarrival);
      this.updateMaxlosMap(ratePlanFields.filter_maxlos);
      this.updatePriceMap(ratePlanFields.filter_price);
      this.updateStayMap(ratePlanFields.filter_stay_controls);
      this.updateFullLosMap(ratePlanFields.filter_fullparentlos);
      this.updatePaymentMap(ratePlanFields.filter_paymentmethods);
      this.updateCheckMap(ratePlanFields.filter_checkincheckout);
    } catch (error) {
      console.error("Error fetching rate plan fields:", error);
    }
  }

  updateStatusMap(closedData = []) {
    if (!closedData || !Array.isArray(closedData)) {
      console.error("No valid closed data available");
      return;
    }

    const statusMap = {};
    closedData.forEach((data) => {
      if (
        data.relevant_date &&
        data.room_type_id &&
        Array.isArray(data.room_type_id) &&
        data.room_type_id.length > 0
      ) {
        const key = `${new Date(data.relevant_date).toISOString().split("T")[0]}-${
          data.room_type_id[0]
        }`;
        statusMap[key] = data.status;
      } else {
        console.error("Invalid closed data:", data);
      }
    });
    this.state.statusMap = statusMap;
  }
  updateCtaMap(ctaData = []) {
    if (!ctaData || !Array.isArray(ctaData)) {
      console.error("No valid closed data available");
      return;
    }

    const ctaMap = {};
    ctaData.forEach((data) => {
      if (
        data.relevant_date &&
        data.room_type_id &&
        Array.isArray(data.room_type_id) &&
        data.room_type_id.length > 0
      ) {
        const key = `${new Date(data.relevant_date).toISOString().split("T")[0]}-${
          data.room_type_id[0]
        }`;
        ctaMap[key] = data.status;
      } else {
        console.error("Invalid closed data:", data);
      }
    });
    this.state.ctaMap = ctaMap;
  }
  updateCtdMap(ctdData = []) {
    if (!ctdData || !Array.isArray(ctdData)) {
      console.error("No valid closed data available");
      return;
    }

    const ctdMap = {};
    ctdData.forEach((data) => {
      if (
        data.relevant_date &&
        data.room_type_id &&
        Array.isArray(data.room_type_id) &&
        data.room_type_id.length > 0
      ) {
        const key = `${new Date(data.relevant_date).toISOString().split("T")[0]}-${
          data.room_type_id[0]
        }`;
        ctdMap[key] = data.status;
      } else {
        console.error("Invalid closed data:", data);
      }
    });
    this.state.ctdMap = ctdMap;
  }
  updateMinlosMap(minlosData = []) {
    if (!minlosData || !Array.isArray(minlosData)) {
      console.error("No valid minlos data available");
      return;
    }

    const minlosMap = {};
    minlosData.forEach((data) => {
      if (
        data.relevant_date &&
        data.room_type_id &&
        Array.isArray(data.room_type_id) &&
        data.room_type_id.length > 0
      ) {
        const key = `${new Date(data.relevant_date).toISOString().split("T")[0]}-${
          data.room_type_id[0]
        }`;
        minlosMap[key] = data.number;
      } else {
        console.error("Invalid minlos data:", data);
      }
    });
    this.state.minlosMap = minlosMap;
  }
  updateMinAdvBookingMap(minAdvBookingData = []) {
    if (!minAdvBookingData || !Array.isArray(minAdvBookingData)) {
      console.error("No valid minlos data available");
      return;
    }

    const minAdvBookingMap = {};
    minAdvBookingData.forEach((data) => {
      if (
        data.relevant_date &&
        data.room_type_id &&
        Array.isArray(data.room_type_id) &&
        data.room_type_id.length > 0
      ) {
        const key = `${new Date(data.relevant_date).toISOString().split("T")[0]}-${
          data.room_type_id[0]
        }`;
        minAdvBookingMap[key] = data.number;
      } else {
        console.error("Invalid minlos data:", data);
      }
    });
    this.state.minAdvBookingMap = minAdvBookingMap;
  }
  updateMaxAdvBookingMap(maxAdvBookingData = []) {
    if (!maxAdvBookingData || !Array.isArray(maxAdvBookingData)) {
      console.error("No valid minlos data available");
      return;
    }

    const maxAdvBookingMap = {};
    maxAdvBookingData.forEach((data) => {
      if (
        data.relevant_date &&
        data.room_type_id &&
        Array.isArray(data.room_type_id) &&
        data.room_type_id.length > 0
      ) {
        const key = `${new Date(data.relevant_date).toISOString().split("T")[0]}-${
          data.room_type_id[0]
        }`;
        maxAdvBookingMap[key] = data.number;
      } else {
        console.error("Invalid minlos data:", data);
      }
    });
    this.state.maxAdvBookingMap = maxAdvBookingMap;
  }
  updateMinlosArrivalMap(minlosArrivalData = []) {
    if (!minlosArrivalData || !Array.isArray(minlosArrivalData)) {
      console.error("No valid minlos data available");
      return;
    }

    const minlosArrivalMap = {};
    minlosArrivalData.forEach((data) => {
      if (
        data.relevant_date &&
        data.room_type_id &&
        Array.isArray(data.room_type_id) &&
        data.room_type_id.length > 0
      ) {
        const key = `${new Date(data.relevant_date).toISOString().split("T")[0]}-${
          data.room_type_id[0]
        }`;
        minlosArrivalMap[key] = data.number;
      } else {
        console.error("Invalid minlos data:", data);
      }
    });
    this.state.minlosArrivalMap = minlosArrivalMap;
  }
  updateMaxlosArrivalMap(maxlosArrivalData = []) {
    if (!maxlosArrivalData || !Array.isArray(maxlosArrivalData)) {
      console.error("No valid minlos data available");
      return;
    }

    const maxlosArrivalMap = {};
    maxlosArrivalData.forEach((data) => {
      if (
        data.relevant_date &&
        data.room_type_id &&
        Array.isArray(data.room_type_id) &&
        data.room_type_id.length > 0
      ) {
        const key = `${new Date(data.relevant_date).toISOString().split("T")[0]}-${
          data.room_type_id[0]
        }`;
        maxlosArrivalMap[key] = data.number;
      } else {
        console.error("Invalid minlos data:", data);
      }
    });
    this.state.maxlosArrivalMap = maxlosArrivalMap;
  }
  updateMaxlosMap(maxlosData = []) {
    if (!maxlosData || !Array.isArray(maxlosData)) {
      console.error("No valid minlos data available");
      return;
    }

    const maxlosMap = {};
    maxlosData.forEach((data) => {
      if (
        data.relevant_date &&
        data.room_type_id &&
        Array.isArray(data.room_type_id) &&
        data.room_type_id.length > 0
      ) {
        const key = `${new Date(data.relevant_date).toISOString().split("T")[0]}-${
          data.room_type_id[0]
        }`;
        maxlosMap[key] = data.number;
      } else {
        console.error("Invalid minlos data:", data);
      }
    });
    this.state.maxlosMap = maxlosMap;
  }

  updatePriceMap(priceData = []) {
    if (!priceData || !Array.isArray(priceData)) {
      console.error("No valid price data available");
      return;
    }

    const priceMap = {};
    priceData.forEach((data) => {
      if (
        data.relevant_date &&
        data.room_type_id &&
        Array.isArray(data.room_type_id) &&
        data.room_type_id.length > 0 &&
        (data.guest_id || data.child_age_range)
      ) {
        const idType = data.guest_id ? "guest" : "child";
        const id = data.guest_id ? data.guest_id[0] : data.child_age_range[0];
        const key = `${new Date(data.relevant_date).toISOString().split("T")[0]}-${
          data.room_type_id[0]
        }-${idType}-${id}`;
        priceMap[key] = data.price;
      } else {
        console.error("Invalid price data:", data);
      }
    });
    this.state.priceMap = priceMap;
  }

  updateStayMap(stayData = []) {
    if (!stayData || !Array.isArray(stayData)) {
      console.error("No valid price data available");
      return;
    }

    const stayMap = {};
    stayData.forEach((data) => {
      if (
        data.relevant_date &&
        data.room_type_id &&
        Array.isArray(data.room_type_id) &&
        data.room_type_id.length > 0 &&
        (data.guest_id || data.child_age_range)
      ) {
        const idType = data.guest_id ? "guest" : "child";
        const id = data.guest_id ? data.guest_id[0] : data.child_age_range[0];
        const key = `${new Date(data.relevant_date).toISOString().split("T")[0]}-${
          data.room_type_id[0]
        }-${idType}-${id}`;
        stayMap[key] = data.status;
      } else {
        console.error("Invalid status:", data);
      }
    });
    this.state.stayMap = stayMap;
  }

  updateFullLosMap(fullLosData = []) {
    if (!fullLosData || !Array.isArray(fullLosData)) {
      console.error("No valid closed data available");
      return;
    }

    const fullLosMap = {};
    fullLosData.forEach((data) => {
      if (
        data.relevant_date &&
        data.room_type_id &&
        Array.isArray(data.room_type_id) &&
        data.room_type_id.length > 0
      ) {
        const key = `${new Date(data.relevant_date).toISOString().split("T")[0]}-${
          data.room_type_id[0]
        }`;
        fullLosMap[key] = data.long_of_stay;
      } else {
        console.error("Invalid closed data:", data);
      }
    });
    this.state.fullLosMap = fullLosMap;
  }
  updatePaymentMap(paymentData = []) {
    if (!paymentData || !Array.isArray(paymentData)) {
      console.error("No valid payment data available");
      return;
    }

    const paymentMap = [];

    paymentData.forEach((data) => {
      if (
        data.payment_methods &&
        data.room_type_id &&
        Array.isArray(data.room_type_id) &&
        data.room_type_id.length > 0
      ) {
        const key = `${new Date(data.relevant_date).toISOString().split("T")[0]}-${
          data.room_type_id[0]
        }`;
        paymentMap.push({
          key: key,
          data: data.payment_methods,
        });
      } else {
        console.error("Invalid payment data:", data);
      }
    });

    this.state.paymentMap = paymentMap;
  }
  updateCheckMap(checkData = []) {
    if (!checkData || !Array.isArray(checkData)) {
      console.error("No valid payment data available");
      return;
    }

    // const checkMap = [];
    // checkData.forEach((data) => {
    //   if (data.checkin_checkout) {
    //     checkMap.push(data);
    //   } else {
    //     console.error("Invalid payment data:", data);
    //   }
    // });
    this.state.checkMap = checkData;
  }

  getPrice(guestOrChildId, filterPrices, type, date, roomTypeId) {
    const dateStr = date.toLocaleDateString("en-CA"); // Format date to 'YYYY-MM-DD' in local time
    for (let filter of filterPrices) {
      if (
        (type === "guest" &&
          filter.guest_id[0] === guestOrChildId &&
          filter.relevant_date === dateStr &&
          filter.room_type_id[0] === roomTypeId) ||
        (type === "child" &&
          filter.child_age_range[0] === guestOrChildId &&
          filter.relevant_date === dateStr &&
          filter.room_type_id[0] === roomTypeId)
      ) {
        return filter.price;
      }
    }
    return "-";
  }
  getStay(guestOrChildId, filterStays, type, date, roomTypeId) {
    const dateStr = date.toLocaleDateString("en-CA"); // Format date to 'YYYY-MM-DD' in local time
    for (let filter of filterStays) {
      if (
        (type === "guest" &&
          filter.guest_id[0] === guestOrChildId &&
          filter.relevant_date === dateStr &&
          filter.room_type_id[0] === roomTypeId) ||
        (type === "child" &&
          filter.child_age_range[0] === guestOrChildId &&
          filter.relevant_date === dateStr &&
          filter.room_type_id[0] === roomTypeId)
      ) {
        return filter.status;
      }
    }
    return "-";
  }

  getStayHtml(guestOrChildId, filterStays, type, date, roomTypeId) {
    const dateStr = date.toLocaleDateString("en-CA"); // Format date to 'YYYY-MM-DD' in local time
    for (let filter of filterStays) {
      if (
        (type === "guest" &&
          filter.guest_id[0] === guestOrChildId &&
          filter.relevant_date === dateStr &&
          filter.room_type_id[0] === roomTypeId) ||
        (type === "child" &&
          filter.child_age_range[0] === guestOrChildId &&
          filter.relevant_date === dateStr &&
          filter.room_type_id[0] === roomTypeId)
      ) {
        if (filter.status === "open") {
          return '<i class="fa fa-check"></i>'; // Open icon
        } else if (filter.status === "close") {
          return '<i class="fa fa-times"></i>'; // Close icon
        }
      }
    }
    return "-";
  }

  getGuestOrChildPrice(guestOrChildId, filterPrices, type) {
    for (let filter of filterPrices) {
      if (type === "guest" && filter.guest_id[0] === guestOrChildId) {
        return filter.price;
      } else if (type === "child" && filter.child_age_range[0] === guestOrChildId) {
        return filter.price;
      }
    }
    return "-";
  }

  generateCalendarRoom(year, month) {
    const startDate = new Date(year, month, 1);
    const endDate = new Date(year, month + 1, 0);

    const currentDate = new Date(startDate.getTime());
    const days = [];

    while (currentDate <= endDate) {
      days.push({
        date: new Date(currentDate),
        formattedDate: `${currentDate.getFullYear()}-${String(
          currentDate.getMonth() + 1
        ).padStart(2, "0")}-${String(currentDate.getDate()).padStart(2, "0")}`,
        data: {},
      });
      currentDate.setDate(currentDate.getDate() + 1);
    }
    return days;
  }
  generateCalendar(year) {
    const days = [];
    let maxWeeks = 0;
    const lastDate = new Date(year, 11, 31);

    for (let month = 0; month < 12; month++) {
      const date = new Date(year, month, 1);
      const startDay = (date.getDay() + 6) % 7; // Adjust for Monday start (0 = Monday)
      const daysInMonth = new Date(year, month + 1, 0).getDate();
      const totalDays = startDay + daysInMonth;
      const weeksInMonth = Math.ceil(totalDays / 7);
      maxWeeks = Math.max(maxWeeks, weeksInMonth);

      // Fill in empty cells before the first day of the month
      for (let i = 0; i < startDay; i++) {
        days.push({
          date: null,
          formattedDate: "",
        });
      }
      // Fill in actual days of the month
      while (date.getMonth() === month) {
        days.push({
          date: new Date(date),
          formattedDate: this.formatDate(date),
        });
        date.setDate(date.getDate() + 1);
      }
      // Fill in empty cells after the last day of the month to complete the week
      const endDay = days.length % 7;
      if (endDay !== 0 && date <= lastDate) {
        for (let i = endDay; i < 7; i++) {
          days.push({
            date: null,
            formattedDate: "",
          });
        }
      }
    }
    return {days, maxWeeks};
  }
  formatDate(date) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(
      2,
      "0"
    )}-${String(date.getDate()).padStart(2, "0")}`;
  }
  updateCalendar() {
    this.state.dayss = this.generateCalendarRoom(
      this.state.activeYear,
      this.state.activeMonth
    );
    this.fetchRatePlanFields();
  }
  toggleYear(event) {
    const year = event.currentTarget.getAttribute("data-year");
    const yearIndex = this.state.selectedYears.indexOf(year);

    if (year === "2024") return;

    if (yearIndex > -1) {
      this.state.selectedYears = this.state.selectedYears.filter(
        (y) => parseInt(y) < parseInt(year)
      );
    } else {
      for (let i = 2024; i <= year; i++) {
        if (!this.state.selectedYears.includes(i.toString())) {
          this.state.selectedYears.push(i.toString());
        }
      }
    }

    this.state.selectedYears.sort();
    localStorage.setItem("selectedYears", JSON.stringify(this.state.selectedYears));
    this.updateCalendar();
  }
  switchMonth(event) {
    const month = parseInt(event.currentTarget.getAttribute("data-month"));
    const year = event.currentTarget.getAttribute("data-year");
    this.state.activeMonth = month;
    this.state.activeYear = year;
    this.updateCalendar();
  }
  switchTab(event) {
    const tabName = event.currentTarget.getAttribute("data-tab");
    this.state.activeTab = tabName;
    this.unmarkCells();
  }
  toggleHidePreviousMonths() {
    this.state.hidePreviousMonths = !this.state.hidePreviousMonths;
    localStorage.setItem(
      "hidePreviousMonths",
      JSON.stringify(this.state.hidePreviousMonths)
    );
    this.updateCalendar();
  }

  openActivity(day, roomTypeId) {
    const statusKey = `${day.formattedDate}-${roomTypeId}`;
    const existingStatus = this.state.statusMap[statusKey] || "close";
    const roomType = this.state.roomtypes.find((rt) => rt.id === roomTypeId);

    if (this.action) {
      this.state.form = {
        ...this.state.form,
        roomType: roomTypeId,
        roomTypeName: roomType ? roomType.rooms : "",
        date: day.formattedDate,
        status: existingStatus,
        isVisible: true,
      };
    } else {
      console.error("Action service not available");
    }
  }
  openCtaActivity(day, roomTypeId) {
    const statusKey = `${day.formattedDate}-${roomTypeId}`;
    const existingStatus = this.state.ctaMap[statusKey] || "close";
    const roomType = this.state.roomtypes.find((rt) => rt.id === roomTypeId);

    if (this.action) {
      this.state.ctaForm = {
        ...this.state.ctaForm,
        roomType: roomTypeId,
        roomTypeName: roomType ? roomType.rooms : "",
        date: day.formattedDate,
        status: existingStatus,
        isVisible: true,
      };
    } else {
      console.error("Action service not available");
    }
  }
  openCtdActivity(day, roomTypeId) {
    const statusKey = `${day.formattedDate}-${roomTypeId}`;
    const existingStatus = this.state.ctdMap[statusKey] || "close";
    const roomType = this.state.roomtypes.find((rt) => rt.id === roomTypeId);

    if (this.action) {
      this.state.ctdForm = {
        ...this.state.ctdForm,
        roomType: roomTypeId,
        roomTypeName: roomType ? roomType.rooms : "",
        date: day.formattedDate,
        status: existingStatus,
        isVisible: true,
      };
    } else {
      console.error("Action service not available");
    }
  }
  // openMinlosActivity(day, roomTypeId) {
  //   const minlosKey = `${day.date.toISOString().split("T")[0]}-${roomTypeId}`;
  //   const existingMinlos = this.state.minlosMap[minlosKey] || 1;
  //   const roomTypeName = this.state.roomtypes.find((rt) => rt.id === roomTypeId).rooms;

  //   if (this.action) {
  //     let adjustedDate = new Date(day.date);
  //     adjustedDate.setDate(adjustedDate.getDate() + 1);
  //     this.state.minlosForm = {
  //       ...this.state.minlosForm,
  //       roomType: roomTypeId,
  //       roomTypeName: roomTypeName,
  //       date: adjustedDate.toISOString().split("T")[0],
  //       minlos: existingMinlos,
  //       isVisible: true,
  //     };
  //   } else {
  //     console.error("Action service not available");
  //   }
  // }
  openMinAdvBookingActivity(day, roomTypeId) {
    const minAdvBookingKey = `${day.date.toISOString().split("T")[0]}-${roomTypeId}`;
    const existingMinAdvBooking = this.state.minAdvBookingMap[minAdvBookingKey] || 1;
    const roomTypeName = this.state.roomtypes.find((rt) => rt.id === roomTypeId).rooms;

    if (this.action) {
      let adjustedDate = new Date(day.date);
      adjustedDate.setDate(adjustedDate.getDate() + 1);
      this.state.minAdvBookingForm = {
        ...this.state.minAdvBookingForm,
        roomType: roomTypeId,
        roomTypeName: roomTypeName,
        date: adjustedDate.toISOString().split("T")[0],
        minAdvBooking: existingMinAdvBooking,
        isVisible: true,
      };
    } else {
      console.error("Action service not available");
    }
  }
  openMaxAdvBookingActivity(day, roomTypeId) {
    const maxAdvBookingKey = `${day.date.toISOString().split("T")[0]}-${roomTypeId}`;
    const existingMaxAdvBooking = this.state.maxAdvBookingMap[maxAdvBookingKey] || 1;
    const roomTypeName = this.state.roomtypes.find((rt) => rt.id === roomTypeId).rooms;

    if (this.action) {
      let adjustedDate = new Date(day.date);
      adjustedDate.setDate(adjustedDate.getDate() + 1);
      this.state.maxAdvBookingForm = {
        ...this.state.maxAdvBookingForm,
        roomType: roomTypeId,
        roomTypeName: roomTypeName,
        date: adjustedDate.toISOString().split("T")[0],
        maxAdvBooking: existingMaxAdvBooking,
        isVisible: true,
      };
    } else {
      console.error("Action service not available");
    }
  }
  openMinlosArrivalActivity(day, roomTypeId) {
    const minlosArrivalKey = `${day.date.toISOString().split("T")[0]}-${roomTypeId}`;
    const existingMinlosArrival = this.state.minlosArrivalMap[minlosArrivalKey] || 1;
    const roomTypeName = this.state.roomtypes.find((rt) => rt.id === roomTypeId).rooms;

    if (this.action) {
      let adjustedDate = new Date(day.date);
      adjustedDate.setDate(adjustedDate.getDate() + 1);
      this.state.minlosArrivalForm = {
        ...this.state.minlosArrivalForm,
        roomType: roomTypeId,
        roomTypeName: roomTypeName,
        date: adjustedDate.toISOString().split("T")[0],
        minlosArrival: existingMinlosArrival,
        isVisible: true,
      };
    } else {
      console.error("Action service not available");
    }
  }
  openMaxlosArrivalActivity(day, roomTypeId) {
    const maxlosArrivalKey = `${day.date.toISOString().split("T")[0]}-${roomTypeId}`;
    const existingMaxlosArrival = this.state.maxlosArrivalMap[maxlosArrivalKey] || 1;
    const roomTypeName = this.state.roomtypes.find((rt) => rt.id === roomTypeId).rooms;

    if (this.action) {
      let adjustedDate = new Date(day.date);
      adjustedDate.setDate(adjustedDate.getDate() + 1);
      this.state.maxlosArrivalForm = {
        ...this.state.maxlosArrivalForm,
        roomType: roomTypeId,
        roomTypeName: roomTypeName,
        date: adjustedDate.toISOString().split("T")[0],
        maxlosArrival: existingMaxlosArrival,
        isVisible: true,
      };
    } else {
      console.error("Action service not available");
    }
  }
  openMaxlosActivity(day, roomTypeId) {
    const maxlosKey = `${day.date.toISOString().split("T")[0]}-${roomTypeId}`;
    const existingMaxlos = this.state.maxlosMap[maxlosKey] || null;
    const roomTypeName = this.state.roomtypes.find((rt) => rt.id === roomTypeId).rooms;

    if (this.action) {
      let adjustedDate = new Date(day.date);
      adjustedDate.setDate(adjustedDate.getDate() + 1);
      this.state.maxlosForm = {
        ...this.state.maxlosForm,
        roomType: roomTypeId,
        roomTypeName: roomTypeName,
        date: adjustedDate.toISOString().split("T")[0],
        maxlos: existingMaxlos,
        isVisible: true,
      };
    } else {
      console.error("Action service not available");
    }
  }
  openPriceActivity(day, roomTypeId) {
    const priceKey = `${day.date.toISOString().split("T")[0]}-${roomTypeId}`;
    const existingPrice = this.state.priceMap[priceKey] || 1;
    const roomTypeName = this.state.roomtypes.find((rt) => rt.id === roomTypeId).rooms;

    if (this.action) {
      let adjustedDate = new Date(day.date);
      adjustedDate.setDate(adjustedDate.getDate() + 1);
      this.state.priceForm = {
        ...this.state.priceForm,
        roomType: roomTypeId,
        roomTypeName: roomTypeName,
        date: adjustedDate.toISOString().split("T")[0],
        price: existingPrice,
        isVisible: true,
      };
    } else {
      console.error("Action service not available");
    }
  }

  async saveStatus(event) {
    event.preventDefault();
    const statusUpdates = [];

    this.state.selectedCells.forEach((cellKey) => {
      const date = cellKey.split("-").slice(0, 3).join("-");
      const roomTypeId = cellKey.split("-").pop();
      const selectedStatus = this.state.form.statusMap[roomTypeId];

      statusUpdates.push({
        relevant_date: date,
        room_type_id: parseInt(roomTypeId),
        status: selectedStatus,
        rate_plan_id: this.state.form.ratePlanId,
        close_id: this.state.form.closeId,
      });
    });

    this.state.form.isVisible = false;
    this.state.loading = true;
    for (const update of statusUpdates) {
      await this.orm.call("rate_plan.closed", "create", [update]);
    }
    this.state.loading = false;
    this.state.selectedCells.clear();
    await this.fetchRatePlanFields();
  }
  async saveCta(event) {
    event.preventDefault();
    const statusUpdates = [];

    this.state.selectedCells.forEach((cellKey) => {
      const date = cellKey.split("-").slice(0, 3).join("-");
      const roomTypeId = cellKey.split("-").pop();
      const selectedStatus = this.state.ctaForm.ctaMap[roomTypeId];

      statusUpdates.push({
        relevant_date: date,
        room_type_id: parseInt(roomTypeId),
        status: selectedStatus,
        rate_plan_id: this.state.ctaForm.ratePlanId,
        filter_id: this.state.ctaForm.filterId,
      });
    });

    this.state.ctaForm.isVisible = false;
    this.state.loading = true;
    for (const update of statusUpdates) {
      await this.orm.call("rate_plan.cta", "create", [update]);
    }
    this.state.loading = false;
    this.state.selectedCells.clear();
    await this.fetchRatePlanFields();
  }
  async saveCtd(event) {
    event.preventDefault();
    const statusUpdates = [];

    this.state.selectedCells.forEach((cellKey) => {
      const date = cellKey.split("-").slice(0, 3).join("-");
      const roomTypeId = cellKey.split("-").pop();
      const selectedStatus = this.state.ctdForm.ctdMap[roomTypeId];

      statusUpdates.push({
        relevant_date: date,
        room_type_id: parseInt(roomTypeId),
        status: selectedStatus,
        rate_plan_id: this.state.ctdForm.ratePlanId,
        filter_id: this.state.ctdForm.filterId,
      });
    });

    this.state.ctdForm.isVisible = false;
    this.state.loading = true;
    for (const update of statusUpdates) {
      await this.orm.call("rate_plan.rate_plan_ctd", "create", [update]);
    }
    this.state.loading = false;
    this.state.selectedCells.clear();
    await this.fetchRatePlanFields();
  }
  async saveMinlos(event) {
    event.preventDefault();
    const minlosUpdates = [];

    this.state.selectedCells.forEach((cellKey) => {
      const date = cellKey.split("-").slice(0, 3).join("-");
      const roomTypeId = cellKey.split("-").pop();
      const selectedMinlos = this.state.minlosForm.minlosMap[roomTypeId];

      minlosUpdates.push({
        relevant_date: date,
        room_type_id: parseInt(roomTypeId),
        number: selectedMinlos,
        rate_plan_id: this.state.minlosForm.ratePlanId,
        filter_id: this.state.minlosForm.filterId,
      });
    });

    this.state.minlosForm.isVisible = false;
    this.state.loading = true;
    for (const update of minlosUpdates) {
      await this.orm.call("rate_plan.min_los", "create", [update]);
    }
    this.state.loading = false;
    this.state.selectedCells.clear();
    await this.fetchRatePlanFields();
  }
  async saveMinAdvBooking(event) {
    event.preventDefault();
    const minAdvBookingUpdates = [];

    this.state.selectedCells.forEach((cellKey) => {
      const date = cellKey.split("-").slice(0, 3).join("-");
      const roomTypeId = cellKey.split("-").pop();
      const selectedMinAdvBooking =
        this.state.minAdvBookingForm.minAdvBookingMap[roomTypeId];

      minAdvBookingUpdates.push({
        relevant_date: date,
        room_type_id: parseInt(roomTypeId),
        number: selectedMinAdvBooking,
        rate_plan_id: this.state.minAdvBookingForm.ratePlanId,
        filter_id: this.state.minAdvBookingForm.filterId,
      });
    });

    this.state.minAdvBookingForm.isVisible = false;
    this.state.loading = true;
    for (const update of minAdvBookingUpdates) {
      await this.orm.call("rate_plan.min_adv_booking", "create", [update]);
    }
    this.state.loading = false;
    this.state.selectedCells.clear();
    await this.fetchRatePlanFields();
  }
  async saveMaxAdvBooking(event) {
    event.preventDefault();
    const maxAdvBookingUpdates = [];

    this.state.selectedCells.forEach((cellKey) => {
      const date = cellKey.split("-").slice(0, 3).join("-");
      const roomTypeId = cellKey.split("-").pop();
      const selectedMaxAdvBooking =
        this.state.maxAdvBookingForm.maxAdvBookingMap[roomTypeId];

      maxAdvBookingUpdates.push({
        relevant_date: date,
        room_type_id: parseInt(roomTypeId),
        number: selectedMaxAdvBooking,
        rate_plan_id: this.state.maxAdvBookingForm.ratePlanId,
        filter_id: this.state.maxAdvBookingForm.filterId,
      });
    });

    this.state.maxAdvBookingForm.isVisible = false;
    this.state.loading = true;
    for (const update of maxAdvBookingUpdates) {
      await this.orm.call("rate_plan.max_adv_booking", "create", [update]);
    }
    this.state.loading = false;
    this.state.selectedCells.clear();
    await this.fetchRatePlanFields();
  }
  async saveMinlosArrival(event) {
    event.preventDefault();
    const minlosArrivalUpdates = [];

    this.state.selectedCells.forEach((cellKey) => {
      const date = cellKey.split("-").slice(0, 3).join("-");
      const roomTypeId = cellKey.split("-").pop();
      const selectedMinlosArrival =
        this.state.minlosArrivalForm.minlosArrivalMap[roomTypeId];

      minlosArrivalUpdates.push({
        relevant_date: date,
        room_type_id: parseInt(roomTypeId),
        number: selectedMinlosArrival,
        rate_plan_id: this.state.minlosArrivalForm.ratePlanId,
        filter_id: this.state.minlosArrivalForm.filterId,
      });
    });

    this.state.minlosArrivalForm.isVisible = false;
    this.state.loading = true;
    for (const update of minlosArrivalUpdates) {
      await this.orm.call("rate_plan.min_los_arrival", "create", [update]);
    }
    this.state.loading = false;
    this.state.selectedCells.clear();
    await this.fetchRatePlanFields();
  }
  async saveMaxlosArrival(event) {
    event.preventDefault();
    const maxlosArrivalUpdates = [];

    this.state.selectedCells.forEach((cellKey) => {
      const date = cellKey.split("-").slice(0, 3).join("-");
      const roomTypeId = cellKey.split("-").pop();
      const selectedMaxlosArrival =
        this.state.maxlosArrivalForm.maxlosArrivalMap[roomTypeId];

      maxlosArrivalUpdates.push({
        relevant_date: date,
        room_type_id: parseInt(roomTypeId),
        number: selectedMaxlosArrival,
        rate_plan_id: this.state.maxlosArrivalForm.ratePlanId,
        filter_id: this.state.maxlosArrivalForm.filterId,
      });
    });

    this.state.maxlosArrivalForm.isVisible = false;
    this.state.loading = true;
    for (const update of maxlosArrivalUpdates) {
      await this.orm.call("rate_plan.max_los_arrival", "create", [update]);
    }
    this.state.loading = false;
    this.state.selectedCells.clear();
    await this.fetchRatePlanFields();
  }
  getPaymentMethods(roomTypeId) {
    if (this.state.checkedMethods[roomTypeId].length === 0) {
      return [[4, 1]];
    }

    return this.state.checkedMethods[roomTypeId].map((checkedMethod) => {
      const method = this.state.paymentMethods.find(
        (method) => method[1] === checkedMethod
      );
      return [4, method[0]];
    });
  }
  async savePayment(event) {
    event.preventDefault();
    const paymentUpdates = [];
    this.state.selectedCells.forEach((cellKey) => {
      const date = cellKey.split("-").slice(0, 3).join("-");
      const roomTypeId = cellKey.split("-").pop();
      paymentUpdates.push({
        relevant_date: date,
        room_type_id: parseInt(roomTypeId),
        payment_methods: this.getPaymentMethods(roomTypeId),
        rate_plan_id: this.state.paymentForm.ratePlanId,
        filter_id: this.state.paymentForm.filterId,
      });
    });

    this.state.paymentForm.isVisible = false;
    this.state.loading = true;
    for (const update of paymentUpdates) {
      await this.orm.call("rate_plan.payment_methods", "create", [update]);
    }
    this.state.loading = false;
    this.state.selectedCells.clear();
    await this.fetchRatePlanFields();
  }
  async saveMaxlos(event) {
    event.preventDefault();
    const maxlosUpdates = [];

    this.state.selectedCells.forEach((cellKey) => {
      const date = cellKey.split("-").slice(0, 3).join("-");
      const roomTypeId = cellKey.split("-").pop();
      const selectedMaxlos = this.state.maxlosForm.maxlosMap[roomTypeId];

      maxlosUpdates.push({
        relevant_date: date,
        room_type_id: parseInt(roomTypeId),
        number: selectedMaxlos,
        rate_plan_id: this.state.maxlosForm.ratePlanId,
        filter_id: this.state.maxlosForm.filterId,
      });
    });

    this.state.maxlosForm.isVisible = false;
    this.state.loading = true;
    for (const update of maxlosUpdates) {
      await this.orm.call("rate_plan.max_los", "create", [update]);
    }
    this.state.loading = false;
    this.state.selectedCells.clear();
    await this.fetchRatePlanFields();
  }
  async saveCheckTime(event) {
    event.preventDefault();
    if (this.state.timeCheckedMethods !== "Do not change") {
      const timeUpdates = [];
      this.state.selectedCells.forEach((cellKey) => {
        const date = cellKey.split("-").slice(0, 3).join("-");

        timeUpdates.push({
          relevant_date: date,
          checkin_checkout: this.state.timeMethods.find(
            (method) => method[1] == this.state.timeCheckedMethods
          )[0],
          rate_plan_id: this.state.checkForm.ratePlanId,
          filter_id: this.state.checkForm.filterId,
        });
      });

      this.state.checkForm.isVisible = false;
      this.state.loading = true;
      for (const update of timeUpdates) {
        await this.orm.call("rate_plan.check_in.check_out", "create", [update]);
      }
      this.state.loading = false;
      this.state.selectedCells.clear();
      await this.fetchRatePlanFields();
    } else {
      this.state.checkForm.isVisible = false;
      this.state.loading = false;
    }
  }

  discardForm() {
    this.state.form.isVisible = false;
  }

  discardCtaForm() {
    this.state.ctaForm.isVisible = false;
  }

  discardCtdForm() {
    this.state.ctdForm.isVisible = false;
  }

  discardMinlosForm() {
    this.state.minlosForm.isVisible = false;
  }
  discardMinAdvBookingForm() {
    this.state.minAdvBookingForm.isVisible = false;
  }
  discardMaxAdvBookingForm() {
    this.state.maxAdvBookingForm.isVisible = false;
  }
  discardMinlosArrivalForm() {
    this.state.minlosArrivalForm.isVisible = false;
  }
  discardMinlosArrivalForm() {
    this.state.maxlosArrivalForm.isVisible = false;
  }
  discardMaxlosForm() {
    this.state.maxlosForm.isVisible = false;
  }
  discardFulllosForm() {
    this.state.fullLosForm.isVisible = false;
  }
  discardPaymentForm() {
    this.state.paymentForm.isVisible = false;
    this.state.methodsVisible = {};
  }
  discardTimesForm() {
    this.state.checkForm.isVisible = false;
    this.state.timesVisible = false;
  }

  toggleMethod(event) {
    const roomTypeId = event.target.dataset.roomtypeid;
    const method = event.target.value;

    if (!this.state.checkedMethods[roomTypeId]) {
      this.state.checkedMethods[roomTypeId] = [];
    }

    const index = this.state.checkedMethods[roomTypeId].indexOf(method);

    if (event.target.checked && index === -1) {
      this.state.checkedMethods[roomTypeId].push(method);
    } else if (!event.target.checked && index > -1) {
      this.state.checkedMethods[roomTypeId].splice(index, 1);
    }

    this.render();
  }

  toggleMethodsVisible(roomTypeId) {
    const newMethodsVisible = {...this.state.methodsVisible};
    for (const id in newMethodsVisible) {
      if (id !== roomTypeId) {
        newMethodsVisible[id] = false;
      }
    }
    newMethodsVisible[roomTypeId] = !this.state.methodsVisible[roomTypeId];
    this.state.methodsVisible = newMethodsVisible;
    this.render();
  }

  removeCheckedMethod(event) {
    const roomTypeId = event.target.dataset.roomtypeid;
    const method = event.target.dataset.value;
    if (!this.state.checkedMethods[roomTypeId]) {
      return;
    }
    const index = this.state.checkedMethods[roomTypeId].indexOf(method);
    if (index > -1) {
      this.state.checkedMethods[roomTypeId].splice(index, 1);
    }
    this.render();
  }

  clearAll(roomTypeId) {
    if (
      this.state.checkedMethods[roomTypeId] &&
      this.state.checkedMethods[roomTypeId].length > 0
    ) {
      // Clear all checked methods if any are currently checked
      this.state.checkedMethods[roomTypeId] = [];
    } else {
      // If none are checked, check all methods
      this.state.checkedMethods[roomTypeId] = this.state.paymentMethods.map(
        (method) => method[1]
      );
      this.state.methodsVisible[roomTypeId] = false;
    }
    this.render();
  }

  closeMethodsMenu() {
    this.state.methodsVisible = {};
    this.render();
  }
  closeTimeMethods() {
    this.state.timesVisible = false;
    this.render();
  }

  isChecked(roomTypeId, method) {
    return (
      this.state.checkedMethods[roomTypeId] &&
      this.state.checkedMethods[roomTypeId].includes(method)
    );
  }

  isPastDate(date) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return date < today;
  }

  toggleTimesVisible() {
    this.state.timesVisible = !this.state.timesVisible;
  }

  toggleTimesMethod(event) {
    const selectedValue = event.target.value;
    this.state.timeCheckedMethods = selectedValue;
  }

  isTimesChecked(methodValue) {
    return this.state.timeCheckedMethods === methodValue;
  }
}

DayPilotScheduler.template = "hms_app.DayPilotScheduler";

export const dayPilotScheduler = {
  component: DayPilotScheduler,
  supportedTypes: ["char"],
};

registry.category("fields").add("daypilot_scheduler", dayPilotScheduler);
