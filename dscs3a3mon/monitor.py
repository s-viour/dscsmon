import logging
import requests

class Monitor:
    def __init__(self, webhook):
        self.session = requests.Session();
        self.cache = {}
        self.baseurl = 'https://terminal.armory.cloud/request.php'
        self.webhook = webhook
        self.session.post(self.webhook, {
            'content': 'monitor starting!'
        })
    
    def command(self, cmd):
        params = {}
        params['command'] = cmd
        self.session.post(self.webhook, {
            'content': f'checking command {cmd}'
        })
        r = self.session.get(self.baseurl, params=params)
        if self.cache.get(cmd) is None:
            logging.info(f'populated cache for command {cmd}')
            self.cache[cmd] = r.json()
        elif self.cache[cmd] == r.json():
            logging.info(f'command {cmd} cache hit')
        else:
            self.cache[cmd] = r.json()
            logging.critical(f'command {cmd} updated!')
            self.session.post(self.webhook, {
                'content': f'command {cmd} updated!'
            })

        return self.cache[cmd]