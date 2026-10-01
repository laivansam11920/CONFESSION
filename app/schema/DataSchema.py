from dataclasses import dataclass


@dataclass(frozen=True)
class TemplateParams:
    email: str
    link: str
    confession: str
    post_time: int
    score: str
    reason: str


@dataclass(frozen=True)
class MailSchema:
    service_id: str
    template_id: str
    user_id: str
    accessToken: str
    template_params: dict
