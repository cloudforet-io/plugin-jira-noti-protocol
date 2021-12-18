import logging
from spaceone.core.service import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class ProtocolService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        return {'metadata': {
            'data_type': 'SECRET',
            'data': {
                'schema': {
                    'properties': {
                        'url': {
                            'description': 'Atlassian JIRA URL',
                            'minLength': 4,
                            'title': 'JIRA URL',
                            'type': 'string',
                            'examples': ['https://myjira.atlassian.net']
                        },
                        'email': {
                            'description': 'Atlassian account email address of token',
                            'minLength': 4,
                            'title': 'Email',
                            'type': 'string',
                            'examples': ['fred@example.com']
                        },
                        'api_token': {
                            'description': 'API token value to create your JIRA Ticket',
                            'minLength': 4,
                            'title': 'API Token',
                            'type': 'string',
                            'examples': ['AzxBVkB24CTWmDqMgEkRF147']
                        },
                        'key': {
                            'description': 'Project KEY representing Project ID',
                            'minLength': 2,
                            'title': 'Project KEY',
                            'type': 'string',
                            'examples': ['MYPRJ']
                        }
                    },
                    'required': [
                        'url',
                        'email',
                        'api_token',
                        'key'
                    ],
                    'type': 'object'
                }
            }
        }}

    @transaction
    @check_required(['options'])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params['options']
        secret_data = params.get('secret_data', {})

        return {}
