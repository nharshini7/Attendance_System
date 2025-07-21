import React from 'react';
import { Link } from 'react-router-dom';

function App() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-blue-300 text-white px-4">
      <div className="max-w-xl text-center space-y-8">
        <h1 className="text-4xl md:text-5xl font-bold leading-tight">
          Smart Face Recognition Attendance Portal
        </h1>
        <p className="text-lg md:text-xl text-white/90">
          Automate attendance using face detection, secure recognition, and insightful tracking.
        </p>

        <div className="flex flex-col gap-4 mt-8">
          <Link
            to="/register"
            className="bg-white text-indigo-700 font-semibold py-3 rounded shadow hover:bg-gray-100 transition duration-300"
          >
            👤 Register New Face
          </Link>

          <Link
            to="/attendance"
            className="bg-white text-green-700 font-semibold py-3 rounded shadow hover:bg-gray-100 transition duration-300"
          >
            ✅ Start Attendance
          </Link>

          <Link
            to="/dashboard"
            className="bg-white text-purple-700 font-semibold py-3 rounded shadow hover:bg-gray-100 transition duration-300"
          >
            📊 View Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}

export default App;
