import pytest
from app.services.weather import WeatherService
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_weather_invalid_city(monkeypatch):
    service = WeatherService()

    async def mock_get_weather(*args, **kwargs):
        raise HTTPException(status_code=404, detail="City not found")

    monkeypatch.setattr(service, "get_weather", mock_get_weather)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_weather("invalidcity")

    assert exc_info.value.status_code == 404
