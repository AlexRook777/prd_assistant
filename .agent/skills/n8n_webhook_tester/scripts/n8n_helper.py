"""
N8n Webhook Testing Utility

This module provides utilities for testing webhooks using the n8n infrastructure.
It supports generating unique order IDs, sending webhooks, and retrieving webhook data.
"""

import json
import time
import uuid
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    requests = None


class N8nWebhookTester:
    """Utility class for n8n webhook testing operations."""

    # Load configuration
    _config_path = Path(__file__).parent.parent / "resources" / "config.json"
    with open(_config_path) as f:
        _config = json.load(f)

    SEND_BASE_URL = _config["n8n_endpoints"]["send_webhook_base_url"]
    RETRIEVE_BASE_URL = _config["n8n_endpoints"]["retrieve_webhook_base_url"]
    AUTH_USERNAME = _config["auth"]["username"]
    AUTH_PASSWORD = _config["auth"]["password"]
    DEFAULT_TIMEOUT = _config["defaults"]["timeout_seconds"]
    DEFAULT_POLL_INTERVAL = _config["defaults"]["poll_interval_seconds"]
    DEFAULT_MAX_RETRIES = _config["defaults"]["max_retries"]

    @staticmethod
    def generate_order_id() -> str:
        """
        Generate a unique order ID for webhook testing.

        Returns:
            str: A unique UUID string suitable for use as an order ID.

        Example:
            >>> order_id = N8nWebhookTester.generate_order_id()
            >>> print(order_id)
            'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
        """
        return str(uuid.uuid4())

    @staticmethod
    def get_send_url(order_id: str) -> str:
        """
        Get the webhook send URL for a specific order ID.

        Args:
            order_id: The unique order identifier.

        Returns:
            str: The complete webhook URL where the provider should send callbacks.

        Example:
            >>> url = N8nWebhookTester.get_send_url("test-order-123")
            >>> print(url)
            'https://n8n.4bill.io/webhook/0154f998-9882-4b6b-b08b-a3a9e6e3d38b/test-order-123'
        """
        return f"{N8nWebhookTester.SEND_BASE_URL}/{order_id}"

    @staticmethod
    def retrieve_webhooks(
        order_id: str,
        timeout: int | None = None,
        poll_interval: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Retrieve all webhooks received for a specific order ID.

        This method polls the n8n endpoint with Basic Auth to fetch webhook data.
        It will retry until webhooks are found or timeout is reached.

        Args:
            order_id: The unique order identifier.
            timeout: Maximum time to wait in seconds (default: from config).
            poll_interval: Time between polling attempts in seconds (default: from config).

        Returns:
            list[dict[str, Any]]: List of webhook payloads received.

        Raises:
            ImportError: If requests library is not available.
            requests.RequestException: If the HTTP request fails.
            TimeoutError: If no webhooks are received within the timeout period.

        Example:
            >>> webhooks = N8nWebhookTester.retrieve_webhooks("test-order-123")
            >>> print(f"Received {len(webhooks)} webhooks")
        """
        if requests is None:
            raise ImportError(
                "requests library is required. Install with: pip install requests"
            )

        timeout = timeout or N8nWebhookTester.DEFAULT_TIMEOUT
        poll_interval = poll_interval or N8nWebhookTester.DEFAULT_POLL_INTERVAL

        url = f"{N8nWebhookTester.RETRIEVE_BASE_URL}/{order_id}"
        auth = (N8nWebhookTester.AUTH_USERNAME, N8nWebhookTester.AUTH_PASSWORD)

        start_time = time.time()
        attempts = 0

        while time.time() - start_time < timeout:
            attempts += 1
            try:
                response = requests.get(url, auth=auth, timeout=10)
                response.raise_for_status()

                data = response.json()

                # Check if we received any webhooks
                if isinstance(data, list) and len(data) > 0:
                    return data
                elif isinstance(data, dict) and data:
                    return [data]

                # No webhooks yet, wait and retry
                time.sleep(poll_interval)

            except requests.RequestException as e:
                # Log error but continue polling
                print(f"Attempt {attempts} failed: {e}")
                time.sleep(poll_interval)

        # Timeout reached without receiving webhooks
        raise TimeoutError(
            f"No webhooks received for order_id '{order_id}' within {timeout} seconds"
        )

    @staticmethod
    def format_for_report(webhooks: list[dict[str, Any]]) -> str:
        """
        Format webhook data for inclusion in markdown reports.

        Args:
            webhooks: List of webhook payloads.

        Returns:
            str: Formatted markdown string with webhook details.

        Example:
            >>> webhooks = [{"status": "paid", "amount": 100}]
            >>> print(N8nWebhookTester.format_for_report(webhooks))
        """
        if not webhooks:
            return "No webhooks received."

        output = []
        output.append(f"**Total Webhooks Received**: {len(webhooks)}\n")

        for idx, webhook in enumerate(webhooks, 1):
            output.append(f"### Webhook {idx}")
            output.append("```json")
            output.append(json.dumps(webhook, indent=2))
            output.append("```\n")

        return "\n".join(output)

    @staticmethod
    def get_curl_example(order_id: str) -> str:
        """
        Generate a curl command example for retrieving webhooks.

        Args:
            order_id: The unique order identifier.

        Returns:
            str: A ready-to-use curl command.

        Example:
            >>> cmd = N8nWebhookTester.get_curl_example("test-order-123")
            >>> print(cmd)
        """
        url = f"{N8nWebhookTester.RETRIEVE_BASE_URL}/{order_id}"
        return (
            f'curl -X GET "{url}" \\\n'
            f'  -u "{N8nWebhookTester.AUTH_USERNAME}:{N8nWebhookTester.AUTH_PASSWORD}"'
        )


# CLI usage example
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Generate order ID:    python n8n_helper.py generate")
        print("  Get send URL:         python n8n_helper.py send <order_id>")
        print("  Retrieve webhooks:    python n8n_helper.py retrieve <order_id>")
        print("  Get curl example:     python n8n_helper.py curl <order_id>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "generate":
        order_id = N8nWebhookTester.generate_order_id()
        print(f"Generated Order ID: {order_id}")
        print(f"Send URL: {N8nWebhookTester.get_send_url(order_id)}")

    elif command == "send" and len(sys.argv) > 2:
        order_id = sys.argv[2]
        print(N8nWebhookTester.get_send_url(order_id))

    elif command == "retrieve" and len(sys.argv) > 2:
        order_id = sys.argv[2]
        try:
            webhooks = N8nWebhookTester.retrieve_webhooks(order_id)
            print(N8nWebhookTester.format_for_report(webhooks))
        except TimeoutError as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif command == "curl" and len(sys.argv) > 2:
        order_id = sys.argv[2]
        print(N8nWebhookTester.get_curl_example(order_id))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
