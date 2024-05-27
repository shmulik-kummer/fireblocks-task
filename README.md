# Fireblocks Task

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project is designed to interface with the Fireblocks platform, receiving webhook notifications about transactions. When an expense account's balance drops below a specified threshold, the application initiates a top-up transaction from a treasury account to maintain sufficient funds in the expense accounts.

## Features

- Receives Transactional webhook notifications from Fireblocks platform
- Check the balance of the expanse accounts (support multiple accounts)
- Tops up expense accounts from a treasury account if their balance is below the threshold
- Logs all relevant activities for monitoring and debugging.

## Project structure

```
fireblocks-task/
  ├── app.py               # Main application entry point
  ├── config_template.py   # Configuration settings template file
  ├── logging_config.py    # Logging configuration
  ├── requirements.txt     # Python dependencies
  ├── routes.py            # Flask routes
  ├── utils.py             # Utility functions
  └── README.md            # Project documentation
  ```

## Flow
1. **Initialization** - The application starts with app.py, setting up the Flask server. Configuration settings are loaded from _config.py_.
2. **Receiving Webhooks** - The app listen to transactional webhooks events from the Fireblocks platform.
3. **Balance Check** - When a confirmed transaction webhook received, the app check each of the expense account balance.
4. **Top-Up Initiation:** - If expense account balance is below the threshold and the treasury account has enough fund to process, it will initiate a transaction to balance the account.

## Setup

### Prerequisites

- Python 3.6 or higher
- `pip` package manager

### Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/shmulik-kummer/fireblocks-task.git
   cd fireblocks-task

2. **Install the required packages:**

    `pip install -r requirements.txt`

There are two dependencies to be installed:
1. Flask
2. Fireblocks SDK - please click [here](https://developers.fireblocks.com/docs/python-guide) for the Python guide.

## Configuration

The app configuration is stored on a config.py file. after cloning the project, please rename the _config_template.py_ file to _config.py_ and add the following properties:

1. **API_URL** - Use 'https://api.fireblocks.io' for testing environment.
2. **API_KEY**: A secured API key should be provided in each API request. click [here](https://developers.fireblocks.com/docs/quickstart#step-1-generate-a-csr-file) for additional information about API key creation
3. **API_SECRET_PATH**: The key is created as part of the API key creation process. Please provide the file path. uncomment the following line:

     `with open(API_SECRET_PATH, 'r') as file:
       API_SECRET = file.read()`

4. **TREASURY_ACCOUNT_ID** - The treasury account ID
5. **EXPENSE_ACCOUNTS** - The expense account ids (array of id and threshold value objects)
6. **ASSET_ID** = The asset type. for testing purposes use "_AMOY_POLYGON_TEST_"
7. **BALANCE_THRESHOLD** = The expense account balance threshold (balance below will trigger a top-up attempt)

## Usage
1. **Configure Webhook URL** - Set the webhook URL in your Fireblocks dashboard to point to your instance URL. click [here](https://developers.fireblocks.com/docs/webhooks-notifications#configuring-webhook-urls) for detailed information on how to configure webhooks on the Fireblocks platform

* **Important** - Each webhook URL must be a complete, globally available HTTPS address.

2. Run the Flask application
   
    `python app.py`


## Logging
The application uses Python's built-in logging module to log various events. Logs are configured in the _logging_config.py_ file to output to both the console and a file named _app.log_.

