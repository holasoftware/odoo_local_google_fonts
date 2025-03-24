
def process_google_font_stylesheet(text):
    text.replace("https://fonts.gstatic.com/", "/css/font/gstatic/")
    return text