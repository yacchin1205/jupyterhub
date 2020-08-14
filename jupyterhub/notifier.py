"""Base Notifier class"""
from smtplib import SMTP, SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
from traitlets.config import LoggingConfigurable
from traitlets import Unicode, Integer, Bool


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


class SMTPNotifier(Notifier):
    """SMTP Notifier

    This notifier send notifications via SMTP

    .. versionadded:: 1.1.0
    """

    host = Unicode(
        config=True,
        help="""
        The hostname of SMTP server
        """,
        default="",
    )

    port = Integer(
        config=True,
        help="""
        The port of SMTP server
        """,
        default=0
    )

    ssl = Bool(
        config=True,
        help="""
        Use SSL
        """,
        default=False
    )

    from_mail = Unicode(
        config=True,
        help="""
        E-mail address for From field
        """
    )

    def _create_smtp(self):
        if self.ssl:
            return SMTP_SSL(host=self.host, port=self.port)
        else:
            return SMTP(host=self.host, port=self.port)

    async def notify(self, handler, to, title, body):
        smtp = self._create_smtp()
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = Header(title, "utf-8")
        msg["From"] = Header(self.from_mail, "utf-8")
        to_mails = [u.mail_address for u in to]
        try:
            smtp.sendmail(self.from_mail, to_mails, msg.as_string())
        finally:
            smtp.quit()
        self.log.info("Message sent: %s" % (to_mails))
