import httpx


class MetaModelClient:
    BASE_URL = "https://api.meta.ai/v1"

    def __init__(
        self,
        api_key: str,
        model: str = "muse-spark-1.3",
        transport: httpx.BaseTransport | None = None,
    ):
        if not api_key:
            raise ValueError("Meta API key is required")

        self.model = model
        self.client = httpx.Client(
            base_url=self.BASE_URL,
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

        data = response.json()

        return data["choices"][0]["message"]["content"]

    def close(self):
        self.client.close()