from textwrap import dedent

from core.config import settings
from core.templates import templates
from models.user import User
from .send_email import send_email


async def send_verification_email(
    user: User,
    verification_link: str,
):
    """
    Отправка пользователю письма с подтверждением email.

    :param user: Пользователь.
    :param verification_link: Ссылка для подтверждения email.
    :return: None. Функция ничего не возвращает.
    """

    recipient = user.email
    recipient_name = user.first_name
    subject = f"Подтвердите адрес электронной почты для сайта {settings.site.site_name}"

    plain_content = dedent(
        f"""\
        Уважаемый {recipient_name},

        Для подтверждения email, пожалуйста, перейдите по ссылке:
        {verification_link}

        Спасибо за регистрацию на {settings.site.site_name}!
        © 2025 {settings.site.site_name}
        """
    )

    template = templates.get_template("mailing/email-verify/email-verification.html")
    context = {
        "user": user,
        "verification_link": verification_link,
    }
    html_content = template.render(context)
    await send_email(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )
