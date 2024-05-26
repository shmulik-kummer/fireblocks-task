# Fireblocks Task

This repository contains a Flask-based application that processes webhook events from the Fireblocks platform. The application checks the balance of specified expense accounts and tops them up from a treasury account if their balance falls below a predefined threshold.

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

- Receives webhook notifications from Fireblocks.
- Checks balances of multiple expense accounts.
- Tops up expense accounts from a treasury account if their balance is below the threshold.
- Logs all relevant activities for monitoring and debugging.

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

## Configuration
The app configuration is stored on a config.py file. after cloing the project, please rename the _config_template.py_ file to _config.py_ and add the following properties:

1. **API_URL** - Use 'https://api.fireblocks.io' for testing enviorment.
2. **API_KEY**: A secured API key should be provided in each API request. click here for additional information about API key creation
3. **API_SECRET_PATH**: The key is created as part of the API key process. Please provide the file path. uncomment the following line:

     `with open(API_SECRET_PATH, 'r') as file:
       API_SECRET = file.read()`

4. **TREASURY_ACCOUNT_ID** - The treasury account ID
5. **EXPENSE_ACCOUNT_ID** - The expanse account id
6. **ASSET_ID** = The asset type. for testing purposes use "AMOY_POLYGON_TEST"
7. **BALANCE_THRESHOLD** = The expanse account balance threshold (balance below will trigger a top-up attempt)



