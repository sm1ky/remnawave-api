# Remnawave Python SDK

> **📢 Repository Migration Notice**
> 
> This repository has been moved from [`sm1ky/remnawave-api`](https://github.com/sm1ky/remnawave-api) to [`remnawave/python-sdk`](https://github.com/remnawave/python-sdk).
> 
> **PyPI Package Migration:**
> - **Legacy versions (≤1.x)**: Available at [`remnawave_api`](https://pypi.org/project/remnawave_api/) *(deprecated)*
> - **New versions (≥2.x)**: Available at [`remnawave`](https://pypi.org/project/remnawave/)
> 
> Please update your dependencies to use the new package name for future updates.

[![Stars](https://img.shields.io/github/stars/remnawave/python-sdk.svg?style=social)](https://github.com/remnawave/python-sdk/stargazers)
[![Forks](https://img.shields.io/github/forks/remnawave/python-sdk.svg?style=social)](https://github.com/remnawave/python-sdk/network/members)
[![Issues](https://img.shields.io/github/issues/remnawave/python-sdk.svg)](https://github.com/remnawave/python-sdk/issues)
[![Supported python versions](https://img.shields.io/pypi/pyversions/remnawave.svg)](https://pypi.python.org/pypi/remnawave)
[![Downloads](https://img.shields.io/pypi/dm/remnawave.svg)](https://pypi.python.org/pypi/remnawave)
[![PyPi Package Version](https://img.shields.io/pypi/v/remnawave)](https://pypi.python.org/pypi/remnawave)
[![Publish Python Package](https://github.com/remnawave/python-sdk/actions/workflows/upload.yml/badge.svg?branch=production)](https://github.com/remnawave/python-sdk/actions/workflows/upload.yml)

A Python SDK client for interacting with the **[Remnawave API](https://remna.st)**.
This library simplifies working with the API by providing convenient controllers, Pydantic models for requests and responses, and fast serialization with `orjson`. 

**🎉 Version 2.0.0** brings full compatibility with the latest Remnawave backend API, including new endpoints, improved response wrappers, and enhanced type safety.

## ✨ Key Features

- **Full v2.0.0 API compatibility**: Updated for latest Remnawave backend features
- **New controllers**: ConfigProfiles, InternalSquads, InfraBilling, NodesUsageHistory
- **Enhanced models**: OpenAPI-compliant response wrappers with improved field mappings
- **Controller-based design**: Split functionality into separate controllers for flexibility. Use only what you need!
- **Pydantic models**: Strongly-typed requests and responses for better reliability.
- **Fast serialization**: Powered by `orjson` for efficient JSON handling.
- **Modular usage**: Import individual controllers or the full SDK as needed.
- **Backward compatibility**: Legacy aliases maintained for smooth migration.

## 📦 Installation

### New Package (Recommended)
Install the latest version from the new PyPI package:

```bash
pip install remnawave
```

### Legacy Package (Deprecated)
If you need older versions (≤1.x), use the legacy package:

```bash
pip install remnawave_api  # Deprecated - use 'remnawave' instead
```

### Development Version
If you need the development version:

```bash
pip install git+https://github.com/remnawave/python-sdk.git@development
```

---

## 🫥 Compatible versions

| Contract Version | Remnawave Panel Version |
| ---------------- | ----------------------- |
| 2.0.0            | >=2.0.0                 |
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
    response: UsersResponseDto = await remnawave.users.get_all_users_v2()
    total_users: int = response.total
    users: list[UserResponseDto] = response.users
    print("Total users: ", total_users)
    print("List of users: ", users)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🧪 Running Tests

To run the test suite, use Poetry:

```bash
poetry run pytest
```

## ❤️ About

This SDK was originally developed by [@kesevone](https://github.com/kesevone) for integration with Remnawave's API.

Previously maintained by [@sm1ky](https://github.com/sm1ky) at [`sm1ky/remnawave-api`](https://github.com/sm1ky/remnawave-api).

Now officially maintained by the Remnawave Community at [`remnawave/python-sdk`](https://github.com/remnawave/python-sdk).