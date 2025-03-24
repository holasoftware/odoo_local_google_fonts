import os
import logging


from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.binary import Binary, ANY_UNIQUE

import requests

from ..constants import GSTATIC_BASE_URL, FONT_GOOGLE_APIS_URL, GOOGLE_FONTS_PATH, GOOGLE_FONT_STYLESHEETS_PATH
from ..google_font_stylesheet_processing import process_google_font_stylesheet


_logger = logging.getLogger(__name__)


def generator_file_stream(filepath, chunk_size=4096):
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk


class LocalGoogleFontsWebClient(Binary):
    def _get_or_download_static_file(self, file_path, url, url_query_params=None, text_replacer=None, is_text=True):
        if not os.path.isfile(file_path):
            try:
                res = requests.get(url, params=url_query_params)
                res.raise_for_status()
            except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as e:
                url = e.request.url
                _logger.info("Error downloading url: %s", url)
                return

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if is_text:
                content = res.text
                if text_replacer is not None:
                    content = text_replacer(content)

                with open(file_path, "w") as f:
                    f.write(content)
            else:
                content = res.content
                with open(file_path, "wb") as f:
                    f.write(content)
        else:
            if is_text:
                with open(file_path, "r") as f:
                    content = f.read()
            else:
                content = generator_file_stream(file_path)

        return content

    def _return_cached_static_file(self, content_type=None, headers=None, **kwargs):
        content = self._get_or_download_static_file(**kwargs)

        if content is None:
            raise request.not_found()
        else:
            response = http.Response(content, 200, content_type=content_type, headers=headers)
            return response

    @http.route('/css/font/google', type="http", auth='public')
    def load_google_font(self, **kw):
        file_path = os.path.join(GOOGLE_FONT_STYLESHEETS_PATH, kw["family"])

        family = kw.pop("family")
        url = FONT_GOOGLE_APIS_URL + "?family=" + family
        return self._return_cached_static_file(file_path=file_path, url=url, url_query_params=kw, text_replacer=process_google_font_stylesheet, content_type="text/css")

    # website=True?
    @http.route('/css/font/gstatic/<path:font_subpath>', type="http", auth='public')
    def load_gstatic(self, font_subpath, **kw):
        filename = os.path.basename(font_subpath)
        file_path = os.path.join(GOOGLE_FONTS_PATH, font_subpath)

        if filename.endswith(".ttf"):
            content_type = "font/ttf"
        elif filename.endswith(".otf"):
            content_type = "font/otf"
        elif filename.endswith(".woff"):
            content_type = "font/woff"
        elif filename.endswith(".woff2"):
            content_type = "font/woff2"
        else:
            content_type = "application/octet-stream"

        url = GSTATIC_BASE_URL + font_subpath

        return self._return_cached_static_file(file_path=file_path, content_type=content_type, is_text=False, headers={'Content-Disposition': f'inline: filename="{filename}"'}, url=url, url_query_params=kw)