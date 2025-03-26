import os
import threading


from odoo import models, exceptions


from ..download_default_google_fonts import download_default_google_fonts
from ..attachments_with_google_fonts import delete_attachments_with_google_fonts


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def action_local_google_fonts_init(self):
        """Action for deleting ir attachments with google fonts and downloading the missing fonts in the background"""

        if not self.env.user.has_group("base.group_system"):
            raise exceptions.AccessError('Only administrators can perform this operation.')

        thread = threading.Thread(target=download_default_google_fonts)
        thread.start()

        num_attachments = delete_attachments_with_google_fonts(self.env)

        if num_attachments != 0:
            message = "Deleted attachments with google fonts."
        else:
            message = "No attachment with google fonts found to delete."

        message +=  " Downloading fonts in the background."

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Notification",
                "sticky": False,
                "message": message
            },
        }