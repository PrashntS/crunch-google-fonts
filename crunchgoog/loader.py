import tinycss
import urllib.request

test_uri = "http://fonts.googleapis.com/css?family=Open+Sans:300italic,400|Slabo+27px"

class get_css():

    def __init__(self, uri):
        self.download(uri)
    
    def download(self, uri):
        return False


if __name__ == "__main__":
    print(get_css(test_uri))