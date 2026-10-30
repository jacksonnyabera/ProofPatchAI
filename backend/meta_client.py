import httpx


class MetaModelClient:
    BASE_URL = "https://api.meta.ai/v1"

    def __init__(
        self,
        api_key: str,
        model: str = "muse-spark-1.3",
        transport: httpx.BaseTransport | None = None,
        base_url: str | None = None,
    ):
        if not api_key:
            raise ValueError("Meta API key is required")

        self.model = model

        self.client = httpx.Client(
            base_url=base_url or self.BASE_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
            transport=transport,
        )

    def chat(self, prompt: str) -> str:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        response = self.client.post(
            "/chat/completions",
            json={
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
            },
        )

        response.raise_for_status()

        try:
            data = response.json()
        except ValueError as exc:
            raise ValueError("Meta returned invalid JSON") from exc

        if not isinstance(data, dict):
            raise ValueError("Meta response must be a JSON object")

        choices = data.get("choices")

        if not isinstance(choices, list) or not choices:
            raise ValueError("Meta response is missing choices")

        message = choices[0].get("message") if isinstance(choices[0], dict) else None

        if not isinstance(message, dict):
            raise ValueError("Meta response is missing the message")

        content = message.get("content")

        if not isinstance(content, str):
            raise ValueError("Meta response content must be a string")

        return content

    def close(self):
        self.client.close()