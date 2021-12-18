from spaceone.core.manager import BaseManager
from spaceone.notification.connector.jira import JiraConnector


class JiraManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = None

    def issue_ticket(self, conn, message, **kwargs):
        self.conn: JiraConnector = self.locator.get_connector('JiraConnector')
        self.conn.issue_ticket(conn, message, **kwargs)
