import pytest
import httpx


@pytest.fixture
async def client():
    async with httpx.AsyncClient(timeout=10.0) as client:
        yield client