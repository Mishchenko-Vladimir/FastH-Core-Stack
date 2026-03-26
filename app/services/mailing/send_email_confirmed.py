from textwrap import dedent

from core.config import settings
from core.templates import templates
from models.user import User
from .send_email import send_email


async def send_email_confirmed(user: User):
    """
    Отправка письма пользователю о подтверждении email.

    :param user: Пользователь.
    :return: None. Функция ничего не возвращает.
    """

    recipient = user.email
    recipient_name = user.first_name
    subject = "Адрес электронной почты подтвержден"

    plain_content = dedent(
        f"""\
        Уважаемый {recipient_name},

        Ваш адрес электронной почты подтверждён.

        Спасибо за использование {settings.site.site_name}!
        © 2025 {settings.site.site_name}
        """
    )

    template = templates.get_template("mailing/email-verify/email-verified.html")
    context = {"user": user}
    html_content = template.render(context)
    await send_email(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )
