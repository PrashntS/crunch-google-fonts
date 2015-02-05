import cssutils
import urllib.request
import os
import re
import uuid
import argparse

options = {
    'dir_location': os.curdir + os.sep + 'fonts',
    'relative_uri': 'fonts/',
    'output_css': str(uuid.uuid4())
}

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
    """
    Parses, Modifies, and Returns the attribute dictionary. Sample attribute
    dictionary is of form:
    Example: a(val_a), b( "val_b" ), a('val_c'). Notice the varying Quotes, and Spaces.
    The above attribute dictionary is parsed to a Python Dictionary-like interface as
    source = {
        a: "val_a",
        b: "val_b",
        a: "val_c"
    }
    Notice that the values are automatically type-promoted/type-casted to String.
    Also, the keys are positional - not named.

    All properties are Greedy.
    """

    def __init__(self, source):
        """Initializes the class instance."""
        self.source = source
        self.pattern = r"[ \"\']*" + r"{0}" + r"\(" + r"[ \"\']*" + r"(.*?)" + r"[ \"\']*" + r"\)" + r"[ \"\']*"

    def get(self, key):
        """
        Returns the Values associated with the key. Since the attribute_dictionary
        can inherently have multiple values, this always returns a List containing
        every encountered value of the given Key. Returns an empty List in case of
        invalid key.
        Greedy.
        """
        pattern = self.pattern.format(key)
        return re.findall(pattern, self.source)

    def set(self, key, value):
        """
        Sets the value associated to the given key. If the "value" argument is
        passed a String, Every Instances of the Key in the attribute_dictionary
        are set to this String.
        If the value argument is passed a List, instead, The "positional" values
        of the Key are set in the order of appearance in the List. Obviously the
        dimension of value must be equal to the number of occurrence of the key
        (len(get(key))).
        Greedy.
        """
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

    def stringify(self):
        """Returns the String representation of attribute_dictionary."""
        return self.source

class crunch:
    """
    Provides methods to Crunch the CSS URI.
    """

    def __init__(self):
        """
        Prepares the class instance, sets the imitator instance, and retrieves defaults.
        """
        self.stylesheets = []
        self.dir_location = options['dir_location']
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
            replacement_list.append(options['relative_uri'] + font_file_name)

        attributes_list.set('url', replacement_list)
        return attributes_list.stringify()

    def f_name(self):
        return str(uuid.uuid4())

    def save_stylesheet(self):
        file_loc = options['dir_location'] + os.sep + options['output_css'] + ".css"
        with open(file_loc, "wb") as Minion:
            for sheet in self.stylesheets:
                Minion.write(sheet.cssText)
                Minion.write(b"\r\n")
        return True

class routines:
    def fetch(base_stylesheet_uri):
        css_reparser = parse()

        for browser, user_agents in imitator.user_agents.items():
            returned_css = imitator().fetch(base_stylesheet_uri, browser)
            css_reparser.routine(returned_css)

        css_reparser.save_stylesheet()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Crunches the Google Font CSS, and liberates them from their Server! Very helpful, if you want to test your website locally, or, serve over your own Server/CDN.',
        prog = 'Crunch Google Fonts')

    parser.add_argument('-s', "--source", nargs='?', help='The CSS URI.')
    parser.add_argument('-d', "--destination", nargs='?', default=os.curdir, help='The CSS URI.')
    parser.add_argument('-r', "--relative_path", nargs='?', default='LOL', help='The CSS URI.')

    args = parser.parse_args()
    print(args)
    parser.print_help()



    #routines.fetch_all(test_uri)