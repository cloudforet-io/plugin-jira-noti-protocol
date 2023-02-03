import requests
import logging
import json

from requests.auth import HTTPBasicAuth

from spaceone.core.connector import BaseConnector

__all__ = ['JiraConnector']
_LOGGER = logging.getLogger(__name__)


class JiraConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def issue_ticket(self, conn, message, **kwargs):
        url = conn.get('url', False)
        email = conn.get('email', False)
        api_token = conn.get('api_token', False)
        if url is False or email is False or api_token is False:
            _LOGGER.error(f'url: {url}, email: {email}, api_token:{api_token}')
            return False
        auth = HTTPBasicAuth(email, api_token)
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

        jira_url = f'{url}/rest/api/3/issue'

        print(message)

        response = requests.request(
            "POST",
            jira_url,
            data=json.dumps(message),
            headers=headers,
            auth=auth)

        _LOGGER.debug(f'[JiraConnector] {response}')
        return response
