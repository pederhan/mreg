"""Test logging middleware and logging output."""


import io
from unittest.mock import MagicMock, patch

from django.http import HttpRequest, HttpResponse
from structlog import get_logger
from structlog.testing import capture_logs

from mreg.middleware.logging_http import LoggingMiddleware

from django.contrib.auth import get_user_model
from mreg.api.v1.tests.tests import MregAPITestCase
from mreg.log_processors import filter_sensitive_data


class TestLoggingInternals(MregAPITestCase):
    """Test internals in the logging framework."""

    def test_filtering_of_sensitive_data(self):
        """Test that sensitive data is filtered correctly."""
        source_dicts = [
            {
                "model": "ExpiringToken",
                "_str": "1234567890123456789012345678901234567890",
                "id": "1234567890123456789012345678901234567890",
            },
            {
                "model": "ExpiringToken",
                "_str": "123456789",
                "id": "123456789",
            },
            {
                "model": "Session",
                "_str": "123456789012345678901234567890123456789a",
                "id": "123456789012345678901234567890123456789a",
            },
        ]

        expected_dicts = [
            {
                "model": "ExpiringToken",
                "_str": "123...890",
                "id": "123...890",
            },
            {
                "model": "ExpiringToken",
                "_str": "...",
                "id": "...",
            },
            {
                "model": "Session",
                "_str": "123...89a",
                "id": "123...89a",
            },
        ]

        for source_dict, expected_dict in zip(source_dicts, expected_dicts):
            self.assertEqual(
                filter_sensitive_data(None, None, source_dict), expected_dict
            )


class TestLoggingMiddleware(MregAPITestCase):
    """Test logging middleware."""

    def test_run_time_ms_escalation(self):
        """Test run_time_ms escalation for logging levels."""
        middleware = LoggingMiddleware(MagicMock())

        # mock the get_response method to return a response with a specified status code and delay
        def mock_get_response(_):
            return HttpResponse(status=200)

        middleware.get_response = mock_get_response

        # test the behavior of the logging system with different delays
        delay_responses = [
            (0.1, "debug"),
            (0.5, "debug"),
            (1.0, "warning"),
            (2.0, "warning"),
            (5.0, "critical"),
            (5.5, "critical"),
        ]

        for delay, expected_level in delay_responses:
            with patch("time.time", side_effect=[0, delay]):
                with capture_logs() as cap_logs:
                    get_logger().bind()
                    request = HttpRequest()
                    request._body = b"Some request body"
                    request.user = get_user_model().objects.get(username="superuser")
                    middleware(request)
                    # cap_logs[0] is the request, cap_logs[1] is the response
                    self.assertEqual(cap_logs[1]["log_level"], expected_level)

    def test_return_500_error(self) -> None:
        """Test middleware returning 500 error."""
        middleware = LoggingMiddleware(MagicMock())

        def mock_get_response(_):
            return HttpResponse(status=500)

        middleware.get_response = mock_get_response

        with capture_logs() as cap_logs:
            get_logger().bind()
            request = HttpRequest()
            request._read_started = False
            request._stream = io.BytesIO(b"request body")  # mock the _stream attribute
            request.user = get_user_model().objects.get(username="superuser")
            middleware(request)
            self.assertEqual(cap_logs[1]["status_code"], 500)

    def test_proxy_ip_in_logs(self) -> None:
        """Check that a proxy IP is logged."""
        middleware = LoggingMiddleware(MagicMock())

        def mock_get_response(_):
            return HttpResponse(status=500)

        middleware.get_response = mock_get_response

        with capture_logs() as cap_logs:
            get_logger().bind()
            request = HttpRequest()
            request._read_started = False
            request._stream = io.BytesIO(b"request body")
            request.user = get_user_model().objects.get(username="superuser")
            request.META["HTTP_X_FORWARDED_FOR"] = "192.0.2.0"  # set a proxy IP
            middleware(request)
            self.assertEqual(cap_logs[0]["proxy_ip"], "192.0.2.0")
