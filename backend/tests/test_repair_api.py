from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_remains_available():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_repair_endpoint_is_disabled_by_default(monkeypatch):
    monkeypatch.delenv("PROOFPATCH_ENABLE_LOCAL_REPAIR", raising=False)
    monkeypatch.setenv("MODEL_API_KEY", "test-key")

    response = client.post(
        "/repair",
        json={
            "code": "def add(a, b):\n    return a - b\n",
            "test_code": "def test_add():\n    assert add(2, 3) == 5\n",
        },
    )

    assert response.status_code == 503
    assert "disabled" in response.json()["detail"].lower()


def test_repair_rejects_empty_code():
    response = client.post(
        "/repair",
        json={
            "code": "",
            "test_code": "def test_example():\n    assert True\n",
        },
    )

    assert response.status_code == 422


def test_repair_requires_both_fields():
    response = client.post(
        "/repair",
        json={"code": "print('hello')"},
    )

    assert response.status_code == 422


def test_repair_requires_credentials_when_enabled(monkeypatch):
    monkeypatch.setenv("PROOFPATCH_ENABLE_LOCAL_REPAIR", "true")
    monkeypatch.delenv("MODEL_API_KEY", raising=False)

    response = client.post(
        "/repair",
        json={
            "code": "def add(a, b):\n    return a - b\n",
            "test_code": "def test_add():\n    assert add(2, 3) == 5\n",
        },
    )

    assert response.status_code == 503
    assert "credentials" in response.json()["detail"].lower()

def test_repair_rejects_whitespace_only_code(monkeypatch):
    monkeypatch.setenv("PROOFPATCH_ENABLE_LOCAL_REPAIR", "true")

    response = client.post(
        "/repair",
        json={
            "code": "   ",
            "test_code": "def test_example():\n    assert True\n",
        },
    )

    assert response.status_code == 422
    assert "whitespace" in response.json()["detail"].lower()

def test_repair_passes_meta_configuration_to_client(monkeypatch):
    import app.main as main_module

    captured = {}

    class FakeMetaModelClient:
        def __init__(self, **kwargs):
            captured.update(kwargs)

        def close(self):
            captured["closed"] = True

    def fake_workflow(**kwargs):
        return {
            "status": "verified_against_defined_tests",
            "baseline": {"status": "failed"},
            "proposal": None,
            "patch": None,
            "verification": {"status": "passed"},
        }

    monkeypatch.setenv("PROOFPATCH_ENABLE_LOCAL_REPAIR", "true")
    monkeypatch.setenv("MODEL_API_KEY", "test-key")
    monkeypatch.setenv("META_MODEL", "test-model")
    monkeypatch.setenv(
        "META_API_BASE_URL",
        "https://mock-meta.example/v1",
    )

    monkeypatch.setattr(
        main_module,
        "MetaModelClient",
        FakeMetaModelClient,
    )
    monkeypatch.setattr(
        main_module,
        "run_repair_workflow",
        fake_workflow,
    )

    response = client.post(
        "/repair",
        json={
            "code": "def add(a, b): return a + b",
            "test_code": "def test_add(): assert add(2, 3) == 5",
        },
    )

    assert response.status_code == 200
    assert captured["api_key"] == "test-key"
    assert captured["model"] == "test-model"
    assert captured["base_url"] == "https://mock-meta.example/v1"
    assert captured["closed"] is True
