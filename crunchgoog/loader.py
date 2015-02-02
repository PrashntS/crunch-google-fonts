import cssutils
import urllib.request
import os
import re
import uuid

test_uri = "http://localhost:90/test_server.css"

class imitator:

    user_agents = {
        'self': 'Mozilla/5.0 Chrunch Google Fonts',
        'chrome_mac': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36',
        'safari_mac': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
    }

    def fetch(self, uri, browser = user_agents['self']):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', self.user_agents[browser])]
        try:
            return (opener.open(uri).read())
        except:
            return False

    def download(self, uri, location):
        return urllib.request.urlretrieve(uri, location)[0]

class attribute_dictionary():
    def __init__(self, source):
        self.source = source
        self.pattern = r"[ \"\']*" + r"{0}" + r"\(" + r"[ \"\']*" + r"(.*?)" + r"[ \"\']*" + r"\)" + r"[ \"\']*"

    def get(self, key):
        pattern = self.pattern.format(key)
        return re.findall(pattern, self.source)

    def set(self, key, value):
        dat = self.get(key)
        pattern = self.pattern.format(key)

        if type(value) is list:
            if len(dat) == len(value):
                value = value[::-1]
                self.source = re.sub(pattern, lambda match: " {0}({1}) ".format(key, value.pop()), self.source)
                return True
            else:
                return False

        elif type(value) is str:
            self.source = re.sub(pattern, " {0}({1}) ".format(key, value), self.source)
            return True

        else:
            return False

    def get_replaced_string(self):
        return self.source

class parse:
    def __init__(self):
        self.stylesheets = []
        self.dir_location = os.curdir + os.sep + 'fonts'
        self.file_name = self.dir_location + os.sep + '{0}'
        self.downloader = imitator.download
        if not os.path.isdir(self.dir_location):
            os.makedirs(self.dir_location)

    def routine(self, css):
        self.stylesheets.append(cssutils.parseString(css))

        for rule in self.stylesheets[-1]:
            if rule.type == rule.FONT_FACE_RULE:
                for prop in rule.style:
                    if prop.name == 'src':
                        font_sources = prop.value
                        new_sources = self.get_font_from_source(font_sources)
                        prop.value = new_sources
        return True

    def get_font_from_source(self, value):
        # Retrieve the font. Save it, and return the new path.
        attributes_list = attribute_dictionary(value)
        font_list = attributes_list.get('url')
        replacement_list = []

        for font in font_list:
            font_file_name = self.f_name()
            font_location = self.file_name.format(font_file_name)
            saved_font_uri = imitator().download(font, font_location)
            replacement_list.append('fonts/'+font_file_name)

        attributes_list.set('url', replacement_list)
        return attributes_list.get_replaced_string()

    def f_name(self):
        return str(uuid.uuid4())

    def save_stylesheet(self, location = None):
        if location is None:
            location = os.curdir
        file_loc = location + os.sep + "font_" + self.f_name() + ".css"
        print(file_loc)
        with open(file_loc, "wb") as Minion:
            for sheet in self.stylesheets:
                Minion.write(sheet.cssText)
                Minion.write(b"\r\n")
        return True

class routines:
    def fetch_all(base_stylesheet_uri):
        css_reparser = parse()

        for browser, user_agents in imitator.user_agents.items():
            returned_css = imitator().fetch(base_stylesheet_uri, browser)
            css_reparser.routine(returned_css)

        css_reparser.save_stylesheet()

if __name__ == "__main__":
    routines.fetch_all(test_uri)