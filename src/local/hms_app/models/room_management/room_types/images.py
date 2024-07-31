import mimetypes

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class RoomImage(models.Model):
    _name = "room_image"
    _description = "Room Image"

    # photo = fields.Image(required=True)
    photo = fields.Binary("Image", required=True)
    file_name = fields.Char("File Name")

    @api.constrains("photo", "file_name")
    def _check_image_format(self):
        allowed_formats = [".jpg", ".jpeg", ".png", ".gif"]
        for record in self:
            if record.file_name:
                file_type = mimetypes.guess_type(record.file_name)[0]
                extension = "." + file_type.split("/")[1] if file_type else ""
                if extension not in allowed_formats:
                    raise ValidationError(
                        f"Unsupported file format. Allowed formats are: {', '.join(allowed_formats)}"
                    )

    @api.constrains("photo")
    def _check_image_size(self):
        max_size_mb = 10  # Maximum size in megabytes
        max_size_bytes = max_size_mb * 1024 * 1024  # Convert to bytes

        for record in self:
            if record.photo:
                # In newer Odoo versions, the photo field contains the binary content directly
                size_bytes = len(record.photo)
                if size_bytes > max_size_bytes:
                    raise ValidationError(
                        f"The image size cannot exceed {max_size_mb}MB."
                    )
