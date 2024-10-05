import base64

from anthropic import AsyncAnthropic
from anthropic.types import ToolUseBlock

from app.models.image_description import ImageDescription
from app.utils import files
from app.utils.errors import ApplicationError
from app.utils.logger import logger
from env import env


class Anthropic:
    _client: AsyncAnthropic = AsyncAnthropic(api_key=env.ANTHROPIC_API_KEY)

    @staticmethod
    def _get_image_data(image_path: str) -> str:
        media_bytes = files.to_webp(image_path=image_path)

        return base64.b64encode(media_bytes).decode("utf-8")

    async def _describe_image(self, prompt: str, image_path: str) -> ToolUseBlock:
        image_data = self._get_image_data(image_path)
        image_media_type = "image/webp"

        response = await self._client.messages.create(
            model="claude-3-5-sonnet-20240620",
            # model="claude-3-haiku-20240307",
            max_tokens=1024,
            tools=[{
                "name": "get_description",
                "description": "Get description of an image",
                "input_schema": ImageDescription.model_json_schema(),
            }],
            tool_choice={"type": "tool", "name": "get_description"},
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image_media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt or "Describe this image in detail",
                    }
                ],
            }],
            system=env.ANTHROPIC_PROMPT,
        )

        return response.content[0]

    async def describe_image(self, prompt: str, image_path: str, n: int = 3) -> ImageDescription:
        for i in range(n):
            logger.info(f"Describing image, attempt {i + 1}")
            try:
                content = await self._describe_image(prompt, image_path)
                return ImageDescription(**dict(content.input))
            except Exception as e:
                logger.error(f"Error describing image: {e}")
                continue
        else:
            raise ApplicationError("Failed to describe image")
