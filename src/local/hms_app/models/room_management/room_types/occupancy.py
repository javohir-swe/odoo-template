from odoo import models, fields, api


class AccommodationOffer(models.Model):
    _name = "accommodation_offer"
    _description = "Accommodation Offer"

    name = fields.Char(required=True)

    # @api.model
    # def create(self, vals):
    #     _logger.info("Creating a new Accommodation Offer with values: %s", vals)
    #     # custom logic before creating
    #     return super(AccommodationOffer, self).create(vals)

    # def write(self, vals):
    #     _logger.info(
    #         "Updating Accommodation Offer ID %s with values: %s", self.id, vals
    #     )
    #     # custom logic before writing
    #     return super(AccommodationOffer, self).write(vals)

    # def unlink(self):
    #     _logger.info("Deleting Accommodation Offer ID %s", self.id)
    #     # custom logic before deletion
    #     return super(AccommodationOffer, self).unlink()
