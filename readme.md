# Qdrant Web Service for Image Description Vectorization

## Overview

This web service is built using `FastAPI` and `Python 3.12` to provide vectorization of image descriptions based on a JSON input file. 
It leverages the Qdrant vector search engine to store and query vector representations of image metadata. 
The service is designed to handle image metadata, not the actual image files themselves. 
Additionally, it supports image storage on DigitalOcean and includes an option for merging facial attributes when relevant.

## Features
- **Vectorization of Image Descriptions**: Converts descriptions provided in JSON format into vector representations.
- **Integration with Qdrant**: Stores and queries vectorized metadata.
- **Image Storage on DigitalOcean**: Uploaded images are stored in a DigitalOcean bucket.
- **Face Merge Functionality**: Capable of merging facial attributes based on provided metadata.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/laruss/qdrantClient.git
   cd qdrantClient
   ```

2. **Up the docker-compose:**
   ```bash
   docker compose up
   ```

3. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set environment variables:**

   - `QDRANT_HOST`: The host address for your Qdrant instance.
   - `QDRANT_PORT`: The port number for your Qdrant instance.
   - `QDRANT_COLLECTION`: The collection name for your Qdrant instance.
   - `DOP_SPACE_PRIVATE_API_KEY`: The DigitalOcean Spaces private API key.
   - `DOP_SPACE_PUBLIC_ACCESS_KEY`: The DigitalOcean Spaces public access key.
   - `DOP_SPACE_NAME`: The DigitalOcean Spaces bucket name.
   - `DOP_SPACE_REGION`: The DigitalOcean Spaces region.

6. **Run the FastAPI service:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage

1. **Upload Image Metadata:**
   
   Send a POST request to the `/files/data` endpoint with a JSON file containing image descriptions. Each entry should follow this format:

   ```json
   {
       "<IMAGE_NAME>": {
            "description": "<DESCRIPTION>",
            "setting": "<SETTING>",
            "femaleDescription": "<femaleDescription>",
            "femalePromiscuity": "<femalePromiscuity>",
            "places": ["<PLACE1>", "<PLACE2>"],
            "hashtags": ["<HASHTAG1>", "<HASHTAG2>"]
       }
   }
   ```

2. **Search for Similar Images:**

   Use the `/search` endpoint to query images based on vectorized descriptions. The query should contain a text description to be converted into a vector and searched against the stored metadata.
   A payload should be the same, as in the previous step.

## Dependencies

- **Python 3.12**
- **FastAPI**
- **Qdrant Client**
- **DigitalOcean SDK**

## Contributing

Please feel free to submit issues and pull requests to improve the functionality of the service.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

Feel free to update the specific project name, repository URL, or any additional configuration parameters as needed.

### TODO

- [ ] Add tests
