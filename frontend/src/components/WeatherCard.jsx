// import React, { useState } from 'react';
// import axios from 'axios';
// import SearchForm from './SearchForm.jsx';

// export default function WeatherCard() {
//   const [weather, setWeather] = useState(null);
//   const [error, setError] = useState('');

//   const fetchWeather = async (city) => {
//     try {
//       const res = await axios.get(`/api/weather/${city}`);
//       setWeather(res.data);
//       setError('');
//     } catch (err) {
//       setError(err.response?.data?.detail || 'Error fetching weather.');
//       setWeather(null);
//     }
//   };

//   return (
//     <div className="bg-white p-6 rounded-xl shadow-xl">
//       <SearchForm onSearch={fetchWeather} />
//       {error && <p className="text-red-500 mt-4">{error}</p>}
//       {weather && (
//         <div className="mt-4">
//           <h2 className="text-xl font-bold">{weather.location}</h2>
//           <p className="text-lg">{weather.temperature}°C - {weather.description}</p>
//           <p>Feels like: {weather.feels_like}°C</p>
//           <p>Humidity: {weather.humidity}%</p>
//           <p>Wind: {weather.wind_speed} m/s</p>
//         </div>
//       )}
//     </div>
//   );
// }

import React, { useState } from 'react';
import axios from 'axios';
import SearchForm from './SearchForm.jsx';
import {
  FaTemperatureHigh,
  FaWind,
  FaTint,
  FaMapMarkerAlt,
  FaThermometerHalf
} from 'react-icons/fa';

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
    <div className="min-h-screen bg-gradient-to-br from-blue-400 via-sky-300 to-indigo-400 flex items-center justify-center p-4 font-sans">
      <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-2xl p-6 w-full max-w-md text-gray-800">
        <SearchForm onSearch={fetchWeather} />

        {error && (
          <p className="text-red-600 mt-4 font-semibold bg-red-100 p-2 rounded-md">{error}</p>
        )}

        {weather && (
          <div className="mt-6 space-y-3">
            <h2 className="text-3xl font-bold flex items-center gap-2 text-blue-800">
              <FaMapMarkerAlt className="text-blue-600" />
              {weather.location}
            </h2>

            <p className="text-xl flex items-center gap-2 text-gray-700">
              <FaTemperatureHigh className="text-orange-500" />
              {weather.temperature}°C – {weather.description}
            </p>

            <p className="flex items-center gap-2">
              <FaThermometerHalf className="text-pink-500" />
              <strong>Feels like:</strong> {weather.feels_like}°C
            </p>

            <p className="flex items-center gap-2">
              <FaTint className="text-blue-500" />
              <strong>Humidity:</strong> {weather.humidity}%
            </p>

            <p className="flex items-center gap-2">
              <FaWind className="text-cyan-600" />
              <strong>Wind:</strong> {weather.wind_speed} m/s
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

