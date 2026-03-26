import aiosmtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.config import settings


async def send_email(
    recipient: str,
    subject: str,
    plain_content: str,
    html_content: str = "",
):
    """
    Асинхронная отправка email через SMTP-сервер.

    :param recipient: Кому отправляется письмо.
    :param subject: Тема письма.
    :param plain_content: Текст письма.
    :param html_content: HTML письма.
    :return: None. Функция ничего не возвращает.
    """

    message = MIMEMultipart("alternative")
    message["From"] = settings.smtp.username
    message["To"] = recipient
    message["Subject"] = subject

    plain_text_message = MIMEText(
        plain_content,
        "plain",
        "utf-8",
    )
    message.attach(plain_text_message)

    if html_content:
        html_message = MIMEText(
            html_content,
            "html",
            "utf-8",
        )
        message.attach(html_message)

    if settings.smtp.enabled or settings.site.environment == "production":
        await aiosmtplib.send(
            message,
            hostname=settings.smtp.host,
            port=settings.smtp.port,
            username=settings.smtp.username,
            password=settings.smtp.password,
            use_tls=settings.smtp.use_tls,
        )
    else:
        # Режим разработки — отправка в MailHog
        await aiosmtplib.send(
            message,
            hostname="127.0.0.1",
            port=1025,
        )
