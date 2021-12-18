import os
import logging
import time
import datetime

from spaceone.core import utils, config
from spaceone.tester import TestCase, print_json, to_json
from google.protobuf.json_format import MessageToDict

_LOGGER = logging.getLogger(__name__)

URL = os.environ.get('URL', None)
EMAIL = os.environ.get('EMAIL', None)
API_TOKEN = os.environ.get('API_TOKEN', None)
KEY = os.environ.get('KEY', None)

if API_TOKEN == None or EMAIL == None or URL == None or KEY == None:
    print("""
##################################################
# ERROR
#
# Configure your Slack Token first for test
##################################################
example)

export URL=<YOUR atlassian url>
export EMAIL=<YOUR_atlassian email>
export API_TOKEN=<YOUR_API_TOKEN>
export KEY=<YOUR_JIRA_project_key>
""")
    exit


class TestSlackNotification(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get('SPACEONE_TEST_CONFIG_FILE', './config.yml'))
    endpoints = config.get('ENDPOINTS', {})
    secret_data = {}
    channel_data = {
        'url': URL,
        'email': EMAIL,
        'api_token': API_TOKEN,
        'key': KEY
    }
    print(channel_data)

    def test_init(self):
        v_info = self.notification.Protocol.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        options = {}
        self.notification.Protocol.verify({'options': options, 'secret_data': self.secret_data})

    def test_dispatch(self):
        options = {}

        self.notification.Notification.dispatch({
            'options': options,
            'message': {
                'title': 'This is sample notification',
                'link': 'https://spaceone.console.doodle.spaceone.dev/monitoring/alert-manager/escalation-policy',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Robert_Jacob_Hamerton_-_Poster_for_F._C._Burnand_and_Arthur_Sullivan%27s_The_Contrabandista.jpg/450px-Robert_Jacob_Hamerton_-_Poster_for_F._C._Burnand_and_Arthur_Sullivan%27s_The_Contrabandista.jpg',
                'description': 'Thresholds Crossed: "1" out of the last 1 datapoints [0.524033991396324 (29/06/21 05:06:00)] was less than the lower thresholds [0.6043306920412774] or greater than the upper thresholds [0.6544568893755576] (minimum 1 datapoint for OK -> ALARM transition).',
                'tags': [
                    {
                        'key': 'project_id',
                        'value': 'project-xxxxx',
                        'options': {'short': True}
                    },
                    {
                        'key': 'project_name',
                        'value': '스페이스원 웹서버',
                        'options': {'short': True}
                    },
                    {
                        'key': 'resource_id',
                        'value': 'Resource [Asia Pacific (Seoul)]:[AWS/NetworkELB]: net/af83f347171a044af96459ebb37c8225/743a23562a96c595'
                    },

                ],
                'callbacks': [{
                    'label': 'Acknowledge SpaceONE Alerts',
                    'url': 'https://monitoring-webhook.dev.spaceone.dev/monitoring/v1/alert/alert-61afa17a25bf/4186dacf2d69a689ca4dbed965ef6e2d/ACKNOWLEDGED'
                }],
                'occured_at': datetime.datetime.utcnow().isoformat()
            },
            'notification_type': 'WARNING',
            'secret_data': self.secret_data,
            'channel_data': self.channel_data
        })
