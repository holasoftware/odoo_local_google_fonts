import os

from odoo import tools


FONT_GOOGLE_APIS_URL = "https://fonts.googleapis.com/css"
GSTATIC_BASE_URL = "https://fonts.gstatic.com/"

IR_ATTACHMENT_NAMES_WITH_GOOGLE_FONTS = ['website.assets_all_wysiwyg.min.js', 'website.assets_all_wysiwyg.js', 'website.assets_all_wysiwyg.min.css', 'website.assets_all_wysiwyg.css', 'web.assets_frontend.min.css', 'web.assets_frontend.css', 'website.backend_assets_all_wysiwyg.min.css', 'website.backend_assets_all_wysiwyg.css', 'website.assets_wysiwyg.min.css', 'website.assets_wysiwyg.css']


LOCAL_GOOGLE_FONTS_CACHE_DIR_PATH = os.path.join(tools.config['data_dir'], "google_fonts")
LOCAL_GOOGLE_FONTS_CACHE_DIR_PATH = os.getenv("LOCAL_GOOGLE_FONTS_CACHE_DIR_PATH", LOCAL_GOOGLE_FONTS_CACHE_DIR_PATH)

GOOGLE_FONT_STYLESHEETS_PATH = os.getenv("GOOGLE_FONT_STYLESHEETS_PATH", LOCAL_GOOGLE_FONTS_CACHE_DIR_PATH)
GOOGLE_FONTS_PATH = os.path.join(LOCAL_GOOGLE_FONTS_CACHE_DIR_PATH, "gstatic")
GOOGLE_FONTS_PATH = os.getenv("GOOGLE_FONTS_PATH", GOOGLE_FONTS_PATH)