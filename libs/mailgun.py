from requests import Response, post
from typing import List


class Mailgun:

    MAILGUN_DOMAIN = "sandboxef49810a6c76481c839cd8d1825462c8.mailgun.org"
    MAILGUN_API_KEY = "0f37e4414b602c70ee3f3d9a2292145d-443ec20e-4ba26b83"
    FROM_TITLE = "Store REST API"
    FROM_EMAIL = "your mailgun email"

    @classmethod
    def send_email(
        cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        return post(
            f"http://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <mailgun@{cls.MAILGUN_DOMAIN}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )
