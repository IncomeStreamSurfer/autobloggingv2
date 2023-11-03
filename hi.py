import openai
import csv
import time
from tqdm import tqdm
import openai.error

# Initialize the OpenAI API client
openai.api_key = "YOUR_OPEN_AI_KEY"

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
                model="gpt-4",
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
        except openai.error.Timeout as e:
            print(f"Request timed out, retrying in {delay} seconds... ({attempt + 1}/{retries})")
            time.sleep(delay)
    print(f"Failed to complete the request after {retries} retries due to timeout.")
    return None, conversation_history

def main():
    for idx, (topic, internal_links) in enumerate(get_topic_and_links("keywords.csv"), start=1):
        print(f"Processing {idx}. {topic}")
        conversation_history = ""
        outline, conversation_history = make_api_call(f"Create an outline for an article on the topic of {topic} using the following internal links: {', '.join(internal_links)}.", 2048, conversation_history)
        if outline is None:
            continue  # Skip this topic if the request timed out
        first_third, conversation_history = make_api_call(f"Based on the outline:\n{outline}\nWrite the part of the article from token 0 to token {len(outline) // 3}.", (len(outline) // 3), conversation_history)
        second_third, conversation_history = make_api_call(f"Based on the outline:\n{outline}\nWrite the part of the article from token {len(outline) // 3} to token {(2 * len(outline)) // 3}.", ((2 * len(outline)) // 3) - (len(outline) // 3), conversation_history)
        final_third, conversation_history = make_api_call(f"Based on the outline:\n{outline}\nWrite the part of the article from token {(2 * len(outline)) // 3} to token {len(outline)}.", len(outline) - ((2 * len(outline)) // 3), conversation_history)
        article = f"{first_third}{second_third}{final_third}"
        table, conversation_history = make_api_call(f"Create a key takeaways table summarizing the following article:\n{article}", 2048, conversation_history)
        with open(f"{idx}. {topic}.txt", "w") as file:
            file.write(f"# {topic}\n\n{article}\n\n## Key Takeaways\n{table}")
        print(f"Completed {idx}. {topic}")

if __name__ == "__main__":
    main()
