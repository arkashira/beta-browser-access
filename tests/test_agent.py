import pytest
from agent import create_agent_config, run_agent

@pytest.fixture
def agent_config():
    return create_agent_config('low_privilege_user', 'TLS 1.3')

def test_create_agent_config(agent_config):
    assert agent_config.user == 'low_privilege_user'
    assert agent_config.encryption == 'TLS 1.3'

def test_run_agent(agent_config, monkeypatch):
    monkeypatch.setattr('os.getlogin', lambda: 'NT AUTHORITY\\LocalService')
    monkeypatch.setattr('platform.system', lambda: 'Windows')
    run_agent(agent_config)

def test_run_agent_non_local_service_account(agent_config, monkeypatch):
    monkeypatch.setattr('os.getlogin', lambda: 'other_user')
    monkeypatch.setattr('platform.system', lambda: 'Windows')
    with pytest.raises(RuntimeError):
        run_agent(agent_config)

def test_run_agent_non_tls_13(agent_config, monkeypatch):
    agent_config.encryption = 'TLS 1.2'
    monkeypatch.setattr('os.getlogin', lambda: 'NT AUTHORITY\\LocalService')
    monkeypatch.setattr('platform.system', lambda: 'Windows')
    with pytest.raises(RuntimeError):
        run_agent(agent_config)

def test_run_agent_non_low_privilege_user(agent_config, monkeypatch):
    monkeypatch.setattr('os.getuid', lambda: 1)
    monkeypatch.setattr('os.geteuid', lambda: 1)
    monkeypatch.setattr('platform.system', lambda: 'Linux')
    with pytest.raises(RuntimeError):
        run_agent(agent_config)
