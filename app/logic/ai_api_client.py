# app/logic/ai_api_client.py

"""This module defines our AI model inputs and handles the API calls."""

import logging
import os
import requests

LOG = logging.getLogger(__name__)

class AIHandler:
    """
        AIHandler provides methods to instantiate and handle OpenRouter
        AI API calls.
    """

    def __init__(self):
        LOG.info("Initializing AIHandler...")

        # Get all inputs needed for API call
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = "deepseek/deepseek-r1-0528-qwen3-8b:free"
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def get_ai_response(self, system_prompt, user_prompt):
        """Sends an API call to OpenRouter AI."""
        LOG.info("Attempting to send request and receive OpenRouter AI API call response.")
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }

        try:
            response = requests.post(
                url=self.url,
                headers=self.headers,
                json=data,
                timeout=10
            )
            LOG.info("Response from OpenRouter AI call was: %s", response)
            response.raise_for_status()

            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as error:
            print(response.text)
            return f"AI request failed: {error}"
