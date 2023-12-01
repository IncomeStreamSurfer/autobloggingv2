# OpenAI Content and Image Generator

This script uses the OpenAI API for automated creation of SEO-optimized articles, related images, and key takeaways tables. It's tailored for content creation websites, focusing on generating articles with internal linking and images using DALL-E 3.

## Features

- **Article Generation**: Generates article outlines and full articles on specific topics.
- **Image Generation**: Creates images relevant to article topics using DALL-E.
- **SEO Optimization**: Incorporates internal linking and formats articles using markdown for SEO.
- **Key Takeaways Table**: Summarizes articles in a table format.

## Prerequisites

- Python 3.x
- An active OpenAI API key.

## Installation and Setup

1. **Clone the Repository**: Download the script files to your local machine.
2. **Set Up a Python Virtual Environment**:
   - Create the environment: `python -m venv env` (replace `env` with your desired environment name).
   - Activate the environment:
     - On Windows: `env\Scripts\activate` (replace `env` with your desired environment name).
     - On Unix or MacOS: `source env/bin/activate` (replace `env` with your desired environment name).
3. **Install Required Packages**: Install the dependencies with `pip install -r requirements.txt`.
4. **Place your OpenAI API key in the script**.

## Usage

1. Define your topics and internal links in `your-keywords.csv`.
2. Run the script within the virtual environment: `python start-now.py`.
3. The generated content will be stored in the `articles` directory.

## Configuration

To tailor the script to your needs, various configuration options are available:

- **OpenAI API Key**:

  - Set your OpenAI API key: `openai.api_key = "your-api-key"`. Replace `"your-api-key"` with your actual OpenAI API key.

- **File Settings**:

  - `AI_CHARACTER_FILE`: The file containing the AI character details. Default is `"Aria_Linkwell.txt"`.
  - `KEYWORDS_FILE`: The file for specifying keywords. Default is `"FlyingWeb-keywords.csv"`.
  - `SAVE_DIRECTORY`: The directory where articles and images are saved. Default is `"articles"`.

- **Website Settings**:

  - `WEBSITE`: The website name for which content is being generated, e.g., `"your-website.com"`.
  - `EXAMPLE_INTERNAL_LINKS`: Example format for internal links, e.g., `"[service](/services/service-name)"`.

- **Image Generation Settings**:
  - `ELEMENTS`: Defines the setting and atmosphere for the image. Example: `"websites, currency symbols"`.
  - `FEATURES`: Specifies particular details to highlight in the image. Example: `"cost aspects, affordability"`.
  - `IMAGE_SIZE`: Determines the resolution of the generated images. Options include `'256x256', '512x512', '1024x1024', '1024x1792', '1792x1024'`. Default is `"1792x1024"`.

Modify these settings in the script as per your requirements to customize the content and image generation process.

## Image Generation

The script includes a feature for generating images using OpenAI's DALL-E 3 model. These images are created based on a set of variables: `topic`, `elements`, and `features`. To achieve the best results, it's important to update these variables according to the specific requirements of your content.

### Elements and Features

When generating images, the script takes into consideration the setting and atmosphere (`elements`) and specific details (`features`). The table below provides examples of what you can specify for these variables:

| Elements (Setting and Atmosphere)             | Features (Specific Details)                     |
| --------------------------------------------- | ----------------------------------------------- |
| 1. Time of Day (e.g., dawn, noon, dusk)       | 1. Textures (e.g., rough, smooth, glossy)       |
| 2. Mood (e.g., serene, bustling, mysterious)  | 2. Colors (e.g., vibrant, muted, monochrome)    |
| 3. Weather (e.g., sunny, rainy, foggy)        | 3. Actions (e.g., running, dancing, resting)    |
| 4. Season (e.g., spring, summer, winter)      | 4. Light Effects (e.g., shadows, reflections)   |
| 5. Location (e.g., urban, rural, forest)      | 5. Material Qualities (e.g., metallic, wooden)  |
| 6. Historical Era (e.g., medieval, modern)    | 6. Emotions (e.g., joy, sorrow, excitement)     |
| 7. Architectural Style (e.g., Gothic, modern) | 7. Movement (e.g., flowing, static, dynamic)    |
| 8. Event (e.g., festival, quiet evening)      | 8. Nature Elements (e.g., leaves, water, rocks) |

Customizing these `elements` and `features` for each topic will help in generating images that are more aligned with your content, enhancing the overall quality and relevance of the generated images.

## Deactivating the Virtual Environment

Once you're done, you can deactivate the virtual environment by typing `deactivate` in your terminal.

## Disclaimer

This tool is intended for educational and research purposes. Please adhere to the OpenAI usage policy and guidelines.

## License

[MIT License](https://opensource.org/licenses/MIT)
