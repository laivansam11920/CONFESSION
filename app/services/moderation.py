from app.base import AiServices, ConfessionManager
from app.prompts.moderation import convert_confession_to_prompts as moderation_prompts
from app.utils.logger import logger
from app.schema.ResponeSchema import (
    ConfessionModerationPayload,
    ConfessionModerationResponse,
    ConfessionItemResult,
)
from configs import Config

from google import genai
from google.genai.errors import ClientError, APIError

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

    def update_confession(self, list_confession: dict):
        try:

            if not Config.MODERATION_CONFESSION:
                return None

            response = self.get_response(moderation_prompts(**list_confession))

            if not response:
                return None
            print(response.results)
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
                            "is_moderation_post": True
                        },
                    },
                )

            return response
        except (Exception, ClientError, APIError) as e:
            logger.error(e)


moderation = GenAIModeration()
