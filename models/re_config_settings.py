import os
import re
import logging
import threading
import urllib.parse


import requests


from odoo import SUPERUSER_ID, models
from odoo.addons import website


from ..constants import IR_ATTACHMENT_NAMES_WITH_GOOGLE_FONTS
from ..config import GOOGLE_FONTS_PATH, GOOGLE_FONT_STYLESHEETS_PATH
from ..google_font_stylesheet_processing import process_google_font_stylesheet

_logger = logging.getLogger(__name__)


# Fonts are defined here:
#   - addons/website/static/src/scss/primary_variables.scss
#   - addons/website/static/src/scss/secondary_variables.scss
primary_variables_scss_path = os.path.join(
    os.path.dirname(website.__file__), "static", "src", "scss", "primary_variables.scss"
)

with open(primary_variables_scss_path) as f:
    primary_variables_scss_src = f.read()


o_theme_font_configs = re.search(
    r"(\$o-theme-font-configs:\s+\(.+?\n\))", primary_variables_scss_src, re.DOTALL
).group(1)
GOOGLE_FONT_URL_FAMILIES_USED_IN_ODOO = [
    urllib.parse.unquote_plus(m.group(1)) for m in re.finditer(r"'url':\s+'(.+?)'", o_theme_font_configs)
]

font_urls_in_google_stylesheet_re = re.compile(
    r"url\((" + re.escape("https://fonts.gstatic.com/") + r".+?)\)"
)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def _download_fonts(self):
        google_style_stylesheet_download_errors = []
        google_font_download_errors = []

        for font_family in GOOGLE_FONT_URL_FAMILIES_USED_IN_ODOO:
            _logger.info("Downloading CSS stylesheet for font family: %s", font_family)
            gfont_style_file_path = os.path.join(
                GOOGLE_FONT_STYLESHEETS_PATH, font_family
            )

            if not os.path.isfile(gfont_style_file_path):
                try:
                    res = requests.get(
                        "https://fonts.googleapis.com/css?family="
                        + font_family
                        + "&display=swap"
                    )
                    res.raise_for_status()
                except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.RequestException,
                ) as e:
                    url = e.request.url
                    google_font_download_errors.append(url)

                    _logger.info("Error downloading url: %s", url)
                    continue

                text = res.text
                gstatic_urls = [
                    m.group(1) for m in font_urls_in_google_stylesheet_re.finditer(text)
                ]
                text = process_google_font_stylesheet(text)

                os.makedirs(os.path.dirname(gfont_style_file_path), exist_ok=True)

                with open(gfont_style_file_path, "w") as f:
                    f.write(text)

                for gstatic_url in gstatic_urls:
                    _logger.info("Downloading google font: %s", gstatic_url)

                    gstatic_font_file_relative_subpath = gstatic_url[
                        len("https://fonts.gstatic.com/") :
                    ]
                    gstatic_font_file_path = os.path.join(
                        GOOGLE_FONTS_PATH, gstatic_font_file_relative_subpath
                    )

                    if not os.path.isfile(gstatic_font_file_path):
                        try:
                            res = requests.get(gstatic_url, stream=True)
                            res.raise_for_status()
                        except (
                            requests.exceptions.ConnectionError,
                            requests.exceptions.RequestException,
                        ) as e:
                            google_font_download_errors.append(gstatic_url)
                            _logger.info("Error downloading url: %s", gstatic_url)
                            continue

                        os.makedirs(
                            os.path.dirname(gstatic_font_file_path), exist_ok=True
                        )

                        with open(gstatic_font_file_path, "wb") as f:
                            for chunk in res.iter_content(chunk_size=8192):
                                f.write(chunk)

        return {
            "google_style_stylesheet_download_errors": google_style_stylesheet_download_errors,
            "google_font_download_errors": google_font_download_errors,
        }

    def action_delete_ir_attachments_containing_google_fonts(self):
        domain = [
            ("public", "=", True),
            ("url", "!=", False),
            ("name", "in", IR_ATTACHMENT_NAMES_WITH_GOOGLE_FONTS),
            ("res_model", "=", "ir.ui.view"),
            ("res_id", "=", 0),
            ("create_uid", "=", SUPERUSER_ID),
        ]

        attachments = self.env["ir.attachment"].sudo().search(domain)
        thread = threading.Thread(target=self._download_fonts)
        thread.start()

        if attachments:
            attachments.unlink()

            message = "Deleted attachments with google fonts. Downloading fonts in the background."
        else:
            message = "No attachment with google fonts found to delete. Downloading fonts in the background."

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Notification",
                "sticky": False,
                "message": message
            },
        }