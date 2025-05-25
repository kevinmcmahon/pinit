# ABOUTME: Handles web page content extraction and bookmark data generation
# ABOUTME: Uses Claude Sonnet 4.0 to analyze pages and extract metadata

import json
from typing import Any

import llm
from jinja2 import Template


class PinboardBookmarkExtractor:
    """Extracts bookmark metadata from web pages using Claude Sonnet."""

    def __init__(self, model_name: str = "claude-sonnet-4-0") -> None:
        self.model = llm.get_model(model_name)

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

    def extract_bookmark(self, url: str) -> dict[str, Any]:
        """
        Extract bookmark data from a URL.

        Args:
            url: The URL to analyze

        Returns:
            Dictionary with title, url, description, and tags

        Raises:
            ValueError: If the response cannot be parsed as JSON
        """
        prompt = self.prompt_template.render(url=url)
        response = self.model.prompt(prompt, system=self.system_prompt)

        try:
            bookmark_data: dict[str, Any] = json.loads(response.text().strip())
            return bookmark_data
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to parse JSON response: {e}\nResponse was: {response.text()}"
            ) from e
