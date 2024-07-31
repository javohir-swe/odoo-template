/** @odoo-module */

import {ListRenderer} from "@web/views/list/list_renderer";
import {useState, onWillStart, onMounted, onWillUnmount} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class HouseKeeping extends ListRenderer {
  setup() {
    super.setup();
    this.rpc = useService("rpc");
    this.orm = useService("orm");
    this.state = useState({
      defaultData: this.getDefaultData() || false,
      roomCount: null,
      status: {
        vacant: 0,
        occupied: 0,
        outOfOrder: 0,
        dirty: 0,
        clean: 0,
        inspected: 0,
        buildings: [],
        floors: [],
        roomTypes: [],
      },
      loading: false,
      columns: this.state.columns || [],
      records: this.props.list.records,
      selected_status: "All",
      selected_building: "All",
      selected_floor: "All",
      selected_roomType: "All",
      action_modal: null,
      filteredData: this.props.list.records,
      xls_modal: false,
      fixing_modal: false,
      todayDate: this.formatDate(new Date()),
      nextDayDate: this.formatDate(this.getNextDay(new Date())),
    });
    this.saveStatus = this.saveStatus.bind(this);
    this.filterData = this.filterData.bind(this);
    this.filteredData = this.filteredData.bind(this);

    onWillStart(async () => {
      this.filterData();
      try {
        this.state.loading = true;
        let defaultData = await this.getDefaultData();
        this.state.defaultData = defaultData;
        this.renderData(defaultData);
      } catch (error) {
        console.error("Error while fetching default data");
      } finally {
        this.state.loading = false;
      }
    });
    this.openModal = this.openModal.bind(this);
    this.openXLS = this.openXLS.bind(this);
  }

  formatDate(date) {
    return date.toISOString().split("T")[0];
  }

  getNextDay(date) {
    const nextDay = new Date(date);
    nextDay.setDate(date.getDate() + 1);
    return nextDay;
  }
  async getDefaultData() {
    try {
      const res = await this.rpc("/web/dataset/call_kw", {
        model: "room_inventory.housekeeping",
        method: "get_rooms_by_type",
        args: [],
        kwargs: {},
      });
      this.state.roomCount = res.reduce((acc, current) => acc + current.count, 0);
      return res;
    } catch (error) {
      console.error("Error fetching rooms data by type:", error);
    }
  }

  renderData(roomsData) {
    this.state.status.vacant = 0;
    this.state.status.occupied = 0;
    this.state.status.outOfOrder = 0;
    this.state.status.dirty = 0;
    this.state.status.clean = 0;
    this.state.status.inspected = 0;

    roomsData.map((data, index) => {
      data.rooms.map((room, i) => {
        if (room.status === "Clean") {
          this.state.status.clean += 1;
        }
        if (room.status === "Need to Clean") {
          this.state.status.dirty += 1;
        }
        if (room.status === "Checked") {
          this.state.status.inspected += 1;
        }
        if (room.status === "Out of Order") {
          this.state.status.outOfOrder += 1;
        }
      });
    });
  }

  toggleHeader() {
    const el = document.getElementById("hk-container");
    if (el) {
      el.classList.toggle("show");
    }
  }

  openModal(id) {
    const record = this.state.records.find((record) => record.data.id === id);
    if (record && record.data.status === "out_of_order") {
      return; // Do not open modal if status is out_of_order
    }

    if (this.state.action_modal === id) {
      this.state.action_modal = null;
    } else {
      this.state.action_modal = id;
    }
  }
  openXLS() {
    this.state.xls_modal = !this.state.xls_modal;
  }

  async saveStatus(status) {
    const record = this.state.records.find(
      (record) => record.data.id === this.state.action_modal
    );
    if (record && record.data.status === "out_of_order") {
      alert("Cannot change the status of a room that is out of order.");
      return;
    }

    const dateIn = document.getElementById("maintenance-dateIn").value;
    const timeIn = document.getElementById("maintenance-timeIn").value;
    const dateOut = document.getElementById("maintenance-dateOut").value;
    const timeOut = document.getElementById("maintenance-timeOut").value;

    const startDateTime = new Date(`${dateIn}T${timeIn}`);
    const endDateTime = new Date(`${dateOut}T${timeOut}`);

    // Check if endDateTime is greater than startDateTime
    if (endDateTime <= startDateTime) {
      alert(
        "The 'Unavailable for accommodation until' date must be later than the 'Unavailable for accommodation from' date."
      );
      return;
    }

    const specification = {
      display_name: "",
      number: "",
      out_of_order_ids: {
        fields: {
          works: "",
          description: "",
          unavailable_from: "",
          unavailable_until: "",
        },
        limit: 40,
      },
      status: "",
    };

    let textarea = document.getElementById("maintenance-desc").value;
    let starting = `${dateIn} ${timeIn}`;
    let ending = `${dateOut} ${timeOut}`;
    let fullPeriod = `${starting}-${ending}`;

    if (status == "out_of_order") {
      this.state.fixing_modal = true;
      const form = document.getElementById("maintenance-form");

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      let update = {
        status: "out_of_order",
        out_of_order_ids: [
          [
            0,
            "virtual_48",
            {
              description: textarea,
              unavailable_from: starting,
              unavailable_until: ending,
              works: "",
            },
          ],
        ],
      };

      try {
        const res = await this.rpc("/web/dataset/call_kw", {
          model: "room_inventory.housekeeping",
          method: "web_save",
          args: [[this.state.action_modal], update],
          kwargs: {specification},
        });
      } catch (error) {
        console.error("Error saving room data:", error);
      } finally {
        this.state.records.forEach((record) => {
          if (record.data.id == this.state.action_modal) {
            record.data.out_of_order_period = fullPeriod;
            document.getElementById("maintenance-desc").value = "";
            document.getElementById("maintenance-dateIn").value = this.state.todayDate;
            document.getElementById("maintenance-dateOut").value =
              this.state.nextDayDate;
            record.data.status = "out_of_order";
            window.location.reload();
          }
        });
        let defaultData = await this.getDefaultData();
        this.renderData(defaultData);
        this.state.action_modal = null;
        this.state.fixing_modal = false;
      }
    } else {
      try {
        const res = await this.rpc("/web/dataset/call_kw", {
          model: "room_inventory.housekeeping",
          method: "web_save",
          args: [[this.state.action_modal], {status: status}],
          kwargs: {specification},
        });
      } catch (error) {
        console.error("Error saving room data:", error);
      } finally {
        this.state.records.forEach((record) => {
          if (record.data.id == this.state.action_modal) {
            record.data.status = status;
          }
        });
        let defaultData = await this.getDefaultData();
        this.renderData(defaultData);
        this.state.action_modal = null;
      }
    }
  }

  statusChecking(status) {
    let statusCheck = "";
    let statusClass = "";
    if (status == "need_to_clean") {
      statusCheck = "Need to clean";
      statusClass = "status-need-to-clean";
    } else if (status == "out_of_order") {
      statusCheck = "Out of order";
      statusClass = "status-out-of-order";
    } else if (status == "clean") {
      statusCheck = "Clean";
      statusClass = "status-clean";
    } else if (status == "checked") {
      statusCheck = "Checked";
      statusClass = "status-checked";
    } else {
      statusCheck = status;
    }
    return {text: statusCheck, class: statusClass};
  }

  filterData() {
    const buildings = [];
    const floors = [];
    const roomTypes = [];
    this.state.records.forEach((item) => {
      if (!buildings.includes(item.data.building_id[1])) {
        buildings.push(item.data.building_id[1]);
      }
      if (!floors.includes(item.data.floor_id[1])) {
        floors.push(item.data.floor_id[1]);
      }
      if (!roomTypes.includes(item.data.room_type[1])) {
        roomTypes.push(item.data.room_type[1]);
      }
    });
    this.state.buildings = buildings;
    this.state.floors = floors;
    this.state.roomTypes = roomTypes;
  }

  filteredData() {
    const {selected_building, selected_floor, selected_roomType, selected_status} =
      this.state;
    const filteredData = this.state.records.filter((record) => {
      return (
        (selected_building === "All" ||
          record.data.building_id[1] === selected_building) &&
        (selected_floor === "All" || record.data.floor_id[1] === selected_floor) &&
        (selected_roomType === "All" ||
          record.data.room_type[1] === selected_roomType) &&
        (selected_status === "All" ||
          this.statusChecking(record.data.status).text === selected_status)
      );
    });
    this.props.list.records;
    this.state.filteredData = filteredData;
  }
}
HouseKeeping.template = "hms_app.HouseKeeping";
