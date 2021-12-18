import time
import logging

from spaceone.core import utils
from spaceone.core.service import *
from spaceone.notification.conf.jira_conf import JIRA_CONF
from spaceone.notification.manager.notification_manager import NotificationManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class NotificationService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)

    @transaction
    @check_required(['options', 'message', 'notification_type'])
    def dispatch(self, params):
        """
        Args:
            params:
                - options
                - message
                - notification_type
                - secret_data
                - channel_data
        """
        channel_data = params.get('channel_data', {})
        notification_type = params['notification_type']
        message = params['message']
        kwargs = {}

        # get Key for payload building
        key = channel_data.get('key')

        noti_mgr: NotificationManager = self.locator.get_manager('NotificationManager')
        message_payload = self._make_jira_issue_ticket(message, notification_type, key)

        noti_mgr.dispatch(channel_data, message_payload, **kwargs)


    def _make_jira_issue_ticket(self, message, notification_type, key):
        '''
        message (dict): {
            'title': 'str',
            'link': 'str',
            'image_url': 'str,
            'description': str,
            'tags': [
                {
                    'key': '',
                    'value': '',
                    'options': {
                        'short': true|false
                    }
                }
            ],
            'callbacks': [
              {
                'label': 'str',
                'url': 'str',
                'options': 'dict'
              }
            ],
            'occurred_at': 'iso8601'
        }

        JIRA format: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-post
        '''

        project_key = key
        title = message.get("title", "No Title")

        description = self._make_jira_description(message)
        payload = {
            "update": {},
            "fields": {
                "issuetype":    {"name": "Task"},
                "project":      {"key" : project_key},
                "summary":      title,
                "description":  description
            }
        }
        return payload

    def _make_jira_description(self, message):
        """ Make Atlassian Document format
        URL: https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/

        MESSAGE example
        ---
        'message': {
                'title': 'This is sample notification',
                'link': 'https://spaceone.console.doodle.spaceone.dev/monitoring/alert-manager/escalation-policy',
                'image_url': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/jal.png',
                'description': 'Thresholds Crossed: 1 out of the last 1 datapoints [0.524033991396324 (29/06/21 05:06:00)] was less than the lower thre  sholds [0.6043306920412774] or greater than the upper thresholds [0.6544568893755576] (minimum 1 datapoint for OK -> ALARM transition).',
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
        """

        content = []
        content.append(self._create_paragraph(message.get('description', 'No description')))
        if 'tags' in message:
            content.append(self._create_table(message['tags']))
        if 'link' in message:
            content.append(self._create_link(message['link'], message['link']))
        for callback in message['callbacks']:
            content.append(self._create_acknowledge(self._create_link(callback['label'], callback['url'])))


        jira_description = {
            "version": 1,
            "type": "doc",
            "content": content
        }

        return jira_description

    @staticmethod
    def _create_paragraph(description):
        """
        Create JIRA content from description

        Return(dict): JIRA content
        """
        content = {
            "type": "paragraph",
            "content": [ {
                "type": "text",
                "text": description
                }
                        ]
        }
        return content

    @staticmethod
    def _create_table(tags):
        """
        Create Table from Tags
        """
        def _cell(value, mark=False):
            """ if mark == False, no action
            mark = "strong" | "strike" | "em"
            """
            content = {"type": "text", "text": value}
            if mark:
                content.update({"marks": [{"type": mark}]})

            cell = {
              "type": "tableCell",
              "attrs": {},
              "content": [
                {
                  "type": "paragraph",
                  "content": [content]
                }
              ]
            }
            return cell

        rows = []
        for tag in tags:
            rows.append({
                "type": "tableRow",
                "content": [_cell(tag["key"], "strong"), _cell(tag["value"])]
            })

        content = {
            "type": "table",
            "attrs": {
                "isNumberColumnEnabled": False,
                "layout": "default"
            },
            "content": rows
        }
        return content

    @staticmethod
    def _create_link(title, link):
        """
        https://developer.atlassian.com/cloud/jira/platform/apis/document/marks/link/
        """
        link_text = {
            "type": "text",
            "text": title,
            "marks": [
                {
                    "type": "link",
                    "attrs": {
                        "href": link,
                        "title": title
                    }
                }
                ]
        }
        content = {
            "type": "paragraph",
            "content": [link_text]
        }
        return content

    @staticmethod
    def _create_acknowledge(link_content):
        """
        https://developer.atlassian.com/cloud/jira/platform/apis/document/marks/link/
        """
        content = {
            "type": "panel",
            "attrs": {
                "panelType": "warning"
            },
            "content": [link_content]
        }

        return content


