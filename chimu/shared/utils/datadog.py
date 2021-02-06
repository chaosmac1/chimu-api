import datadog
from os import environ


def InitializeDatadog():
    print('Datadog: Initializing...')

    options = {
        "api_key": environ.get("DD_API_KEY"),
        "app_key": environ.get("DD_APP_KEY"),
        "statsd_host": environ.get("DD_STATSD_HOST"),
        "statsd_port": environ.get("DD_STATSD_PORT"),
    }
    datadog.initialize(**options)

    print("Datadog: Announce that we're alive...")

    try:
        title = "API v1 Startup!"
        text = "API v1 instance has just started."
        tags = ["version:1", "application:web"]

        datadog.api.Event.create(title=title, text=text, tags=tags)
        print("Datadog: Done...")
    except datadog.api.exceptions.ApiNotInitialized as e:
        print(f"Datadog: Failed {e}")
        print(f"Datadog: Wrong DD_API_KEY ?")
        print(f"Datadog: Wrong DD_APP_KEY ?")
