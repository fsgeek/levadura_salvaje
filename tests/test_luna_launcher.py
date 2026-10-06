"""The Luna deployment must preserve optional selectors and shared schemas."""
import importlib.util
from pathlib import Path

import pytest

pytest.importorskip("hamutay.taste_open")


def test_luna_payload_preserves_optional_recall_selectors():
    from hamutay.taste_open import OpenAITasteBackend
    from hamutay.tools.schemas import RECALL_WORDS_SCHEMA
    import copy
    path = Path(__file__).parents[1] / 'scripts' / 'luna_heartbeat.py'
    spec = importlib.util.spec_from_file_location('luna_heartbeat', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original = copy.deepcopy(RECALL_WORDS_SCHEMA)
    backend = module.LunaTasteBackend(base_url='https://openrouter.ai/api/v1', api_key='fixture', wake_mode='natural')
    payload = backend._first_payload_natural('openai/gpt-6-luna', 'fixture', [], [RECALL_WORDS_SCHEMA])
    function = payload['tools'][0]['function']
    assert function['strict'] is False
    assert function['parameters'] == original['input_schema']
    assert 'record_id' not in function['parameters'].get('required', [])
    assert RECALL_WORDS_SCHEMA == original
    # Other processes and the base backend retain their prior behavior.
    assert 'strict' not in OpenAITasteBackend._openai_tool_def(RECALL_WORDS_SCHEMA)['function']
