"""Tests for SMTP Notifier"""
from unittest import mock

from jupyterhub import notifier


@mock.patch('jupyterhub.notifier.SMTP_SSL')
@mock.patch('jupyterhub.notifier.SMTP')
async def test_smtp_notifier(mocksmtp, mocksmtpssl):
    smtp = notifier.SMTPNotifier()

    mockuser = mock.MagicMock()
    mockuser.mail_address = "test@sample.jp"
    await smtp.notify(None, [mockuser], "TEST", "Test Message")

    mocksmtp.assert_called_with(host='', port=0)
    mocksmtp.return_value.sendmail.assert_called_with(
        '',
        ['test@sample.jp'],
        'Content-Type: text/plain; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: base64\nSubject: =?utf-8?q?TEST?=\nFrom: \nTo: \n\nVGVzdCBNZXNzYWdl\n',
    )


@mock.patch('jupyterhub.notifier.SMTP_SSL')
@mock.patch('jupyterhub.notifier.SMTP')
async def test_smtp_ssl_notifier(mocksmtp, mocksmtpssl):
    smtp = notifier.SMTPNotifier()
    smtp.ssl = True

    mockuser = mock.MagicMock()
    mockuser.mail_address = "test@sample.jp"
    await smtp.notify(None, [mockuser], "TEST", "Test Message")

    mocksmtpssl.assert_called_with(host='', port=0)
    mocksmtpssl.return_value.sendmail.assert_called_with(
        '',
        ['test@sample.jp'],
        'Content-Type: text/plain; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: base64\nSubject: =?utf-8?q?TEST?=\nFrom: \nTo: \n\nVGVzdCBNZXNzYWdl\n',
    )
