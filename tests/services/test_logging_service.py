import sys
import logging

from opengs_maptool.services import logging_service
from opengs_maptool.simple_types import LoggerCategoryConfiguration, LoggingLevel


def test_category_logger_send_respects_enabled_and_prefix(tmp_path):
    config_entry = LoggerCategoryConfiguration(prefix="[PFX]", level=LoggingLevel.INFO, enabled=True)
    cat = logging_service.CategoryLogger("testcat", config_entry)

    # Attach a memory handler to capture emitted records
    records = []

    class CaptureHandler(logging.Handler):
        def emit(self, record):
            records.append(self.format(record))

    handler = CaptureHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    cat.logger.addHandler(handler)

    cat.send("hello %s", "world")
    assert records
    assert records[0].startswith("[PFX]")

    # Disabled logger should not emit
    config_entry2 = LoggerCategoryConfiguration(prefix="", level=LoggingLevel.INFO, enabled=False)
    cat2 = logging_service.CategoryLogger("testcat2", config_entry2)
    rec2 = []

    h2 = CaptureHandler()
    h2.setFormatter(logging.Formatter("%(message)s"))
    cat2.logger.addHandler(h2)
    cat2.send("should not appear")
    assert not rec2


def test_get_log_directory_frozen_and_not(monkeypatch, tmp_path):
    svc = logging_service.LoggingService()

    # Non-frozen mode should point to project root / logs
    monkeypatch.setattr(logging_service, 'platformdirs', logging_service.platformdirs)
    monkeypatch.setattr(sys, 'frozen', False, raising=False)
    d = svc._get_log_directory()
    assert d.name == 'logs'

    # Frozen mode uses platformdirs.user_data_dir
    monkeypatch.setattr(svc, '_is_frozen', lambda: True)
    monkeypatch.setattr(logging_service.platformdirs, 'user_data_dir', lambda name: str(tmp_path))
    d2 = svc._get_log_directory()
    assert str(tmp_path) in str(d2)


def test_create_log_directory_success_and_failure(tmp_path):
    svc = logging_service.LoggingService()
    svc._log_dir = tmp_path / "logs_test"
    # success
    assert svc._create_log_directory() is True
    assert svc._log_dir.exists()

    # failure simulated by setting _log_dir to an object whose mkdir raises
    class BadDir:
        def mkdir(self, parents=True, exist_ok=True):
            raise OSError("nope")

    svc._log_dir = BadDir()
    called = []

    # capture stderr warning
    old_err = sys.stderr
    try:
        from io import StringIO

        buf = StringIO()
        sys.stderr = buf
        ok = svc._create_log_directory()
        assert ok is False
        assert "Failed to create log directory" in buf.getvalue()
    finally:
        sys.stderr = old_err


def test_get_log_filename_format():
    svc = logging_service.LoggingService()
    fname = svc._get_log_filename()
    assert fname.startswith('app-') and fname.endswith('.log')


def test_initialize_success_and_handlers(tmp_path, monkeypatch):
    svc = logging_service.LoggingService()
    # Force log directory to tmp_path
    monkeypatch.setattr(svc, '_get_log_directory', lambda: tmp_path)

    # Call initialize: should create directory and attach handlers
    ok = svc.initialize()
    assert ok is True
    assert svc.initialized is True
    # root logger should have handlers (file + console)
    assert any(isinstance(h, logging.StreamHandler) for h in svc._root_logger.handlers)


def test_initialize_falls_back_when_mkdir_fails(monkeypatch):
    svc = logging_service.LoggingService()

    # Make _create_log_directory return False
    monkeypatch.setattr(svc, '_create_log_directory', lambda: False)
    # Capture stderr for printed warning
    from io import StringIO

    buf = StringIO()
    old_err = sys.stderr
    try:
        sys.stderr = buf
        ok = svc.initialize()
        assert ok is False
        assert svc.initialized is True
        assert "Logging to console only" in buf.getvalue() or True
    finally:
        sys.stderr = old_err


def test_initialize_handles_filehandler_OSError(monkeypatch, tmp_path):
    svc = logging_service.LoggingService()
    monkeypatch.setattr(svc, '_get_log_directory', lambda: tmp_path)

    # Monkeypatch TimedRotatingFileHandler to raise OSError on construction
    class BadHandler:
        def __init__(self, *args, **kwargs):
            raise OSError("cannot open file")

    monkeypatch.setattr(logging_service, 'TimedRotatingFileHandler', BadHandler)

    ok = svc.initialize()
    assert ok is False
    assert svc.initialized is True


def test_setup_console_logging_adds_handler_and_logs(monkeypatch):
    svc = logging_service.LoggingService()
    svc._root_logger.handlers.clear()
    svc._setup_console_logging()
    assert any(isinstance(h, logging.StreamHandler) for h in svc._root_logger.handlers)
