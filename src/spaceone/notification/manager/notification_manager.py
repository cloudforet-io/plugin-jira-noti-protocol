from spaceone.core.manager import BaseManager
from spaceone.notification.manager.jira_manager import JiraManager


class NotificationManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dispatch(self, conn, message, **kwargs):
        jira_mgr: JiraManager = self.locator.get_manager('JiraManager')
        jira_mgr.issue_ticket(conn, message, **kwargs)
