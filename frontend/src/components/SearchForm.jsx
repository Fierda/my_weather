// import React, { useState } from 'react';
// import PropTypes from 'prop-types'; // ✅ add this

// export default function SearchForm({ onSearch }) {
//   const [city, setCity] = useState('');

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     if (city) onSearch(city);
//   };

//   return (
//     <form onSubmit={handleSubmit} className="flex gap-2">
//       <input
//         type="text"
//         placeholder="Enter city"
//         value={city}
//         onChange={(e) => setCity(e.target.value)}
//         className="border p-2 rounded w-full"
//       />
//       <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
//         Search
//       </button>
//     </form>
//   );
// }

// // ✅ declare prop types
// SearchForm.propTypes = {
//   onSearch: PropTypes.func.isRequired,
// };

import React, { useState } from 'react';
import PropTypes from 'prop-types';

export default function SearchForm({ onSearch }) {
  const [city, setCity] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (city.trim()) onSearch(city.trim());
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <input
        type="text"
        placeholder="Enter city name..."
        value={city}
        onChange={(e) => setCity(e.target.value)}
        className="flex-grow px-4 py-2 rounded-md border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition duration-200"
      />
      <button
        type="submit"
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-semibold shadow transition duration-200"
      >
        Search
      </button>
    </form>
  );
}

SearchForm.propTypes = {
  onSearch: PropTypes.func.isRequired,
};
