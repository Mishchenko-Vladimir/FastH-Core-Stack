from textwrap import dedent

from core.config import settings
from core.templates import templates
from models.user import User
from .send_email import send_email


async def send_reset_password(
    user: User,
    reset_password_link: str,
):
    """
    Отправка пользователю письма со сбросом пароля.

    :param user: Пользователь.
    :param reset_password_link: Ссылка для сброса пароля.
    :return: None. Функция ничего не возвращает.
    """

    recipient = user.email
    recipient_name = user.first_name
    subject = f"Сбросить пароль на сайте {settings.site.site_name}"

    plain_content = dedent(
        f"""\
        Уважаемый {recipient_name},

        Для сброса пароля, пожалуйста, перейдите по ссылке:
        {reset_password_link}

        Спасибо за использование {settings.site.site_name}!
        © 2025 {settings.site.site_name}
        """
    )

    template = templates.get_template("mailing/email-reset-password.html")
    context = {
        "user": user,
        "reset_password_link": reset_password_link,
    }
    html_content = template.render(context)
    await send_email(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )
