import httpx
import pytest

from meta_client import MetaModelClient


def make_client(handler):
    return MetaModelClient(
        api_key="test-key",
        model="muse-spark-1.3",
        base_url="https://mock.meta.test/v1",
        transport=httpx.MockTransport(handler),
    )


def test_chat_returns_model_content_and_uses_configured_url():
    def handler(request):
        assert str(request.url) == (
            "https://mock.meta.test/v1/chat/completions"
        )
        assert request.headers["Authorization"] == "Bearer test-key"

        return httpx.Response(
            200,
            json={
                "choices": [
                    {"message": {"content": '{"root_cause": "test"}'}}
                ]
            },
        )

    client = make_client(handler)

    try:
        assert client.chat("Fix this bug") == '{"root_cause": "test"}'
    finally:
        client.close()


def test_client_rejects_missing_api_key():
    with pytest.raises(ValueError, match="API key"):
        MetaModelClient(api_key="")


def test_chat_rejects_empty_prompt():
    client = make_client(
        lambda request: httpx.Response(200, json={})
    )

    try:
        with pytest.raises(ValueError, match="Prompt"):
            client.chat("   ")
    finally:
        client.close()


def test_chat_raises_for_http_errors():
    client = make_client(
        lambda request: httpx.Response(401, json={"error": "Unauthorized"})
    )

    try:
        with pytest.raises(httpx.HTTPStatusError):
            client.chat("Test prompt")
    finally:
        client.close()


def test_chat_rejects_invalid_json():
    client = make_client(
        lambda request: httpx.Response(200, text="not-json")
    )

    try:
        with pytest.raises(ValueError, match="invalid JSON"):
            client.chat("Test prompt")
    finally:
        client.close()


def test_chat_rejects_missing_choices():
    client = make_client(
        lambda request: httpx.Response(200, json={"unexpected": "data"})
    )

    try:
        with pytest.raises(ValueError, match="choices"):
            client.chat("Test prompt")
    finally:
        client.close()


def test_chat_rejects_missing_message_content():
    client = make_client(
        lambda request: httpx.Response(
            200,
            json={"choices": [{"message": {}}]},
        )
    )

    try:
        with pytest.raises(ValueError, match="content"):
            client.chat("Test prompt")
    finally:
        client.close()