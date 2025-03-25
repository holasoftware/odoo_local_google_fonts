from odoo import models

from ..constants import IR_ATTACHMENT_NAMES_WITH_GOOGLE_FONTS


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def _postprocess_contents(self, values):
        values = super()._postprocess_contents(values)

        if (
            values["name"] in IR_ATTACHMENT_NAMES_WITH_GOOGLE_FONTS
        ):  # and values['mimetype'] == 'text/css':
            values["raw"] = (
                values["raw"]
                .decode()
                .replace("https://fonts.googleapis.com/css", "/css/font/google")
                .encode()
            )
        return values
