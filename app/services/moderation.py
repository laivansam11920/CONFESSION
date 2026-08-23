from app.base import AiServices
from app.prompts.moderation import _return_prompt_from_list_cfs
from app.utils.logger import logger
from configs import Config

from google import genai
from google.genai.errors import ClientError, APIError


class GenAIModeration(AiServices):

    def __init__(self):
        super().__init__(
            client=genai.Client(api_key=Config.GOOGLE_AI_API_KEY),
            model=Config.MODEL_GOOGLE_AI,
        )

    def get_response(self, contents_input: str) -> str | None:
        try:
            interaction = self.client.models.generate_content(
                model=self.model,
                contents=contents_input,
            )
            if not interaction or not interaction.text:
                return None
            return interaction.text
        except (Exception, ClientError, APIError) as e:
            logger.error(e)

    def check_confession(self, list_confession: dict):
        try:
            list_confession = _return_prompt_from_list_cfs(**list_confession)

            response = self.get_response(list_confession)

            return response
        except (Exception, ClientError, APIError) as e:
            logger.error(e)

moderation = GenAIModeration()