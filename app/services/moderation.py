from app.base import AiServices, ConfessionManager
from app.prompts.moderation import _return_prompt_from_list_cfs
from app.utils.logger import logger
from .get_confession import GetConfession
from configs import Config

from google import genai
from google.genai.errors import ClientError


class GenAIModeration(AiServices, ConfessionManager):

    def __init__(self):
        super().__init__(
            client=genai.Client(api_key=Config.GOOGLE_AI_API_KEY),
            model=Config.MODEL_GOOGLE_AI,
        )



    def check_confession(self, **list_confession): ...
