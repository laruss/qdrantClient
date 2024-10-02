from pydantic import BaseModel

from app.encoder import encoder


class ImageDescription(BaseModel):
    description: str
    setting: str
    femaleDescription: str
    femalePromiscuity: str
    places: list[str]
    hashtags: list[str]  # hashtags are not used in the vector representation, but are used in the description

    def get_as_vector(self) -> list[float]:
        """
        Get the description as a vector

        Returns:
            list[float]: The description as a vector
        """
        data = self.model_dump(exclude={'hashtags'})
        data_values = list(data.values())

        for i, value in enumerate(data_values):
            # if value is a list, join it into a string
            if isinstance(value, list):
                data_values[i] = ' '.join(value)

        result = []

        for value in data_values:
            result += encoder.encoder.encode(value).tolist()

        return result
