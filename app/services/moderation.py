from app.base import AiServices, ConfessionManager
from app.prompts.moderation import _return_prompt_from_list_cfs
from app.utils.logger import logger
from configs import Config

from google import genai
from google.genai.errors import ClientError


class GenAIModeration(AiServices, ConfessionManager):

    def __init__(self):
        super().__init__(
            client=genai.Client(api_key=Config.GOOGLE_AI_API_KEY),
            model=Config.MODEL_GOOGLE_AI,
        )

    def get_confession(self):
        try:
            confession = self.db.docs.find(
                {"status": "pending", "send": False},
                {"_id": 0, "confession": 1, "confession_id": 1},
            )
            list_confession = {}

            for docs in confession:

                confession_id = docs.get("confession_id", None)
                confession = docs.get("confession", None)

                if confession_id and confession:
                    list_confession[confession_id] = confession

            return list_confession
        except Exception as e:
            logger.error(e)

    def check_confession(self, **list_confession): ...
