import pytest
from browser_force import BrowserStatus, upload_enforcement_status, get_local_log, encrypt_log, rotate_log

def test_browser_status() -> None:
    status = BrowserStatus(
        os="Windows 10",
        browser_version="100.0.1",
        timestamp="2024-09-16 14:30:00",
        enforcement_status="success"
    )
    assert status.os == "Windows 10"
    assert status.browser_version == "100.0.1"
    assert status.timestamp == "2024-09-16 14:30:00"
    assert status.enforcement_status == "success"

def test_upload_enforcement_status() -> None:
    status = BrowserStatus(
        os="Windows 10",
        browser_version="100.0.1",
        timestamp="2024-09-16 14:30:00",
        enforcement_status="success"
    )
    assert upload_enforcement_status(status) == True

def test_get_local_log() -> None:
    log = get_local_log()
    assert log["os"] == "Windows 10"
    assert log["browser_version"] == "100.0.1"
    assert log["timestamp"] != ""
    assert log["enforcement_status"] == "success"

def test_encrypt_log() -> None:
    log = get_local_log()
    encrypted_log = encrypt_log(log)
    assert encrypted_log != ""

def test_rotate_log() -> None:
    rotate_log()
    # No assertion, just checking it runs without error

def test_upload_enforcement_status_failure() -> None:
    status = BrowserStatus(
        os="Windows 10",
        browser_version="100.0.1",
        timestamp="2024-09-16 14:30:00",
        enforcement_status="failure",
        reason="Browser not installed"
    )
    assert upload_enforcement_status(status) == True

def test_encrypt_log_empty() -> None:
    log = {}
    encrypted_log = encrypt_log(log)
    assert encrypted_log == "{}"
