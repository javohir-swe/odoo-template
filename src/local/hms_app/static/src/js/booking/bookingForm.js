/* @odoo-module */

import {Component, useState, onMounted, onWillStart, onWillUnmount} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {standardFieldProps} from "@web/views/fields/standard_field_props";

class BookingFormView extends Component {
  static props = {
    ...standardFieldProps,
  };
  setup() {
    super.setup();
    this.rpc = useService("rpc");
    this.orm = useService("orm");
    this.actionService = useService("action");
    this.state = useState({
      records: this.props.record,
      roomsData: [],
      activeTab: "DateOfStay",
      ratePlanData: [],
      ratePlanId: 1,
      roomTypeId: 1,
      times: [],
      guests: [],
      accommodation: [],
      availableRooms: [],
      readonly: true,
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
      purpose: [
        ["tourism", "Tourism"],
        ["service", "Service"],
        ["business", "Business"],
        ["education", "Education"],
        ["medical_care", "Medical care"],
        ["work", "Work"],
        ["private", "Private"],
        ["transit", "Transit"],
        ["humanitarian", "Humanitarian"],
        ["other", "Other"],
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
      language: [
        ["uz", "Uzbek"],
        ["af", "Afrikaans"],
        ["sq", "Albanian"],
        ["am", "Amharic"],
        ["ar", "Arabic"],
        ["hy", "Armenian"],
        ["az", "Azerbaijani"],
        ["eu", "Basque"],
        ["be", "Belarusian"],
        ["bn", "Bengali"],
        ["bs", "Bosnian"],
        ["bg", "Bulgarian"],
        ["ca", "Catalan"],
        ["ceb", "Cebuano"],
        ["zh", "Chinese (Simplified)"],
        ["zh-TW", "Chinese (Traditional)"],
        ["co", "Corsican"],
        ["hr", "Croatian"],
        ["cs", "Czech"],
        ["da", "Danish"],
        ["nl", "Dutch"],
        ["en", "English"],
        ["eo", "Esperanto"],
        ["et", "Estonian"],
        ["fi", "Finnish"],
        ["fr", "French"],
        ["fy", "Frisian"],
        ["gl", "Galician"],
        ["ka", "Georgian"],
        ["de", "German"],
        ["el", "Greek"],
        ["gu", "Gujarati"],
        ["ht", "Haitian Creole"],
        ["ha", "Hausa"],
        ["haw", "Hawaiian"],
        ["he", "Hebrew"],
        ["hi", "Hindi"],
        ["hmn", "Hmong"],
        ["hu", "Hungarian"],
        ["is", "Icelandic"],
        ["ig", "Igbo"],
        ["id", "Indonesian"],
        ["ga", "Irish"],
        ["it", "Italian"],
        ["ja", "Japanese"],
        ["jw", "Javanese"],
        ["kn", "Kannada"],
        ["kk", "Kazakh"],
        ["km", "Khmer"],
        ["rw", "Kinyarwanda"],
        ["ko", "Korean"],
        ["ku", "Kurdish (Kurmanji)"],
        ["ky", "Kyrgyz"],
        ["lo", "Lao"],
        ["la", "Latin"],
        ["lv", "Latvian"],
        ["lt", "Lithuanian"],
        ["lb", "Luxembourgish"],
        ["mk", "Macedonian"],
        ["mg", "Malagasy"],
        ["ms", "Malay"],
        ["ml", "Malayalam"],
        ["mt", "Maltese"],
        ["mi", "Maori"],
        ["mr", "Marathi"],
        ["mn", "Mongolian"],
        ["my", "Myanmar (Burmese)"],
        ["ne", "Nepali"],
        ["no", "Norwegian"],
        ["ny", "Nyanja (Chichewa)"],
        ["or", "Odia (Oriya)"],
        ["ps", "Pashto"],
        ["fa", "Persian"],
        ["pl", "Polish"],
        ["pt", "Portuguese"],
        ["pa", "Punjabi"],
        ["ro", "Romanian"],
        ["ru", "Russian"],
        ["sm", "Samoan"],
        ["gd", "Scots Gaelic"],
        ["sr", "Serbian"],
        ["st", "Sesotho"],
        ["sn", "Shona"],
        ["sd", "Sindhi"],
        ["si", "Sinhala (Sinhalese)"],
        ["sk", "Slovak"],
        ["sl", "Slovenian"],
        ["so", "Somali"],
        ["es", "Spanish"],
        ["su", "Sundanese"],
        ["sw", "Swahili"],
        ["sv", "Swedish"],
        ["tl", "Tagalog (Filipino)"],
        ["tg", "Tajik"],
        ["ta", "Tamil"],
        ["tt", "Tatar"],
        ["te", "Telugu"],
        ["th", "Thai"],
        ["tr", "Turkish"],
        ["tk", "Turkmen"],
        ["uk", "Ukrainian"],
        ["ur", "Urdu"],
        ["ug", "Uyghur"],
        ["vi", "Vietnamese"],
        ["cy", "Welsh"],
        ["xh", "Xhosa"],
        ["yi", "Yiddish"],
        ["yo", "Yoruba"],
        ["zu", "Zulu"],
      ],
      country: [
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
      specification: {
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
      },
    });
    this.saveFieldData = this.saveFieldData.bind(this);
    this.saveDontMove = this.saveDontMove.bind(this);
    onMounted(() => {
      document.querySelector(".o_control_panel").classList.add("d-none");
      // this.openServices() //o'chirilmasin !!!
      this.getRelatedAccommodation(
        this.state.records.data.available_room_ids?._currentIds
      );
      this.generateTimes();
    });

    onWillStart(async () => {
      try {
        if (this.state.records.data.id > 0) {
          let accommodation = await this.getRelatedAccommodation();
          this.state.accommodation = accommodation;
        }
        let ratePlanData = await this.ratePlan();
        let roomsData = await this.getDefaultData();
        let guest = await this.getGuests();
        this.state.ratePlanData = ratePlanData;
        this.state.roomsData = roomsData;
        this.state.guests = guest;
        this.fillAvailableRooms(
          this.state.records.data.available_room_ids?._currentIds
        );
      } catch (error) {
        console.error("Error fetching necessary datas: ", error);
      } finally {
      }
    });
  }

  fillAvailableRooms(data) {
    const housekeepingIds = data.map((item) => item);
    let filteredRooms = [];

    this.state.roomsData.forEach((roomType) => {
      const roomsWithHousekeepingId = roomType.rooms.filter((room) =>
        housekeepingIds.includes(room.housekeeping_id)
      );

      if (roomsWithHousekeepingId.length > 0) {
        filteredRooms.push(...roomsWithHousekeepingId);
      }
    });

    const formattedRooms = filteredRooms.map((room) => ({
      number: room.number,
      id: room.housekeeping_id,
    }));
    this.state.availableRooms = formattedRooms;
  }

  setActiveTab(tab) {
    this.state.activeTab = tab;
  }

  generateTimes() {
    const times = [];
    for (let hour = 0; hour < 24; hour++) {
      for (let minutes = 0; minutes < 60; minutes += 30) {
        const time = `${this.padTime(hour)}:${this.padTime(minutes)}`;
        times.push(time);
      }
    }
    times.push("23:59");
    this.state.times = times;
    return times;
  }

  padTime(number) {
    return number.toString().padStart(2, "0");
  }

  recordDate(date) {
    return `${date.year}-${String(date.month).padStart(2, "0")}-${String(
      date.day
    ).padStart(2, "0")}`;
  }

  setMin() {
    let month = new Date().getMonth();
    let day = new Date().getDate();
    let year = new Date().getFullYear();
    return `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(
      2,
      "0"
    )}`;
  }

  async checkInDateChange(e) {
    e.preventDefault();

    const checkInDate = new Date(e.target.value);
    const nextDay = new Date(checkInDate);

    nextDay.setDate(nextDay.getDate() + 1);

    const nextDayStr = nextDay.toISOString().split("T")[0];
    const checkoutDateElement = document.getElementById("checkout_date");
    checkoutDateElement.min = e.target.value;
    checkoutDateElement.value = nextDayStr;

    const nightElement = document.getElementById("nights");
    nightElement.value = 1;

    let specification = this.state.specification;
    if (this.state.records.data.id > 0) {
      let bookingDetails = {
        check_in_date: e.target.value,
        check_out_date: nextDayStr,
      };

      try {
        const result = await this.orm.call(
          "booking",
          "web_save",
          [[this.state.records.data.id], bookingDetails],
          {specification}
        );
        this.state.records.data.id = result[0].id;
        this.state.records.data.unique_id = result[0].unique_id;
      } catch (error) {
        console.error("Error while creating data: ", error);
      } finally {
        this.state.availableRooms = [];
        let accommodation = await this.getRelatedAccommodation();
        this.state.accommodation = accommodation;
        // this.setActiveTab("Stay");
      }
    } else {
      this.saveFieldData("stay");
    }
  }

  async checkOutDateChange(e) {
    e.preventDefault();

    const checkinDateValue = document.getElementById("checkin_date").value;

    const checkinDate = new Date(checkinDateValue);
    const checkoutDate = new Date(e.target.value);

    const timeDifference = checkoutDate - checkinDate;

    const daysDifference = Math.ceil(timeDifference / (1000 * 3600 * 24));

    const nightElement = document.getElementById("nights");
    nightElement.value = daysDifference;

    let specification = this.state.specification;
    if (this.state.records.data.id > 0) {
      let bookingDetails = {
        check_in_date: checkinDateValue,
        check_out_date: e.target.value,
      };

      try {
        const result = await this.orm.call(
          "booking",
          "web_save",
          [[this.state.records.data.id], bookingDetails],
          {specification}
        );
        this.state.records.data.id = result[0].id;
        this.state.records.data.unique_id = result[0].unique_id;
      } catch (error) {
        console.error("Error while creating data: ", error);
      } finally {
        this.state.availableRooms = [];
        let accommodation = await this.getRelatedAccommodation();
        this.state.accommodation = accommodation;
        // this.setActiveTab("Stay");
      }
    } else {
      this.saveFieldData("stay");
    }
  }

  async adultsChange(e) {
    e.preventDefault();

    let adults = document.getElementById("adults").value;

    let specification = this.state.specification;
    if (this.state.records.data.id > 0) {
      let bookingDetails = {
        adults: +adults,
      };

      try {
        const result = await this.orm.call(
          "booking",
          "web_save",
          [[this.state.records.data.id], bookingDetails],
          {specification}
        );
        this.state.records.data.id = result[0].id;
        this.state.records.data.unique_id = result[0].unique_id;
      } catch (error) {
        console.error("Error while creating data: ", error);
      } finally {
        this.state.records.data.adults = +e.target.value;
        this.state.availableRooms = [];
        let accommodation = await this.getRelatedAccommodation();
        this.state.accommodation = accommodation;
        // this.setActiveTab("Stay");
      }
    } else {
      this.saveFieldData("stay");
    }
  }

  async childrenChange(e) {
    e.preventDefault();

    const children = document.getElementById("children").value;

    let specification = this.state.specification;
    if (this.state.records.data.id > 0) {
      let bookingDetails = {
        children: +children,
      };

      try {
        const result = await this.orm.call(
          "booking",
          "web_save",
          [[this.state.records.data.id], bookingDetails],
          {specification}
        );
        this.state.records.data.id = result[0].id;
        this.state.records.data.unique_id = result[0].unique_id;
      } catch (error) {
        console.error("Error while creating data: ", error);
      } finally {
        this.state.records.data.children = +e.target.value;
        this.state.availableRooms = [];
        let accommodation = await this.getRelatedAccommodation();
        this.state.accommodation = accommodation;
        // this.setActiveTab("Stay");
      }
    } else {
      this.saveFieldData("stay");
    }
  }

  async ratePlan() {
    try {
      const res = await this.orm.call("rate.plan", "name_search", []);
      return res;
    } catch (error) {
      console.error(error);
    } finally {
    }
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
    } finally {
    }
  }

  async getGuests() {
    try {
      const res = await this.rpc("/web/dataset/call_kw", {
        model: "guest",
        method: "name_search",
        args: [],
        kwargs: {args: [], limit: "", name: "", operator: "ilike"},
      });
      return res;
    } catch (error) {
      console.error("Error fetching rooms data by type:", error);
    } finally {
    }
  }

  async saveFieldData(action) {
    if (this.state.records.data.id > 0) {
      let accommodation = await this.getRelatedAccommodation();
      this.state.accommodation = accommodation;
      this.setActiveTab("Stay");
      let records = await this.getRecord();
      this.state.records.data.price_detail_ids = records[0].price_detail_ids;
      this.state.records.data.room_service_ids = records[0].room_service_ids;
    } else {
      let checkInDate = document.getElementById("checkin_date").value;
      let checkOutDate = document.getElementById("checkout_date").value;
      let adults = document.getElementById("adults").value;
      let children = document.getElementById("children").value;
      let bookingDetails;
      bookingDetails = {
        accommodation: false,
        adults: adults,
        agent_company_id: false,
        arrival_status: "same_day_bookings",
        check_in_date: checkInDate,
        check_in_price: 0,
        check_in_times: "14:00",
        check_out_date: checkOutDate,
        check_out_price: 0,
        check_out_times: "12:00",
        children: children,
        citizenship: false,
        customer_company_id: false,
        customer_language: false,
        departure_status: "waiting",
        deposit: 0,
        dont_move: false,
        email: false,
        first_name: false,
        gender: false,
        guarantee_method: false,
        guest_comment: false,
        guest_id: false,
        guest_status: false,
        is_front_desk_booking: false,
        js_field: false,
        last_name: false,
        market_segment: false,
        middle_name: false,
        new_payment_method: false,
        phone: false,
        point_of_sale: false,
        price_detail_ids: [],
        purpose_of_visit: false,
        rate_plan: 1,
        room_number: false,
        room_service_ids: [],
        room_type_id: false,
        send_email: false,
        staff: false,
        status: "created",
        total: 0,
      };
      let specification = this.state.specification;
      try {
        const result = await this.orm.call(
          "booking",
          "web_save",
          [
            this.state.records.data.id ? [this.state.records.data.id] : [],
            bookingDetails,
          ],
          {specification}
        );
        this.state.records.data.id = result[0].id;
        this.state.records.data.unique_id = result[0].unique_id;
        this.state.records.data.check_in_date = result[0].check_in_date;
        this.state.records.data.check_out_date = result[0].check_out_date;
      } catch (error) {
        console.error("Error while creating data: ", error);
      } finally {
        let accommodation = await this.getRelatedAccommodation();
        this.state.accommodation = accommodation;
        if (action == "go") {
          this.setActiveTab("Stay");
        }
      }
    }
  }

  async getRecord() {
    let specification = this.state.specification;
    try {
      const res = await this.orm.call(
        "booking",
        "web_read",
        [[this.state.records.data.id]],
        {specification}
      );
      return res;
    } catch (error) {
      console.error(error);
    } finally {
      this.state.loading = false;
    }
  }

  async saveOnChangedPlanData(e) {
    let specification = this.state.specification;
    this.state.ratePlanId = +e.target.value.split(",")[0];
    try {
      const result = await this.orm.call(
        "booking",
        "web_save",
        [[this.state.records.data.id], {rate_plan: +e.target.value.split(",")[0]}],
        {specification}
      );
    } catch (error) {
      console.error("Error while changing data: ", error);
    } finally {
      let accommodation = await this.getRelatedAccommodation();
      this.state.accommodation = accommodation;
      let records = await this.getRecord();
      this.state.records.data = records[0];
    }
  }
  // // don't remove this function below
  // async saveOnChangedAccommodation(e) {
  //   this.state.availableRooms = [];
  //   let specification = this.state.specification;
  //   try {
  //     const result = await this.orm.call(
  //       "booking",
  //       "onchange",
  //       [
  //         [this.state.records.data.id],
  //         {accommodation: +e.target.value},
  //         ["accommodation"],
  //         specification,
  //       ],
  //       {}
  //     );
  //     this.state.roomTypeId = this.findRoomTypeId(+e.target.value);
  //   } catch (error) {
  //     console.error("Error while changing data: ", error);
  //   } finally {
  //     this.saveAccommodation(e);
  //   }
  // }

  async saveAccommodation(e) {
    this.state.roomTypeId = this.findRoomTypeId(+e.target.value);
    let specification = this.state.specification;
    try {
      const result = await this.orm.call(
        "booking",
        "web_save",
        [
          [this.state.records.data.id],
          {accommodation: +e.target.value, room_type_id: this.state.roomTypeId},
        ],
        {specification}
      );
      this.uniqueRoom(result[0].available_room_ids);
    } catch (error) {
      console.error("Error while changing data: ", error);
    } finally {
      let records = await this.getRecord();
      this.state.records.data = records[0];
      let accData = records[0].accommodation;
      this.state.records.data.accommodation = [];
      this.state.records.data.accommodation[0] = accData.id;
      this.state.records.data.accommodation[1] = accData.display_name;
    }
  }

  async saveRoom(e) {
    let specification = this.state.specification;
    try {
      const result = await this.orm.call(
        "booking",
        "web_save",
        [[this.state.records.data.id], {room_number: +e.target.value}],
        {specification}
      );
    } catch (error) {
      console.error("Error while changing data: ", error);
    } finally {
      let records = await this.getRecord();
      let roomData = records[0].room_number;
      let accData = records[0].accommodation;
      this.state.records.data = records[0];
      this.state.records.data.accommodation = [];
      this.state.records.data.accommodation[0] = accData.id;
      this.state.records.data.accommodation[1] = accData.display_name;
      this.state.records.data.room_number = [];
      this.state.records.data.room_number[0] = roomData.id;
      this.state.records.data.room_number[1] = roomData.display_name;
    }
  }

  async saveCheckInTime(e) {
    let specification = this.state.specification;
    try {
      const result = await this.orm.call(
        "booking",
        "web_save",
        [[this.state.records.data.id], {check_in_times: e.target.value}],
        {specification}
      );
    } catch (error) {
      console.error("Error while changing data: ", error);
    } finally {
      this.state.records.data.check_in_times = e.target.value;
    }
  }

  async saveCheckOutTime(e) {
    let specification = this.state.specification;
    try {
      const result = await this.orm.call(
        "booking",
        "web_save",
        [[this.state.records.data.id], {check_out_times: e.target.value}],
        {specification}
      );
    } catch (error) {
      console.error("Error while changing data: ", error);
    } finally {
      this.state.records.data.check_out_times = e.target.value;
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
            ["booking_unique", "=", this.state.records.data.unique_id],
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

  uniqueRoom(data) {
    const roomMap = new Map();

    data.forEach((room) => {
      if (!roomMap.has(room.number)) {
        roomMap.set(room.number, room.id);
      }
    });

    const uniqueRoomNumbersWithIds = Array.from(roomMap, ([number, id]) => ({
      number,
      id,
    }));
    this.state.availableRooms = uniqueRoomNumbersWithIds;
    return uniqueRoomNumbersWithIds;
  }

  async saveDontMove(e) {
    let specification = this.state.specification;
    try {
      const result = await this.orm.call(
        "booking",
        "web_save",
        [[this.state.records.data.id], {dont_move: e.target.checked}],
        {specification}
      );
    } catch (error) {
      console.error("Error while changing data: ", error);
    } finally {
    }
  }

  async saveGuests(e) {
    if (e.target.value != "create") {
      let specification = {
        birthday: {},
        citizenships: {},
        last_name: {},
        first_name: {},
        middle_name: {},
        comment_for_guest: {},
        email_ids: {fields: {email: {}}, limit: 40, order: ""},
        full_name: {},
        sex: {},
        guest_status: {},
        phone_ids: {fields: {phone: {}}, limit: 40, order: ""},
      };
      try {
        const res = await this.rpc("/web/dataset/call_kw", {
          model: "guest",
          method: "web_read",
          args: [+e.target.value],
          kwargs: {specification},
        });
        this.fillGuestData(res);
        return res;
      } catch (error) {
        console.error("Error fetching rooms data by type:", error);
      } finally {
        this.state.records.data.guest_id = [];
        this.state.records.data.guest_id[0] = +e.target.value;
      }
    } else if (e.target.value == "create") {
      document.getElementById("last-name").value = "";
      document.getElementById("first-name").value = "";
      document.getElementById("middle-name").value = "";
      document.getElementById("guest-email").value = "";
      document.getElementById("phone").value = "";
      document.getElementById("male").checked = false;
      document.getElementById("female").checked = false;
      document.getElementById("citizenship").value = "";
      this.state.readonly = false;
    }
  }

  fillGuestData(guest) {
    this.state.records.data.last_name = guest[0].last_name;
    this.state.records.data.first_name = guest[0].first_name;
    this.state.records.data.middle_name = guest[0].middle_name;
    this.state.records.data.email = guest[0].email_ids[0]?.email;
    this.state.records.data.phone = guest[0].phone_ids[0]?.phone;
    this.state.records.data.gender = guest[0].sex;
    this.state.records.data.citizenship = guest[0].citizenships;
    document.getElementById("last-name").innerText = guest[0].last_name;
    document.getElementById("first-name").value = guest[0].first_name;
    document.getElementById("middle-name").value = guest[0].middle_name
      ? guest[0].middle_name
      : "";
    document.getElementById("guest-email").value = guest[0].email_ids[0]?.email ?? "";
    document.getElementById("phone").value = guest[0].phone_ids[0]?.phone ?? "";

    if (guest[0].sex === "male") {
      document.getElementById("male").checked = true;
    } else if (guest[0].sex === "female") {
      document.getElementById("female").checked = true;
    } else {
      document.getElementById("female").checked = false;
      document.getElementById("male").checked = false;
    }
    const citizenshipSelect = document.getElementById("citizenship");
    citizenshipSelect.value = guest[0].citizenships;
    this.state.readonly = false;
  }

  // async openServices() {
  //   try {
  //     const result = await this.orm.call(
  //       "rate_plan.extras",
  //       "get_views",
  //       [],
  //       {
  //         options: { action_id: false, load_filters: true, toolbar: false },
  //         views: [[false, 'list'], [false, 'search']]
  //       }
  //     );
  //   } catch (error) {
  //     console.error("Error while changing data: ", error);
  //   } finally {
  //     this.getServices()
  //   }
  // }

  // async getServices() {
  //   this.actionService
  //     .doAction(
  //       {
  //         type: "ir.actions.act_window",
  //         res_model: "rate_plan.extras",
  //         name: "Payment",
  //         target: "new",
  //         views: [[false, "search"], [false, "list"]],
  //       },
  //       { clearBreadcrumbs: false }
  //     )
  //     .catch((error) => {
  //       console.error(`Action does not exist or failed:`, error);
  //     });
  // }

  findRoomTypeId(id) {
    let accName = this.state.accommodation.find((acc) => acc[0] == id);
    let roomTypeId = this.state.roomsData.find((roomType) =>
      accName[1].includes(roomType.room_type)
    );
    return roomTypeId.rooms[0]?.room_type_id;
  }

  fillNights(data) {
    return data.split("|")[0];
  }
  fillServiceCnt(data) {
    return data.split("|")[0];
  }
  fillDailyRate(data) {
    return `UZS ${data.split("|")[1]}`;
  }
  fillCostStay(data) {
    return `UZS ${data.split("|")[2]}`;
  }
  fillCostServices(data) {
    return `UZS ${data.split("|")[1]}`;
  }

  async saveData(e) {
    e.preventDefault();
    let guest_id = document.getElementById("guest_id").value;
    let lastName = document.getElementById("last-name").value;
    let firstName = document.getElementById("first-name").value;
    let middleName = document.getElementById("middle-name").value;
    let guestEmail = document.getElementById("guest-email").value;
    let sendEmail = document.getElementById("email-notify").value;
    let phone = document.getElementById("phone").value;
    let citizenship = document.getElementById("citizenship").value;
    let guerantee = document.getElementById("guerantee").value;
    let pointOfSale = document.getElementById("pointOfSale").value;
    let marketSegment = document.getElementById("marketSegment").value;
    let purpose = document.getElementById("purpose").value;
    let language = document.getElementById("language").value;
    let comment = document.getElementById("comment").value;
    const checkedGender = document.querySelector('input[name="gender"]:checked');
    let specification = this.state.specification;
    let bookingDetails = {
      citizenship: citizenship,
      customer_language: language,
      email: guestEmail,
      first_name: firstName,
      gender: checkedGender?.value,
      guarantee_method: guerantee,
      guest_comment: comment,
      guest_id: guest_id == "create" ? false : +guest_id,
      is_front_desk_booking: pointOfSale,
      last_name: lastName,
      market_segment: marketSegment,
      middle_name: middleName,
      phone: phone,
      purpose_of_visit: purpose,
      send_email: sendEmail,
      status: "done",
    };

    try {
      const result = await this.orm.call(
        "booking",
        "web_save",
        [[this.state.records.data.id], bookingDetails],
        {specification}
      );
    } catch (error) {
      console.error("Error while creating data: ", error);
    } finally {
      this.actionService
        .doAction(
          {
            type: "ir.actions.act_window",
            res_model: "booking",
            name: "Booking",
            target: "current",
            views: [
              [false, "list"],
              [false, "form"],
              [false, "search"],
            ],
          },
          {clearBreadcrumbs: true}
        )
        .catch((error) => {
          console.error(`Action does not exist or failed:`, error);
          alert(`The action does not exist.`);
        });
    }
  }

  checkGuest() {
    this.setActiveTab("Guest");
    if (this.state.records.data.guest_id[0] > 0) {
      this.state.readonly = false;
      // document.getElementById("last-name").value = this.state.records.data.last_name
      // document.getElementById("first-name").value = this.state.records.data.first_name
      // document.getElementById("middle-name").value = this.state.records.data.middle_name ?? ""
      // document.getElementById("guest-email").value = this.state.records.data.email
      // document.getElementById("email-notify").value = this.state.records.data.send_email
      // document.getElementById("phone").value = this.state.records.data.phone
      // document.getElementById("citizenship").value = this.state.records.data.citizenship
      // document.getElementById("guerantee").value = this.state.records.data.guarantee_method
      // document.getElementById("pointOfSale").value = this.state.records.data.is_front_desk_booking
      // document.getElementById("marketSegment").value = this.state.records.data.market_segment ?? ""
      // document.getElementById("purpose").value = this.state.records.data.purpose_of_visit ?? ""
      // document.getElementById("language").value = this.state.records.data.customer_language ?? ""
      // document.getElementById("comment").value = this.state.records.data.guest_comment
    }
  }
}

BookingFormView.template = "hms_app.BookingForm";

export const bookingFormCustom = {
  component: BookingFormView,
  supportedTypes: ["char"],
};

registry.category("fields").add("booking_form", bookingFormCustom);
