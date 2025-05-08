# Remnawave SDK

[![Stars](https://img.shields.io/github/stars/sm1ky/remnawave-api.svg?style=social)](https://github.com/sm1ky/remnawave-api/stargazers)
[![Forks](https://img.shields.io/github/forks/sm1ky/remnawave-api.svg?style=social)](https://github.com/sm1ky/remnawave-api/network/members)
[![Issues](https://img.shields.io/github/issues/sm1ky/remnawave-api.svg)](https://github.com/sm1ky/remnawave-api/issues)
[![Supported python versions](https://img.shields.io/pypi/pyversions/remnawave-api.svg)](https://pypi.python.org/pypi/remnawave-api)
[![Downloads](https://img.shields.io/pypi/dm/remnawave-api.svg)](https://pypi.python.org/pypi/remnawave-api)
[![PyPi Package Version](https://img.shields.io/pypi/v/remnawave-api)](https://pypi.python.org/pypi/remnawave-api)
[![Publish Python Package](https://github.com/sm1ky/remnawave-api/actions/workflows/upload.yml/badge.svg?branch=production)](https://github.com/sm1ky/remnawave-api/actions/workflows/upload.yml)

A Python SDK client for interacting with the **[Remnawave API](https://remna.st)**.
This library simplifies working with the API by providing convenient controllers, Pydantic models for requests and responses, and fast serialization with `orjson`. 
Library checked with Remnawave **[v1.6.0](https://github.com/remnawave/panel/releases/tag/1.6.0)**

## ✨ Key Features

- **Controller-based design**: Split functionality into separate controllers for flexibility. Use only what you need!
- **Pydantic models**: Strongly-typed requests and responses for better reliability.
- **Fast serialization**: Powered by `orjson` for efficient JSON handling.
- **Modular usage**: Import individual controllers or the full SDK as needed.

## 📦 Installation

You can install it directly using `pip`:

```bash
pip install remnawave_api
```

If you need dev version:

```bash
pip install git+https://github.com/sm1ky/remnawave-api.git@development
```

---

### Dependencies
- `orjson` (>=3.10.15, <4.0.0)
- `rapid-api-client` (==0.6.0)
- `httpx` (>=0.27.2, <0.28.0)

## 🚀 Usage

Here’s a quick example to get you started:

```python
import os
import asyncio

from remnawave_api import RemnawaveSDK
from remnawave_api.models import UsersResponseDto, UserResponseDto

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

    # Disable a specific user
    test_uuid: str = "e4d3f3d2-4f4f-4f4f-4f4f-4f4f4f4f4f4f"
    disabled_user: UserResponseDto = await remnawave.users.disable_user(test_uuid)
    print("Disabled user: ", disabled_user)

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

Maintained and extended by [@sm1ky](https://github.com/sm1ky).