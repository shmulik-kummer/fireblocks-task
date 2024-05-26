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
1. **API Key**: follow fireblock docs for instructions on how to generate the API user key.
2. **Private key**: 
3. Environment Variables: Update the config.py file with your specific configuration settings, including the expense account IDs and thresholds.
