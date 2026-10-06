import importlib.util
import json
import sys
from pathlib import Path


def load_reader():
    spec = importlib.util.spec_from_file_location('luna_read', Path(__file__).parents[1]/'scripts/luna_read.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_reader_records_attempt_before_first_wake_finishes(tmp_path, monkeypatch, capsys):
    reader=load_reader()
    monkeypatch.setattr(reader,'HOME',tmp_path)
    monkeypatch.setattr(sys,'argv',['reader','--by','fixture','--why','first wake'])
    reader.main()
    assert 'No completed' in capsys.readouterr().out
    assert json.loads((tmp_path/'reads.jsonl').read_text().splitlines()[-1])['cycles']==[]


def test_reader_outputs_only_addressed_reply_and_logs_failed_wake(tmp_path,monkeypatch,capsys):
    reader=load_reader()
    monkeypatch.setattr(reader,'HOME',tmp_path)
    monkeypatch.setattr(sys,'argv',['reader','--by','fixture','--why','check addressed reply'])
    records=[{'cycle':1,'response_text':'ADDRESSED','state':{'secret':'PRIVATE_SENTINEL'},'raw_output':'RAW_SENTINEL'},
             {'cycle':2,'response_text':'','status':'failed','failure_classification':{'reason':'PRIVATE_ERROR_DETAIL'}}]
    (tmp_path/'session.jsonl').write_text('\n'.join(json.dumps(r) for r in records)+'\n')
    reader.main()
    out=capsys.readouterr().out
    assert 'ADDRESSED' in out and 'failed' in out
    assert all(secret not in out for secret in ('PRIVATE_SENTINEL','RAW_SENTINEL','PRIVATE_ERROR_DETAIL'))
    assert json.loads((tmp_path/'reads.jsonl').read_text().splitlines()[-1])['cycles']==[1,2]


def test_reader_keeps_completed_replies_when_tail_is_being_written(tmp_path, monkeypatch, capsys):
    reader=load_reader()
    monkeypatch.setattr(reader,'HOME',tmp_path)
    monkeypatch.setattr(sys,'argv',['reader','--by','fixture','--why','concurrent read'])
    complete=json.dumps({'cycle':1,'response_text':'ADDRESSED'})+'\n'
    (tmp_path/'session.jsonl').write_text(complete+'{"cycle":2,"state":{"secret":"PRIVATE_TAIL')
    reader.main()
    out=capsys.readouterr().out
    assert 'ADDRESSED' in out and 'PRIVATE_TAIL' not in out
    ledger=json.loads((tmp_path/'reads.jsonl').read_text().splitlines()[-1])
    assert ledger['cycles']==[1] and ledger['incomplete_tail'] is True


def test_corrupt_complete_record_still_logs_inspection(tmp_path, monkeypatch):
    import pytest
    reader=load_reader()
    monkeypatch.setattr(reader,'HOME',tmp_path)
    monkeypatch.setattr(sys,'argv',['reader','--by','fixture','--why','corrupt record'])
    (tmp_path/'session.jsonl').write_text('{invalid\n')
    with pytest.raises(RuntimeError,match='line 1'):
        reader.main()
    assert json.loads((tmp_path/'reads.jsonl').read_text().splitlines()[-1])['error_line']==1


def test_wanderer_reader_does_not_read_or_log_first_resident(tmp_path, monkeypatch, capsys):
    reader = load_reader()
    first = tmp_path / 'luna'
    second = tmp_path / 'luna-wanderer'
    first.mkdir()
    second.mkdir()
    (first / 'session.jsonl').write_text(json.dumps({'cycle':1,'response_text':'FIRST_PRIVATE'})+'\n')
    (second / 'session.jsonl').write_text(json.dumps({'cycle':1,'response_text':'SECOND_ADDRESSED'})+'\n')
    monkeypatch.setattr(reader, 'HOME', first)
    monkeypatch.setattr(sys, 'argv', ['reader','--resident','luna-wanderer','--by','fixture','--why','second reply'])
    reader.main()
    output = capsys.readouterr().out
    assert 'SECOND_ADDRESSED' in output and 'FIRST_PRIVATE' not in output
    assert (second / 'reads.jsonl').exists()
    assert not (first / 'reads.jsonl').exists()
