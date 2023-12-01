import openai
import csv
import time
import os
import string
from tqdm import tqdm
import requests

# Initialize the OpenAI API client
openai.api_key = "your-api-key"

# Constants
AI_CHARACTER_FILE = "Spinnerette.txt"
KEYWORDS_FILE = "keywords.csv"

# Website Settings
WEBSITE = "yourwebsite.com"
EXAMPLE_INTERNAL_LINKS = "[website design](https://www.yourwebsite.com/category/page/)"

# Save Directory
SAVE_DIRECTORY = "articles"

# Language Settings
LANGUAGE = "English"

# Image Style
ELEMENTS = "realistic details, natural lighting, vibrant colors"
FEATURES = "the subject, the setting, the mood"

#['256x256', '512x512', '1024x1024', '1024x1792', '1792x1024'] - 'size'
IMAGE_SIZE = "1792x1024"

def get_topic_and_links(filename):
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            yield row[0], row[1].split()

def make_api_call(prompt, max_tokens, conversation_history="", retries=3, delay=10):
    with open(AI_CHARACTER_FILE, "r", encoding='utf-8') as file:
        prompt_ai_content = file.read()

    prompt_with_history = conversation_history + prompt

    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": prompt_ai_content},
                    # Original
                    {"role": "system", "content": (f"You never use placeholder content. You create articles for {WEBSITE}. You always internally link. You never invent internal links, you only use the ones provided. Every 2 paragraphs or so make a list or a table to not have big walls of text. You always create SEO-Optimized articles with titles, including an H1 title at the beginning, then h2 headers for main headers, and h3 headers for subheadings. You never mention h1 or h2 or h3, but instead you use markdown to format. You also internally link, with keyword rich anchor text, for example {EXAMPLE_INTERNAL_LINKS}. You never use an internal link more than once. You always use lists and tables to break up large walls of text. IMPORTANT: YOU MUST WRITE THIS ARTICLE IN {LANGUAGE} Language")},
                    {"role": "user", "content": prompt_with_history}
                ],
                max_tokens=max_tokens
            )
            content = response.choices[0].message['content']
            new_conversation_history = conversation_history + content
            return content, new_conversation_history
        except openai.error.OpenAIError as e:
            print(f"API error: {e}, attempting again in {delay} seconds... ({attempt + 1}/{retries})")
            time.sleep(delay)
    print(f"Request failed after {retries} attempts.")
    return None, conversation_history

def generate_image(topic, ELEMENTS, FEATURES, save_directory=SAVE_DIRECTORY):
    try:
        # Updated prompt with variables
        prompt = (f"Create a realistic image of {topic}, focusing on lifelike details and natural lighting. The scene should capture {ELEMENTS}. Include elements that highlight {FEATURES}. The composition should be balanced, with attention to depth and perspective, making the viewer feel as if they are looking at a real-life scene. Aim for a high level of detail and clarity, resembling a high-resolution photograph.")

        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size=IMAGE_SIZE,
            n=1
        )
        image_url = response.data[0].url

        # Sanitize the topic to create a valid file name
        valid_chars = "-_." + string.ascii_letters + string.digits + " "
        sanitized_topic = ''.join(c if c in valid_chars else '_' for c in topic)

        # Create save directory if it doesn't exist
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Set the path for the image file
        save_path = os.path.join(save_directory, sanitized_topic + ".png")

        # Download and save the image
        with requests.get(image_url, stream=True) as r:
            r.raise_for_status()
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        return save_path

    except openai.Error as e:
        print(f"Failed to generate image due to an API error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to download the image: {e}")
        return None

def sanitize_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in filename if c in valid_chars)
    filename = filename.replace(' ', '_')
    return filename

def main():
    article_directory = SAVE_DIRECTORY
    if not os.path.exists(article_directory):
        os.makedirs(article_directory)

    for idx, (topic, internal_links) in enumerate(tqdm(get_topic_and_links(KEYWORDS_FILE)), start=1):
        print(f"\nProcessing {idx}. {topic}")
        conversation_history = ""

        outline, conversation_history = make_api_call(f"Create an outline for an article on the topic of {topic} using the following internal links: {', '.join(internal_links)}.", 4096, conversation_history)
        if outline is None:
            continue

        article, conversation_history = make_api_call(f"Write an article based on the outline:\n{outline}", 4096, conversation_history)
        if article is None:
            continue

        image_path = generate_image(topic, ELEMENTS, FEATURES)
        if image_path is None:
            continue
        image_markdown = f"![Image related to {topic}]({image_path})\n\n"

        table, conversation_history = make_api_call(f"Create a key takeaways table summarizing the following article:\n{article}", 4096, conversation_history)
        if table is None:
            continue

        sanitized_topic = sanitize_filename(topic)
        with open(os.path.join(article_directory, f"{idx}. {sanitized_topic}.md"), "w", encoding='utf-8') as file:
            file.write(f"# {topic}\n\n{article}\n\n{image_markdown}## Key Takeaways\n{table}")

        print(f"Completed {idx}. {topic}")

if __name__ == "__main__":
    main()