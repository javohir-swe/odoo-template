/** @odoo-module **/

import {ListRenderer} from "@web/views/list/list_renderer";
import {useState, onMounted, onWillUnmount, onWillStart} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class AvailabilitySettingsRenderer extends ListRenderer {
  setup() {
    super.setup();
    this.rpc = useService("rpc");
    this.orm = useService("orm");
    this.actionService = useService("action");
    this.state = useState({
      rules: [],
      records: this.props.list.records,
      columns: this.state.columns,
      activeTab: "calendar",
      currentMonth: new Date(),
      monthName: this.getMonthNames(new Date(), 0, 0),
      calendar: this.generateCalendar(new Date()),
      weekdays: [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
      ],
      contextMenuVisible: false,
      loading: false,
      contextMenuPosition: {x: 0, y: 0},
      selectedDay: null,
      isSelecting: false,
      startCell: null,
      selectedCells: new Set(),
      initialSelectionState: new Map(),
      isModalVisible: false,
      isRulesVisible: false,
      saveSelectedRuleId: "",
      selectedRule: "Do not change",
      selectedRuleId: "",
      selectionRuleData: [],
      selectionRuleNumber: "",
    });
    this.toggleRules = this.toggleRules.bind(this);
    this.saveRule = this.saveRule.bind(this);
    onWillStart(async () => {
      try {
        let rule = await this.getRuleData();
        this.state.rules = rule;
        this.state.selectedRule = this.state.rules[0]?.name;
        this.state.saveSelectedRuleId = this.state.rules[0]?.id;
        this.state.selectedRuleId = this.state.rules[0]?.mark_on;
        this.state.selectionRuleData = this.state.rules[0]?.room_types;
        this.state.selectionRuleNumber = this.state.rules[0]?.number_of_days;
      } catch (error) {
        console.error("Error fetching rules data:", error);
      }
    });
  }

  async getRuleData() {
    try {
      this.state.loading = true;

      const res = await this.rpc("/web/dataset/call_kw", {
        model: "availability.online_sales_role",
        method: "get_all_data",
        args: [],
        kwargs: {},
      });
      return res;
    } catch (error) {
      console.error("Error fetching rule data:", error);
      throw error;
    } finally {
      this.state.loading = false;
    }
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
    return `${months[number]} ${month.getFullYear()}`;
  }

  createRule() {
    this.actionService
      .doAction(
        {
          type: "ir.actions.act_window",
          res_model: "availability.online_sales_role",
          name: "New Rule",
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

  prevMonth() {
    const newMonth = new Date(this.state.currentMonth);
    newMonth.setMonth(newMonth.getMonth() - 1);
    this.state.currentMonth = newMonth;
    this.state.monthName = this.getMonthNames(newMonth, 0, 0);
    this.state.calendar = this.generateCalendar(newMonth);
  }

  nextMonth() {
    const newMonth = new Date(this.state.currentMonth);
    newMonth.setMonth(newMonth.getMonth() + 1);
    this.state.currentMonth = newMonth;
    this.state.monthName = this.getMonthNames(newMonth, 0, 0);
    this.state.calendar = this.generateCalendar(newMonth);
  }

  setActiveTab(tab) {
    this.state.contextMenuVisible = false;
    this.unmark();
    this.state.activeTab = tab;
  }

  generateCalendar(date) {
    const firstDayOfMonth = new Date(date.getFullYear(), date.getMonth(), 1).getDay();
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
      hasCurrentMonthDay = false; // Reset for each week
      for (let j = 0; j < 7; j++) {
        if (i === 0 && j < firstDayOfMonth) {
          week[j] = {day: prevMonthDay++, type: "prev"};
        } else if (day > daysInMonth) {
          week[j] = {day: nextMonthDay++, type: "next"};
        } else {
          const currentDate = new Date(date.getFullYear(), date.getMonth(), day)
            .toISOString()
            .split("T")[0];
          week[j] = {day: day++, type: "current", date: currentDate};
          hasCurrentMonthDay = true;
        }
      }

      if (hasCurrentMonthDay || i < 5) {
        calendar.push(week);
      }
    }

    return calendar;
  }

  startSelection(event) {
    if (event.button !== 0) return; // Only proceed if left mouse button is clicked
    const cell = event.currentTarget.closest("td");
    const cellKey = cell.getAttribute("data-cell-key");

    if (this.state.selectedCells.has(cellKey)) {
      // If the cell is already selected, remove it from the selection
      this.toggleCellSelection(cell, false);
      this.applySelectionToDOM();
    } else {
      // Otherwise, start a new selection
      this.state.isSelecting = true;
      this.state.startCell = cell; // Track the starting cell
      this.state.initialSelectionState = new Set(this.state.selectedCells); // Save the initial state of selected cells
      this.toggleCellSelection(cell, true);
      document.addEventListener("mousemove", this.handleMouseOver.bind(this));
      document.addEventListener("mouseup", this.endSelection.bind(this));
      event.preventDefault(); // Prevent text selection
    }
  }

  endSelection(event) {
    if (this.state.isSelecting) {
      this.state.isSelecting = false;
      document.removeEventListener("mousemove", this.handleMouseOver.bind(this));
      document.removeEventListener("mouseup", this.endSelection.bind(this));
      if (this.state.selectedCells.size > 0) {
        this.showContextMenu(event); // Show context menu at the end of selection
      } else {
        this.state.contextMenuVisible = false;
      }
    }
  }

  showContextMenu(event) {
    if (event && event.clientX !== undefined && event.clientY !== undefined) {
      const menuWidth = 150; // Adjust the width as needed
      const menuHeight = 100; // Adjust the height as needed
      const windowWidth = window.innerWidth;
      const windowHeight = window.innerHeight;

      let x = event.clientX + 10; // Add a small offset
      let y = event.clientY + 10; // Add a small offset

      // Adjust x position to prevent overflow
      if (x + menuWidth > windowWidth) {
        x = windowWidth - menuWidth - 10;
      }

      // Adjust y position to prevent overflow
      if (y + menuHeight > windowHeight) {
        y = windowHeight - menuHeight - 10;
      }

      this.state.contextMenuPosition = {x, y};
      this.state.contextMenuVisible = true;
    }
  }

  handleMouseOver(event) {
    if (!this.state.isSelecting) return;
    const target = document.elementFromPoint(event.clientX, event.clientY);
    const cell = target.closest("td");
    if (cell && cell.tagName.toLowerCase() === "td") {
      this.state.endCell = cell; // Track the ending cell
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
    this.state.selectedCells = new Set(this.state.initialSelectionState);

    for (let rowIndex = minRowIndex; rowIndex <= maxRowIndex; rowIndex++) {
      for (let colIndex = minColIndex; colIndex <= maxColIndex; colIndex++) {
        const cell = startRow.parentElement.children[rowIndex].children[colIndex];
        this.toggleCellSelection(cell, true);
      }
    }

    // Apply the changes to the DOM
    this.applySelectionToDOM();
  }

  toggleCellSelection(cell, add = true) {
    const cellKey = cell.getAttribute("data-cell-key");
    if (this.state.selectedCells.has(cellKey)) {
      if (!add) {
        this.state.selectedCells.delete(cellKey);
        cell.classList.remove("av_selected");
      }
    } else {
      if (add) {
        this.state.selectedCells.add(cellKey);
        cell.classList.add("av_selected");
      }
    }
  }

  applySelectionToDOM() {
    document.querySelectorAll("td[data-cell-key]").forEach((cell) => {
      const cellKey = cell.getAttribute("data-cell-key");
      if (this.state.selectedCells.has(cellKey)) {
        cell.classList.add("av_selected");
      } else {
        cell.classList.remove("av_selected");
      }
    });
  }

  changeValue() {
    this.state.selectedCells.forEach((cellKey) => {
      const cell = document.querySelector(`[data-cell-key="${cellKey}"]`);
      if (cell) {
        cell.classList.add("av_selected");
      }
    });
    // this.state.selectedCells.clear();
    this.state.contextMenuVisible = false;
    this.state.isModalVisible = true;
  }

  unmark() {
    this.state.selectedCells.forEach((cellKey) => {
      const cell = document.querySelector(`[data-cell-key="${cellKey}"]`);
      if (cell) {
        cell.classList.remove("av_selected");
      }
    });
    this.state.selectedCells.clear();
    this.state.contextMenuVisible = false;
  }

  editRule(rule) {
    this.actionService
      .doAction(
        {
          type: "ir.actions.act_window",
          context: {
            create: false,
          },
          res_model: "availability.online_sales_role",
          res_id: rule.id,
          name: "Edit Rule",
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

  closeRuleMenu(e) {
    if (this.state.isRulesVisible) {
      this.state.isRulesVisible = false;
      e.stopPropagation();
    } else {
      e.stopPropagation();
    }
  }

  closeModal() {
    // this.unmark()
    if (this.state.isRulesVisible) {
      this.state.isRulesVisible = false;
    } else {
      this.state.contextMenuVisible = true;
      this.state.isModalVisible = false;
    }
  }

  showRules(e) {
    e.stopPropagation();
    this.state.isRulesVisible = !this.state.isRulesVisible;
  }

  toggleRules(e, rule) {
    if (e.target.value !== "Do not change") {
      this.state.selectedRule = rule.name;
      this.state.selectedRuleId = rule.mark_on;
      this.state.saveSelectedRuleId = rule.id;
      this.state.selectionRuleData = rule.room_types;
      this.state.selectionRuleNumber = rule.number_of_days;
    } else {
      this.state.selectedRule = rule;
      this.state.selectedRuleId = "";
      this.state.selectionRuleData = [];
      this.state.selectionRuleNumber = "";
    }
    this.state.isRulesVisible = false;
  }

  async saveRule(e) {
    e.preventDefault();
    const specification = {
      date: {},
      display_name: {},
      role_sales: {fields: {display_name: {}}},
    };
    const updatedRule = [];
    if (this.state.selectedRule !== "Do not change") {
      this.state.selectedCells.forEach((cellKey) => {
        const date = cellKey.split("-").slice(0, 3).join("-");
        updatedRule.push({
          date: date,
          role_sales: this.state.saveSelectedRuleId,
        });
      });

      for (const update of updatedRule) {
        try {
          const response = await this.orm.call(
            "availability_settings",
            "web_save",
            [[], update],
            {specification}
          );
        } catch (error) {
          console.error(`Error updating rule: ${update}`, error);
        } finally {
          this.closeModal();
          this.unmark();
          window.location.reload();
        }
      }
    } else {
      this.closeModal();
      this.unmark();
    }
  }

  fixDate(date) {
    return `${date.year}-${String(date.month).padStart(2, "0")}-${String(
      date.day
    ).padStart(2, "0")}`;
  }

  ruleDateName(date) {
    const ruleName = this.state.records.find(
      (rule) => date == this.fixDate(rule.data.date.c)
    );
    return ruleName?.data.role_sales[1] ? ruleName.data.role_sales[1] : "-";
  }
}

AvailabilitySettingsRenderer.template = "hms_app.AvailabilitySettings";
