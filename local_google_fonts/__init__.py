import threading


from . import controllers
from . import models
from .config import DONT_DOWNLOAD_GOOGLE_FONTS_ON_MODULE_INSTALL


from .download_default_google_fonts import download_default_google_fonts
from .attachments_with_google_fonts import delete_attachments_with_google_fonts


def post_init(env):
    if DONT_DOWNLOAD_GOOGLE_FONTS_ON_MODULE_INSTALL == '1':
        return

    delete_attachments_with_google_fonts(env)

    thread = threading.Thread(target=download_default_google_fonts)
    thread.start()