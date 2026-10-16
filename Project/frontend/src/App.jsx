import React, { useEffect, useState } from 'react';

export default function App() {
  const [assets, setAssets] = useState([]);
  const [form, setForm] = useState({ name: '', category: 'Laptop', serial_number: '' });

  const fetchAssets = async () => {
    const res = await fetch('/api/assets');
    if (res.ok) setAssets(await res.json());
  };

  useEffect(() => { fetchAssets(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await fetch('/api/assets', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });
    setForm({ name: '', category: 'Laptop', serial_number: '' });
    fetchAssets();
  };

  const toggleStatus = async (asset) => {
    const nextStatus = asset.status === 'Available' ? 'Assigned' : 'Available';
    await fetch(`/api/assets/${asset.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: nextStatus }),
    });
    fetchAssets();
  };

  const removeAsset = async (id) => {
    await fetch(`/api/assets/${id}`, { method: 'DELETE' });
    fetchAssets();
  };

  return (
    <div style={{ maxWidth: '800px', margin: '40px auto', padding: '20px' }}>
      <h1>EquipTrack Hardware Inventory</h1>
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px', marginBottom: '24px' }}>
        <input
          placeholder="Device Name (e.g. MacBook Pro)"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          required
          style={{ padding: '8px', flex: 1 }}
        />
        <input
          placeholder="Serial Number (e.g. SN-901)"
          value={form.serial_number}
          onChange={(e) => setForm({ ...form, serial_number: e.target.value })}
          required
          style={{ padding: '8px', flex: 1 }}
        />
        <button type="submit" style={{ padding: '8px 16px', background: '#3b82f6', color: '#fff', border: 'none', cursor: 'pointer' }}>
          Add Asset
        </button>
      </form>

      <table style={{ width: '100%', borderCollapse: 'collapse', background: '#1e293b' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #334155', textAlign: 'left' }}>
            <th style={{ padding: '12px' }}>Name</th>
            <th style={{ padding: '12px' }}>Serial</th>
            <th style={{ padding: '12px' }}>Status</th>
            <th style={{ padding: '12px' }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {assets.map((a) => (
            <tr key={a.id} style={{ borderBottom: '1px solid #334155' }}>
              <td style={{ padding: '12px' }}>{a.name}</td>
              <td style={{ padding: '12px' }}>{a.serial_number}</td>
              <td style={{ padding: '12px' }}>{a.status}</td>
              <td style={{ padding: '12px', display: 'flex', gap: '8px' }}>
                <button onClick={() => toggleStatus(a)}>Toggle Status</button>
                <button onClick={() => removeAsset(a.id)} style={{ color: '#ef4444' }}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}