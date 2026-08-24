from app.base import AiServices, ConfessionManager
from app.prompts.moderation import convert_confession_to_prompts as moderation_prompts
from app.utils.logger import logger
from app.schema.ResponeSchema import *
from configs import Config

from google import genai
from google.genai.errors import ClientError, APIError
from pymongo.errors import PyMongoError

from json import loads

__all__ = ["moderation"]


class GenAIModeration(AiServices, ConfessionManager):

    def __init__(self):
        AiServices.__init__(
            self,
            client=genai.Client(api_key=Config.GOOGLE_AI_API_KEY),
            model=Config.MODEL_GOOGLE_AI,
        )
        ConfessionManager.__init__(self)

    def get_response(self, contents_input: str) -> ConfessionModerationResponse | None:
        try:
            interaction = self.client.models.generate_content(
                model=self.model,
                contents=contents_input,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": ConfessionModerationPayload,
                },
            )
            if not interaction or not interaction.text:
                return None

            res = loads(interaction.text)
            items = [ConfessionItemResult(**item) for item in res.get("results", [])]
            return ConfessionModerationResponse(results=items)

        except (Exception, ClientError, APIError) as e:
            logger.error(e)

    def update_confession_moderation(self, list_confession: dict) -> bool:
        try:

            if not Config.MODERATION_CONFESSION:
                return False

            response = self.get_response(moderation_prompts(**list_confession))

            if not response:
                return False

            for item in response.results:
                self.db.docs.update_one(
                    {"confession_id": item.id_origin},
                    {
                        "$set": {
                            "ai_data": {
                                "score": item.score,
                                "reason": item.reason,
                                "propose": item.propose,
                                "uncertain": item.uncertain,
                            },
                            "status": "approved",
                        },
                    },
                )

            return True
        except (Exception, PyMongoError) as e:
            logger.error(e)
            return False


moderation = GenAIModeration()
