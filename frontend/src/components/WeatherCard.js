import React, { useState } from 'react';
import axios from 'axios';
import SearchForm from './SearchForm';

export default function WeatherCard() {
  const [weather, setWeather] = useState(null);
  const [error, setError] = useState('');

  const fetchWeather = async (city) => {
    try {
      const res = await axios.get(`/api/weather/${city}`);
      setWeather(res.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Error fetching weather.');
      setWeather(null);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-xl">
      <SearchForm onSearch={fetchWeather} />
      {error && <p className="text-red-500 mt-4">{error}</p>}
      {weather && (
        <div className="mt-4">
          <h2 className="text-xl font-bold">{weather.location}</h2>
          <p className="text-lg">{weather.temperature}°C - {weather.description}</p>
          <p>Feels like: {weather.feels_like}°C</p>
          <p>Humidity: {weather.humidity}%</p>
          <p>Wind: {weather.wind_speed} m/s</p>
        </div>
      )}
    </div>
  );
}