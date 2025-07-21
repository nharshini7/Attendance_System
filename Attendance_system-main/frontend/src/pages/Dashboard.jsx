import React, { useEffect, useState } from 'react';

function Dashboard() {
  const [registeredCount, setRegisteredCount] = useState(0);
  const [todayMarked, setTodayMarked] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSummary();
    fetchRegistered();
  }, []);

  const fetchSummary = async () => {
    try {
      const res = await fetch('http://localhost:5000/summary');
      const data = await res.json();
      setTodayMarked(data.names || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchRegistered = async () => {
    try {
      const res = await fetch('http://localhost:5000/summary');
      const data = await res.json();
      const count = data?.totalRegistered || 0;
      setRegisteredCount(count);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDownload = () => {
    const today = new Date().toISOString().split('T')[0];
    window.open(`http://localhost:5000/download?date=${today}`, '_blank');
  };

  return (
    <div className="p-6 max-w-xl mx-auto text-center">
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>

      {loading ? (
        <p className="text-blue-500">Loading summary...</p>
      ) : (
        <>
          <div className="text-left bg-white rounded shadow p-4 mb-4">
            <p><strong>✅ Marked Today:</strong> {todayMarked.length}</p>
            <p><strong>👥 Registered People:</strong> Unknown (optional)</p>
          </div>

          <h2 className="text-xl font-semibold mb-2">Marked Today:</h2>
          <ul className="text-left bg-white rounded shadow p-4 mb-4 max-h-40 overflow-y-auto">
            {todayMarked.map((name, i) => (
              <li key={i} className="border-b py-1">{name}</li>
            ))}
          </ul>

          <button
            onClick={handleDownload}
            className="bg-purple-600 text-white px-4 py-2 rounded"
          >
            📥 Download Today’s CSV
          </button>
        </>
      )}
    </div>
  );
}

export default Dashboard;
