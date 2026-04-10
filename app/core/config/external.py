from pydantic import BaseModel, SecretStr


class WebhookConfig(BaseModel):
    """Конфигурация вебхука, для отправки сообщений"""

    # Куда будут отправляться сообщения
    webhook_url: str


class SMTPConfig(BaseModel):
    """Конфигурация SMTP для отправки писем"""

    # Режим работы приложения: False - письма уходили в MailHog, True - отправляются на реальный SMTP
    use_real_smtp: bool = False

    host: str  # SMTP-сервер (smtp.gmail.com, smtp.yandex.ru, smtp.mail.ru, smtp-mail.outlook.com , smtp.sendgrid.net)
    port: int = 587  # Порт для подключения: 587 (TLS), 465 (SSL), 25 (устаревший)
    username: str  # Логин (обычно email)
    password: SecretStr  # (app password - пароль для приложения)
    use_tls: bool = True  # Использовать ли шифрование TLS
    timeout: int = 10  # Максимальное время ожидания ответа от сервера (в секундах)
