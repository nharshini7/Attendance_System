import React, { useState } from 'react';

function Attendance() {
  const [attendees, setAttendees] = useState([]);
  const [status, setStatus] = useState('');
  const [count, setCount] = useState(0);

  const handleRecognize = async () => {
    setStatus('Running face recognition...');

    const res = await fetch('http://localhost:5000/recognize');
    const data = await res.json();

    if (data.recognized) {
      setAttendees(data.recognized);
      setCount(data.recognized.length);
      setStatus('Attendance session complete ✅');
    } else {
      setStatus('Face recognition failed ❌');
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto text-center">
      <h1 className="text-2xl font-bold mb-4">Attendance</h1>

      <button
        onClick={handleRecognize}
        className="bg-green-600 text-white px-4 py-2 rounded mb-4"
      >
        Start Recognition
      </button>

      <p className="mb-4 text-blue-500">{status}</p>

      <h2 className="text-xl font-semibold mb-2">Today's Marked Attendance</h2>
      <p className="text-gray-700 mb-4">Total Marked: {count}</p>

      <ul className="text-left bg-white rounded shadow p-4">
        {attendees.map((name, idx) => (
          <li key={idx} className="border-b py-1">{name}</li>
        ))}
      </ul>
    </div>
  );
}

export default Attendance;
