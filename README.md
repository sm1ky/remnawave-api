# Remnawave Python SDK

[![Stars](https://img.shields.io/github/stars/sm1ky/remnawave-api.svg?style=social)](https://github.com/sm1ky/remnawave-api/stargazers)
[![Forks](https://img.shields.io/github/forks/sm1ky/remnawave-api.svg?style=social)](https://github.com/sm1ky/remnawave-api/network/members)
[![Issues](https://img.shields.io/github/issues/sm1ky/remnawave-api.svg)](https://github.com/sm1ky/remnawave-api/issues)
[![Supported python versions](https://img.shields.io/pypi/pyversions/remnawave.svg)](https://pypi.python.org/pypi/remnawave)
[![Downloads](https://img.shields.io/pypi/dm/remnawave.svg)](https://pypi.python.org/pypi/remnawave)
[![PyPi Package Version](https://img.shields.io/pypi/v/remnawave)](https://pypi.python.org/pypi/remnawave)
[![Publish Python Package](https://github.com/sm1ky/remnawave-api/actions/workflows/upload.yml/badge.svg?branch=production)](https://github.com/sm1ky/remnawave-api/actions/workflows/upload.yml)

A Python SDK client for interacting with the **[Remnawave API](https://remna.st)**.
This library simplifies working with the API by providing convenient controllers, Pydantic models for requests and responses, and fast serialization with `orjson`. 

## 📦 Installation

### Package (Recommended)
Install the latest version from the new PyPI package:

```bash
pip install remnawave_api
```

### Development Version
If you need the development version:

```bash
pip install git+https://github.com/sm1ky/remnawave-api.git@development
```

---

## 🫥 Compatible versions

| Contract Version | Remnawave Panel Version |
| ---------------- | ----------------------- |
| 2.8.0            | >=2.8.0                 |
| 2.7.1            | >=2.7.0                 |
| 2.6.3            | >=2.6.3                 |
| 2.6.2            | >=2.6.2                 |
| 2.6.1            | >=2.6.0                 |
| 2.4.4            | >=2.4.0                 |
| 2.3.2            | >=2.3.0, <2.4.0         |
| 2.3.0            | >=2.3.0, <2.3.2         |
| 2.2.6            | ==2.2.6                 |
| 2.2.3            | >=2.2.13                |
| 2.1.19           | >=2.1.19, <2.2.0        |
| 2.1.18           | >=2.1.18                |
| 2.1.17           | >=2.1.16, <=2.1.17      |
| 2.1.16           | >=2.1.16                |
| 2.1.13           | >=2.1.13, <=2.1.15      |
| 2.1.9            | >=2.1.9, <=2.1.12       |
| 2.1.8            | ==2.1.8                 |
| 2.1.7.post1      | ==2.1.7                 |
| 2.1.4            | >=2.1.4, <2.1.7         |
| 2.1.1            | >=2.1.1, <2.1.4         |
| 2.0.0            | >=2.0.0,<2.1.0          |
| 1.1.3            | >=1.6.12,<2.0.0         |
| 1.1.2            | >=1.6.3,<=1.6.11        |
| 1.1.1            | 1.6.1, 1.6.2            |
| 1.1.0            | 1.6.0                   |
| 1.0.8            | 1.5.7                   |

### Dependencies
- `orjson` (>=3.10.15, <4.0.0)
- `rapid-api-client` (==0.6.0)
- `httpx` (>=0.27.2, <0.28.0)

## 🚀 Usage

Here’s a quick example to get you started:

```python
import os
import asyncio

from remnawave import RemnawaveSDK  # Updated import for new package
from remnawave.models import (  # Updated import path
    UsersResponseDto, 
    UserResponseDto,
    GetAllConfigProfilesResponseDto,
    CreateInternalSquadRequestDto
)

async def main():
    # URL to your panel (ex. https://vpn.com or http://127.0.0.1:3000)
    base_url: str = os.getenv("REMNAWAVE_BASE_URL")
    # Bearer Token from panel (section: API Tokens) 
    token: str = os.getenv("REMNAWAVE_TOKEN")

    # Initialize the SDK
    remnawave = RemnawaveSDK(base_url=base_url, token=token)

    # Fetch all users
    response: UsersResponseDto = await remnawave.users.get_all_users()
    total_users: int = response.total
    users: list[UserResponseDto] = response.users
    print("Total users: ", total_users)
    print("List of users: ", users)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## ❤️ About

This SDK was originally developed by [@kesevone](https://github.com/kesevone) for integration with Remnawave's API.

Maintained by [@sm1ky](https://github.com/sm1ky) at [`sm1ky/remnawave-api`](https://github.com/sm1ky/remnawave-api).