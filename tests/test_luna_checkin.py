import importlib.util
import sys
from pathlib import Path
import pytest

@pytest.mark.parametrize('resident', ['luna', 'luna-wanderer'])
def test_daily_invitation_goes_to_selected_home(tmp_path, monkeypatch, resident):
    spec = importlib.util.spec_from_file_location('checkin', Path(__file__).parents[1]/'scripts/luna_checkin.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, 'HOME', tmp_path/'luna')
    calls = []
    monkeypatch.setattr(module.subprocess, 'run', lambda command, **kwargs: calls.append(command))
    monkeypatch.setattr(sys, 'argv', ['checkin','--resident',resident])
    module.main()
    assert len(calls) == 1
    command = calls[0]
    assert command[command.index('--log-path')+1] == str(tmp_path/resident/'session.jsonl')
