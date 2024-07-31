from odoo import fields, models, api


class Comments(models.Model):
    _name = "comments"
    _description = "comments"
    _rec_name = "opening_note"

    # Comments on booking confirmation
    opening_note = fields.Char(string="Opening note")
    closing_note = fields.Char(string="Closing note")

    # Comments for payment methods in booking confirmation
    at_check_in = fields.Char(string='At check-in [ Prepayment "No pre-payment" ]')
    bank_card_guarantee = fields.Char(
        string='Bank card guarantee [ Prepayment "No pre-payment" ]'
    )
    bank_transfer_for_individuals = fields.Char(
        string='Bank transfer for individuals (invoice issued by hotel) [ Prepayment "100%" ]'
    )
    bank_transfer_for_legal_entities = fields.Char(
        string='Bank transfer for legal entities (invoice issued by hotel) [ Prepayment "First nights: 1" ]'
    )

    # Comments on payment methods in Exely Booking Engine
    at_check_in_description = fields.Text(
        string='At check-in [ Prepayment "No pre-payment" ] Description'
    )
    bank_card_guarantee_description = fields.Text(
        string='Bank card guarantee [ Prepayment "No pre-payment" ] Description'
    )
    bank_transfer_for_individuals_description = fields.Text(
        string='Bank transfer for individuals (invoice issued by hotel) [ Prepayment "100%" ] Description'
    )
    bank_transfer_for_legal_entities_prepayment_comment = fields.Text(
        string='Bank transfer for legal entities (invoice issued by hotel) [ Prepayment "First nights: 1" ] Prepayment comment'
    )
    description = fields.Text(string="Description")

    # Benefits for guests who join the loyalty program
    heading = fields.Text(string="Heading")
    benefits = fields.Text(string="Benefits")

    @api.model
    def create(self, vals):
        record = self.search([], limit=1)
        if record:
            record.write(vals)  # Mavjud yozuvni yangilash
            return record
        return super(Comments, self).create(vals)

    @api.model
    def default_get(self, fields):
        res = super(Comments, self).default_get(fields)
        record = self.search([], limit=1)
        if record:
            res.update(
                {
                    "opening_note": record.opening_note,
                    "closing_note": record.closing_note,
                    "at_check_in": record.at_check_in,
                    "bank_card_guarantee": record.bank_card_guarantee,
                    "bank_transfer_for_individuals": record.bank_transfer_for_individuals,
                    "bank_transfer_for_legal_entities": record.bank_transfer_for_legal_entities,
                    "at_check_in_description": record.at_check_in_description,
                    "bank_card_guarantee_description": record.bank_card_guarantee_description,
                    "bank_transfer_for_individuals_description": record.bank_transfer_for_individuals_description,
                    "bank_transfer_for_legal_entities_prepayment_comment": record.bank_transfer_for_legal_entities_prepayment_comment,
                    "description": record.description,
                    "heading": record.heading,
                    "benefits": record.benefits,
                }
            )
        return res
