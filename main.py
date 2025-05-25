import json
import os
import sys

import llm
import pinboard
from dotenv import load_dotenv
from jinja2 import Template

# Load environment variables
load_dotenv()


class PinboardBookmarkExtractor:
    def __init__(self):
        self.model = llm.get_model("anthropic/claude-sonnet-4-0")

        self.system_prompt = """You are a bookmark extraction assistant. Fetch the web page content and extract bookmark data.
Extract these four fields:
- title: The main title/headline of the page (not the HTML title tag, but the actual content title)
- url: The original URL provided
- description: A concise 1-2 sentence summary of what the page is about
- tags: An array of 3-8 relevant lowercase tags (use hyphens for multi-word tags)
CRITICAL: Return ONLY the JSON object with no additional text, explanations, code fences, or markdown formatting. Your entire response must be valid JSON that can be parsed directly."""

        self.prompt_template = Template(
            """Please fetch and analyze this web page to create a Pinboard bookmark entry:
URL: {{ url }}
First fetch the web page content, then extract the bookmark data as JSON. DO NOT include a code fence."""
        )

    def extract_bookmark(self, url):
        """
        Extract bookmark data from a URL

        Args:
            url (str): The URL to analyze

        Returns:
            dict: Parsed JSON with title, url, description, and tags
        """
        # Render the prompt with the URL
        prompt = self.prompt_template.render(url=url)

        # Get response from the model
        response = self.model.prompt(prompt, system=self.system_prompt)

        # Parse the JSON response
        try:
            bookmark_data = json.loads(response.text().strip())
            return bookmark_data
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to parse JSON response: {e}\nResponse was: {response.text()}"
            )


def add_bookmark_from_json(pb, bookmark_json):
    """Add a bookmark to Pinboard from a JSON object"""

    # If bookmark_json is a string, parse it
    if isinstance(bookmark_json, str):
        bookmark_data = json.loads(bookmark_json)
    else:
        bookmark_data = bookmark_json

    # Map JSON fields to Pinboard API parameters
    result = pb.posts.add(
        url=bookmark_data["url"],
        description=bookmark_data["title"],  # Pinboard calls the title "description"
        extended=bookmark_data.get(
            "description", ""
        ),  # Pinboard calls the description "extended"
        tags=bookmark_data.get("tags", []),
        shared=True,  # Make it public (set to False for private)
        toread=False,  # Set to True if you want to mark it as "to read"
    )

    return result


def main():
    # Check if URL argument is provided
    if len(sys.argv) < 2:
        print("Usage: python main.py <url>")
        sys.exit(1)

    url = sys.argv[1]

    # Initialize the Pinboard client
    pb = pinboard.Pinboard(os.getenv("PINBOARD_API_TOKEN"))
    extractor = PinboardBookmarkExtractor()

    try:
        bookmark = extractor.extract_bookmark(url)
        print(json.dumps(bookmark, indent=2))

        result = add_bookmark_from_json(pb, bookmark)
        if not result:
            print("Failed to add bookmark.")
            return
        else:
            print("Bookmark added successfully.")
        print(f"Bookmark added successfully: {result}")
    except Exception as e:
        print(f"Error adding bookmark: {e}")


if __name__ == "__main__":
    main()
