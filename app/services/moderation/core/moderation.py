from app.database import db
from app.base import AiServices
from app.prompts.moderation import convert_confession_to_prompts as moderation_prompts
from app.utils.logger import console
from app.schema.ResponeSchema import *
from app.schema.confession import ConfessionSchema
from configs import Config

from google import genai
from google.genai.errors import ClientError, APIError
from pymongo.errors import PyMongoError

from json import loads

__all__ = ["moderation"]


class GenAIModeration(AiServices):

    def __init__(self):
        AiServices.__init__(
            self,
            client=genai.Client(api_key=Config.GOOGLE_AI_API_KEY),
            model=Config.MODEL_GOOGLE_AI,
        )

    def get_response(self, contents_input: str) -> ConfessionItemResult:
        try:
            interaction = self.client.models.generate_content(
                model=self.model,
                contents=contents_input,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": ConfessionItem,
                },
            )
            if not interaction or not interaction.text:
                return ConfessionItemResult()

            res = loads(interaction.text)

            return ConfessionItemResult(**res)

        except (Exception, ClientError, APIError) as e:
            console.error(e)
            return ConfessionItemResult()

    def update_confession_moderation(self, cfs: ConfessionSchema) -> bool:
        try:

            if not Config.MODERATION_CONFESSION:
                return False

            if not cfs.confession_id or not cfs.confession:
                return False

            response: ConfessionItemResult = self.get_response(
                moderation_prompts(cfs.confession)
            )

            if (
                not response
                or response.score is None
                or not (response.reason and response.propose)
            ):
                return False

            db.docs.update_one(
                {"confession_id": cfs.confession_id},
                {
                    "$set": {
                        "ai_data": {
                            "score": response.score,
                            "reason": response.reason,
                            "propose": response.propose,
                            "uncertain": response.uncertain,
                        },
                        "status": "approved",
                    },
                },
            )

            return True
        except (Exception, PyMongoError) as e:
            console.error(e)
            return False


moderation = GenAIModeration()
