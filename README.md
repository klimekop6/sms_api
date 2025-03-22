# SMS API

A simple REST API service used by the Tribal Wars Bot project to send SMS notifications and alerts.

## Overview

This API connects to an Android phone attached to the server and controls it using ADB (Android Debug Bridge). It leverages the Python `pyairmore` library along with the Airmore app installed on the phone to send SMS messages programmatically.

## Requirements

- Python 3.12+
- Android phone with USB debugging enabled
- Airmore app installed on the phone
- ADB (Android Debug Bridge)

## Installation

```
uv sync
```

### Usage
Run the API server

```
uv run sms_api.py
```

The server will start on port 5001 and provide endpoints for SMS sending.

### API Endpoints
`HEAD /status` - Check if the API is ready  
`POST /send_sms` - Send an SMS message (requires API key authentication)