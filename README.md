# Local google fonts
Host google fonts and serve them from your own odoo instance.

## Rationale
Serving cached google fonts improves privacy. For European citizens, hosting the google fonts locally doesn't require user consent for being GDPR compliant. It also allows local development without internet connection. Some odoo modules like the website module requires to load some google fonts by default to function properly, otherwise there is an error loading the website editor because it couldn't load without errors the stylesheet. At the same time, not having the computer connected to the Internet has some advantages such as being less exposed to cybersecurity risks and also saving internet data.

## Configuration
It's possible to configure the directories used to store the google font files and stylesheets using environment variables
- `LOCAL_GOOGLE_FONTS_CACHE_DIR_PATH`: Path to directory used for storing locally the data for this module (google font stylesheets and font files). By default, it's the directory `google_fonts` in odoo data directory. (`data_dir` config parameter).
- `GOOGLE_FONT_STYLESHEETS_PATH`: Path to the directory for storing the google font stylesheets. By default it's the same value than `LOCAL_GOOGLE_FONTS_CACHE_DIR_PATH`.
- `GOOGLE_FONTS_PATH`: Path to the directory for storing the font files. By default is the directory `gstatic` in `LOCAL_GOOGLE_FONTS_CACHE_DIR_PATH`.

## How does it work?
The application adds a button in a new section `Local Google Fonts` in the General settings. Clicking the button the application deletes some attachments in the database like stylesheet bundles containing URL's to stylesheet with declarations for google fonts. The next time that the bundle is regenerated, the content's bundle will have the links to google fonts pointing to local resources. The font files referenced in the google font stylesheet are also extracted and downloaded and the links to external resources are replaced to links pointing to the cached ones.

Also all the default fonts used in odoo, defined in `addons/website/static/src/scss/primary_variables.scss` are scrapped and downloaded in a thread if they are not yet cached.