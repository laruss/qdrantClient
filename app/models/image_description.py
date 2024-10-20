from pydantic import BaseModel, Field

from app.utils.encoder import encoder


class ImageDescription(BaseModel):
    description: str = Field(..., description="The description of the image", title='h')
    setting: str = Field(..., description="The setting of the image", title='s')
    femaleDescription: str = Field(..., description="The description of the female in the image")
    femalePromiscuity: str = Field(..., description="If there is a female in the photo, describe her promiscuity (where promiscuity stands for the totality of the provocativeness of the female's clothing, pose, makeup and other parameters.)")
    places: list[str] = Field(..., description="The places where the image could be taken")
    # hashtags are not used in the vector representation, but are used in the description
    hashtags: list[str] = Field(..., description="The hashtags of the image")

    def get_as_vector(self) -> dict[str, list[float]] | dict[str, tuple[list[float], float]]:
        """
        Get the description as a vector

        Returns:
            dict[str, float]: The description as a vector
        """
        data = self.model_dump(exclude={'hashtags'})
        result = {}

        for key, value in data.items():
            if isinstance(value, list):
                value = ' '.join(value)
            result[key] = encoder.encoder.encode(value).tolist()

        return result
