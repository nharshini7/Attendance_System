import React, { useState } from 'react';

function Register() {
  const [name, setName] = useState('');
  const [status, setStatus] = useState('');

  const handleRegister = async () => {
    if (!name) return alert("Please enter a name");

    setStatus("Registering...");

    const res = await fetch('http://localhost:5000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name })
    });

    const data = await res.json();
    if (data.success) {
      setStatus("Face registered successfully ✅");
    } else {
      setStatus("Failed to register ❌");
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto text-center">
      <h1 className="text-2xl font-bold mb-4">Register Face</h1>
      <input
        type="text"
        value={name}
        placeholder="Enter your name"
        onChange={e => setName(e.target.value)}
        className="border p-2 rounded w-full mb-4"
      />
      <button
        onClick={handleRegister}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Register
      </button>
      {status && <p className="mt-4 text-green-600">{status}</p>}
    </div>
  );
}

export default Register;
