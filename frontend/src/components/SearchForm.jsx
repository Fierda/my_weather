import React, { useState } from 'react';
import PropTypes from 'prop-types'; // ✅ add this

export default function SearchForm({ onSearch }) {
  const [city, setCity] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (city) onSearch(city);
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        placeholder="Enter city"
        value={city}
        onChange={(e) => setCity(e.target.value)}
        className="border p-2 rounded w-full"
      />
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
        Search
      </button>
    </form>
  );
}

// ✅ declare prop types
SearchForm.propTypes = {
  onSearch: PropTypes.func.isRequired,
};
