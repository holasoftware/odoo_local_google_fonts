# Local google fonts
Host google fonts and serve them from your own odoo instance.

Supported odoo version: 18

## Rationale
Serving cached google fonts improves privacy. For European citizens, hosting the google fonts locally doesn't require user consent for being GDPR compliant.

It also allows local development without internet connection. Some odoo modules like the website module requires to load some google fonts by default to function properly, otherwise there is an error loading the website editor because it couldn't load without errors the stylesheet.

At the same time, not having the computer connected to the Internet has some advantages such as being less exposed to cybersecurity risks and also saving internet data.

## Configuration
It's possible to configure the directories used to store the google font files and stylesheets using environment variables:

- `ODOO_LOCAL_GOOGLE_FONTS_CACHE_DIR_PATH`

Path to directory used for storing locally the data for this module (google font stylesheets and font files). By default, it's the directory `google_fonts` in odoo data directory. (`data_dir` config parameter).

- `ODOO_GOOGLE_FONT_STYLESHEETS_PATH`

Path to the directory for storing the google font stylesheets. By default, it's the same value than `LOCAL_GOOGLE_FONTS_CACHE_DIR_PATH`.

- `ODOO_GOOGLE_FONTS_PATH`

Path to the directory for storing the font files. By default, it's the subdirectory `gstatic` in `ODOO_LOCAL_GOOGLE_FONTS_CACHE_DIR_PATH`.

- `ODOO_DONT_DOWNLOAD_GOOGLE_FONTS_ON_MODULE_INSTALL`

If the value of this environment variable is `1`, the module doesn't host the google fonts on install. It will be required to install manually in the settings section from the superuser.


## How does it work?
After installation, the application starts downloading the default google fonts used in odoo and defined here:
```
    addons/website/static/src/scss/primary_variables.scss
```
It also deletes some attachments in the database like stylesheet bundles containing URL's to stylesheet with declarations for google fonts. The next time the bundle is regenerated, the content's bundle will have the links to google fonts pointing to local resources. The font files referenced in the google font stylesheet are also extracted and downloaded and the links to external resources are replaced to links pointing to the cached ones. The download process is executed in a python thread.

The module also adds a button in a new section called `Local Google Fonts` in the General settings only available for the admin. Clicking the button, the module runs the same process as when it was installed. It helps to download again google fonts not yet cached (because there was no internet connection during installation and it was not possible to download the fonts for example) or deleted manually and to regenerate the attachments containing google fonts with all the replacement links.