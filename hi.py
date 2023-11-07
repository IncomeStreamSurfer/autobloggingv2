import openai
import csv
import time
import os
import string
from tqdm import tqdm
import openai.error

# Initialize the OpenAI API client
openai.api_key = "YOUR_API_kEY"

def get_topic_and_links(filename):
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            yield row[0], row[1].split()

def make_api_call(prompt, max_tokens, conversation_history="", retries=3, delay=10):
    prompt_with_history = conversation_history + prompt
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are writerGPT. You never use placeholder content. You create articles for 2Men.it. You always internally link. You never invent internal links, you only use the ones provided. Every 2 paragraphs or so make a list or a table to not have big walls of text. You always create SEO-Optimized articles with titles, including an H1 title at the beginning, then h2 headers for main headers, and h3 headers for subheadings. You never mention h1 or h2 or h3, but instead you use markdown to format. You also internally link, with keyword rich anchor text, for example [kiton](/collections/kiton). You never use an internal link more than once. You always use lists and tables to break up large walls of text."
                    },
                    {
                        "role": "user",
                        "content": prompt_with_history
                    }
                ],
                max_tokens=max_tokens
            )
            new_conversation_history = conversation_history + response['choices'][0]['message']['content']
            return response['choices'][0]['message']['content'], new_conversation_history
        except openai.error.OpenAIError as e:
            print(f"API error: {e}, attempting again in {delay} seconds... ({attempt + 1}/{retries})")
            time.sleep(delay)
    print(f"Request failed after {retries} attempts.")
    return None, conversation_history

def generate_image(prompt):
    try:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        image_url = response['data'][0]['url']
        return image_url
    except openai.error.OpenAIError as e:
        print(f"Failed to generate image due to an API error: {e}")
        return None

def sanitize_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in filename if c in valid_chars)
    filename = filename.replace(' ', '_')  # replace spaces with underscores for Windows compatibility
    return filename

def main():
    # Ensure the directory for articles exists, if not, create it
    article_directory = "articles"
    if not os.path.exists(article_directory):
        os.makedirs(article_directory)

    for idx, (topic, internal_links) in enumerate(tqdm(get_topic_and_links("keywords.csv")), start=1):
        print(f"\nProcessing {idx}. {topic}")
        conversation_history = ""
        
        # Generate an outline for the article
        outline, conversation_history = make_api_call(f"Create an outline for an article on the topic of {topic} using the following internal links: {', '.join(internal_links)}.", 2048, conversation_history)
        if outline is None:
            continue  # Skip this topic if the request failed

        # Generate the full article
        article, conversation_history = make_api_call(f"Write an article based on the outline:\n{outline}", 2048, conversation_history)
        if article is None:
            continue  # Skip this topic if the request failed

        # Generate an image
        image_url = generate_image(f"An image illustrating the concept of {topic}")
        if image_url is None:
            continue  # Skip this topic if image generation failed
        image_markdown = f"![Image related to {topic}]({image_url})\n\n"

        # Generate a key takeaways table for the article
        table, conversation_history = make_api_call(f"Create a key takeaways table summarizing the following article:\n{article}", 2048, conversation_history)
        if table is None:
            continue  # Skip this topic if the request failed

        # Write the article and the table to a file
        sanitized_topic = sanitize_filename(topic)
        with open(os.path.join(article_directory, f"{idx}. {sanitized_topic}.md"), "w", encoding='utf-8') as file:
            file.write(f"# {topic}\n\n{article}\n\n{image_markdown}## Key Takeaways\n{table}")

        print(f"Completed {idx}. {topic}")

if __name__ == "__main__":
    main()
