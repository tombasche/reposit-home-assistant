import logging

import requests
from requests import HTTPError
from requests.auth import HTTPBasicAuth

from reposit.auth import AUTH_URL

logger = logging.getLogger(__name__)


class RPConnection(object):
    """
    Establish a connection to the Reposit cloud
    """
    def _login(self):
        """
        Given a username and password, obtain an access token
        :return:
        """
        resp = requests.post(AUTH_URL, auth=HTTPBasicAuth(self.username, self.password), headers={
            "Reposit-Auth": "API"
        })
        try:
            resp.raise_for_status()
        except HTTPError:
            if resp.status_code in (401, 403):
                logger.exception('Unauthorized. Please check your credentials are correct.')
                return None
            else:
                logger.exception('Unable to authenticate - please try again later.')
                return None
        return resp.json()['access_token']

    def __init__(self, username, password):
        """
        Authenticate with a username and password.
        :param username:
        :param password:
        """
        self.username = username
        self.password = password
        self.token = self._login()

    def __str__(self):
        return self.username