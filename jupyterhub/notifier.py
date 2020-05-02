"""Base Notifier class"""
from traitlets.config import LoggingConfigurable


class Notifier(LoggingConfigurable):
    """Base class for implementing a notifier for JupyterHub"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def notify(self, handler, to, title, body):
        """Notify a message to user

        This must be a coroutine.

        Args:
            handler (tornado.web.RequestHandler): the current request handler
            to (list): The users which receive this notification
            title (str): The title of this message
            body (str): The body of this message
        Returns:
            None
        """


class DummyNotifier(Notifier):
    """Dummy Notifier for testing

    This notifier write the notification to the log

    .. versionadded:: 1.0
    """

    async def notify(self, handler, to, title, body):
        self.log.info("Notification: to: %r" % [u.mail_address for u in to])
        self.log.info("Notification: title: %r" % title)
        self.log.info("Notification: message: %r" % body)
