import cssutils
import urllib.request

test_uri = "http://localhost:90/test_server.css"

class imitator:

    user_agents = {
        'self': 'Mozilla/5.0 Chrunch Google Fonts',
        'chrome_mac': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36',
        'safari_mac': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
    }

    def download(self, uri, browser = user_agents['self']):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', self.user_agents[browser])]
        try:
            return (opener.open(uri).read())
        except:
            return False

class parse:
    def __init__(self):
        #self.parser = cssutils.p('page3')
        self.stylesheets = []

    def get_font_uri(self, css):
        self.stylesheets.append(cssutils.parseString(css))

        for rule in self.stylesheets[-1]:
            if rule.type == rule.FONT_FACE_RULE:
                for prop in rule.style:
                    if prop.name == 'src':
                        font_sources = prop.value
                        print(font_sources)
        return False

    #def 

if __name__ == "__main__":
    css = imitator().download(test_uri, 'chrome_mac')

    parse().get_font_uri(css)