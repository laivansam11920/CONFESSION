from app.database import db
from app.base import AiServices
from app.prompts.moderation import convert_confession_to_prompts as moderation_prompts
from app.utils.logger import console
from app.schema.ResponeSchema import *
from app.schema.confession import ConfessionSchema
from app.schema.ReturnSchema import ReturnSchema
from app.services.moderation.set_cfs_status import UpdateStatusModerationCfs as Cfs
from configs import Config

from google import genai
from google.genai.errors import ClientError, APIError
from google.genai import types
from pymongo.errors import PyMongoError

from json import loads

__all__ = ["moderation"]


class GenAIModeration(AiServices):

    def __init__(self):
        AiServices.__init__(
            self,
            client=genai.Client(
                api_key=Config.GOOGLE_AI_API_KEY,
                http_options=types.HttpOptions(timeout=30000),
            ),
            model=Config.MODEL_GOOGLE_AI,
        )
        self.default_res = ConfessionItemResult()

    @staticmethod
    def _save_confession_moderation(
        cfs: ConfessionSchema, response: ConfessionItemResult
    ) -> None:
        def update():
            try:
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
            except PyMongoError as e:
                console.error(e)

        update()

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
                return self.default_res

            return ConfessionItemResult(**loads(interaction.text))

        except (Exception, ClientError, APIError) as e:
            console.error(e)
            return self.default_res

    @Cfs.update_cfs_moderation
    def update_confession_moderation(self, cfs: ConfessionSchema) -> ReturnSchema:
        try:

            if not cfs or not cfs.confession_id:
                return ReturnSchema()

            if not Config.MODERATION_CONFESSION or not cfs.confession:
                self._save_confession_moderation(cfs, self.default_res)
                return ReturnSchema()

            response: ConfessionItemResult = self.get_response(
                moderation_prompts(cfs.confession)
            )

            if (
                not response
                or response.score is None
                or not (response.reason and response.propose)
            ):
                self._save_confession_moderation(cfs, self.default_res)
                return ReturnSchema()

            self._save_confession_moderation(cfs, response)

            return ReturnSchema(success=True, data={"confession_id": cfs.confession_id})
        except (Exception, PyMongoError) as e:
            console.error(e)
            return ReturnSchema()


moderation = GenAIModeration()
