import logging
logging.basicConfig(level=logging.DEBUG)
 
from trakt import Trakt
import os
 
 
class Application(object):
    def __init__(self):
        self.authorization = None
 
        # Bind trakt events
        Trakt.on('oauth.token_refreshed', self.on_token_refreshed)
 
    def run(self):
        self.authenticate()
 
        if not self.authorization:
            print 'Authentication required'
            exit(1)
 
        # Simulate expired token
        self.authorization['expires_in'] = 0
 
        # Test authenticated calls
        with Trakt.configuration.oauth.from_response(self.authorization):
            # Expired token, requests will return `None`
            print Trakt['sync/collection'].movies()
 
        with Trakt.configuration.oauth.from_response(self.authorization, refresh=True):
            # Expired token will be refreshed automatically (as `refresh=True`)
            print Trakt['sync/collection'].movies()
 
        with Trakt.configuration.oauth.from_response(self.authorization):
            # Current token is still valid
            print Trakt['sync/collection'].movies()
 
    def authenticate(self):
        # Request authentication
        print 'Navigate to %s' % Trakt['oauth/pin'].url()
        pin = raw_input('Pin: ')
 
        # Exchange `code` for `access_token`
        self.authorization = Trakt['oauth'].token_exchange(pin, 'urn:ietf:wg:oauth:2.0:oob')
 
        if not self.authorization:
            return False
 
        print 'Token exchanged - authorization: %r' % self.authorization
        return True
 
    def on_token_refreshed(self, response):
        # OAuth token refreshed, save token for future calls
        self.authorization = response
 
        print 'Token refreshed - authorization: %r' % self.authorization
 
if __name__ == '__main__':
    # Configure
    Trakt.base_url = 'http://api.staging.trakt.tv'
 
    Trakt.configuration.defaults.app(
        id=os.environ.get('Python MediaLibrary')
    )
 
    Trakt.configuration.defaults.client(
        id=os.environ.get('661ed081a80cd8f085839f99fe7f8e91e11a5a66359dcfd9220b737d221a9a90'),
        secret=os.environ.get('661ed081a80cd8f085839f99fe7f8e91e11a5a66359dcfd9220b737d221a9a90')
    )
 
    # Start application
    app = Application()
    app.run()
