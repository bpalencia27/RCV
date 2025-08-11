from rcvco.adapters.llm.factory import get_llm_client
from rcvco.config import settings

def test_factory_default():
    c = get_llm_client()
    assert c.generate_report("hola").startswith(f"[gemini:{settings.GEMINI_MODEL}]")
