from odoo import api, fields, models

AIRPORT = [
    ("1", "1"),
    ("2", "2"),
]
BUS_STATION = [
    ("11", "11"),
    ("22", "22"),
]
RAILWAY_STATION = [
    ("111", "111"),
    ("222", "222"),
]

OTHER = [("other", "other")]


class Transfers(models.Model):
    _name = "transfers"
    _description = "Transfers"

    status = fields.Boolean(default=True)

    type = fields.Selection(
        [
            ("airport", "Airport"),
            ("bus_station", "Bus station"),
            ("railway_station", "Railway station"),
            ("other", "Other"),
        ],
        default="airport",
        required=True,
        string="Type",
    )
    station = fields.Char(
        string="Station", compute="_compute_station", store=True
    )  # Tanlangan Selectiondan compute qilish kerak.
    airport = fields.Selection(
        [
            ("not_selected", "Not selected"),
            ("regional_airport", "Regional airport"),
            ("international_airport", "International airport"),
        ],
        required=True,
        default="not_selected",
        string="Airport",
    )
    bus_station = fields.Selection(
        [
            ("not_selected", "Not selected"),
            ("regional_bus_station", "Regional bus station"),
            ("international_bus_station", "International bus station"),
        ],
        required=True,
        default="not_selected",
        string="Bus station",
    )
    railway_station = fields.Selection(
        [
            ("not_selected", "Not selected"),
            ("regional_railway_station", "Regional railway station"),
            ("international_railway_station", "International railway station"),
        ],
        required=True,
        default="not_selected",
        string="Railway station",
    )

    invisible_airport = fields.Boolean(
        string="Invisible Airport", compute="_compute_invisibility"
    )
    invisible_bus_station = fields.Boolean(
        string="Invisible Bus Station", compute="_compute_invisibility"
    )
    invisible_railway_station = fields.Boolean(
        string="Invisible Railway Station", compute="_compute_invisibility"
    )
    invisible_other = fields.Boolean(
        string="Invisible other", compute="_compute_invisibility"
    )

    transfer_type = fields.Many2one("transfer.type", string="Transfer Type")
    station_id = fields.Many2one("station", string="Station")
    hotel_transfer_direction = fields.Selection(
        [("to_hotel", "To Hotel"), ("from_hotel", "From Hotel")],
        string="Hotel Transfer Direction",
        default="to_hotel",
    )
    type_name = fields.Char(string="Transfer Type")
    description = fields.Text(string="Description")
    transfers_type = fields.Selection(
        [("company", "Company"), ("vehicles", "Vehicles")],
        default="company",
        string="Transfer Type",
    )
    invisible_transfers_type = fields.Boolean(
        string="Invisible Transfer Type", compute="_compute_invisibility_type"
    )
    invisible_transfers_type_company = fields.Boolean(
        string="Invisible Transfer Type", compute="_compute_invisibility_type"
    )
    vehicle_ids = fields.Many2many("vehicles", string="Vehicles")
    transport_company = fields.Many2one(
        "transport.companies", string="Transport Company"
    )
    price_usd = fields.Float(string="Price USD")
    price_uzs = fields.Float(string="Price UZS")
    price_rub = fields.Float(string="Price RUB")
    vehicle_count = fields.Integer(string="Vehicle", compute="_compute_vehicle_count")

    @api.depends("transfers_type")
    def _compute_invisibility_type(self):
        for record in self:
            record.invisible_transfers_type = record.transfers_type == "company"
            record.invisible_transfers_type_company = (
                record.transfers_type == "vehicles"
            )

    @api.depends("vehicle_ids")
    def _compute_vehicle_count(self):
        for record in self:
            record.vehicle_count = int(len(record.vehicle_ids))

    @api.depends("type")
    def _compute_invisibility(self):
        for record in self:
            record.invisible_airport = record.type != "airport"
            record.invisible_bus_station = record.type != "bus_station"
            record.invisible_railway_station = record.type != "railway_station"
            record.invisible_other = record.type != "other"

    @api.onchange("type")
    def _onchange_type(self):
        self.airport = "not_selected"
        self.bus_station = "not_selected"
        self.railway_station = "not_selected"

    @api.depends("airport", "bus_station", "railway_station")
    def _compute_station(self):
        for record in self:
            if record.airport != "not_selected":
                record.station = dict(
                    self.fields_get(["airport"])["airport"]["selection"]
                )[record.airport]
            elif record.bus_station != "not_selected":
                record.station = dict(
                    self.fields_get(["bus_station"])["bus_station"]["selection"]
                )[record.bus_station]
            elif record.railway_station != "not_selected":
                record.station = dict(
                    self.fields_get(["railway_station"])["railway_station"]["selection"]
                )[record.railway_station]
            else:
                if record.type_name:
                    record.station = record.type_name
                else:
                    record.station = "not_selected"
