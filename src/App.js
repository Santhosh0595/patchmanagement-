import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [systems, setSystems] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [search, setSearch] = useState("");
  const [osFilter, setOsFilter] = useState("All");
  const [selectedSystem, setSelectedSystem] = useState(null);
  const [software, setSoftware] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/systems")
      .then(res => {
        setSystems(res.data);
        setFiltered(res.data);
      });
  }, []);

  useEffect(() => {
    let data = systems;

    if (search) {
      data = data.filter(s =>
        s.hostname.toLowerCase().includes(search.toLowerCase()) ||
        s.ip_address.includes(search)
      );
    }

    if (osFilter !== "All") {
      data = data.filter(s => s.os === osFilter);
    }

    setFiltered(data);
  }, [search, osFilter, systems]);

  const fetchSoftware = (systemId) => {
    axios.get(`http://localhost:8000/software/${systemId}`)
      .then(res => setSoftware(res.data));
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h2 style={{ textAlign: 'center' }}>🖥️ Patch Management Dashboard</h2>

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="🔍 Search by hostname/IP"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ flex: 1, padding: '8px' }}
        />
        <select value={osFilter} onChange={(e) => setOsFilter(e.target.value)} style={{ padding: '8px' }}>
          <option>All</option>
          <option>Windows</option>
          <option>Linux</option>
          <option>Darwin</option>
        </select>
      </div>

      <table style={{ width: '100%', borderCollapse: 'collapse', boxShadow: '0 0 10px rgba(0,0,0,0.1)' }}>
        <thead style={{ backgroundColor: '#343a40', color: 'white' }}>
          <tr>
            <th style={th}>Hostname</th>
            <th style={th}>OS</th>
            <th style={th}>CPU</th>
            <th style={th}>RAM</th>
            <th style={th}>IP</th>
            <th style={th}>Last Seen</th>
            <th style={th}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(sys => (
            <tr key={sys.id} style={{ backgroundColor: '#f8f9fa', textAlign: 'center' }}>
              <td style={td}>{sys.hostname}</td>
              <td style={td}>{sys.os}</td>
              <td style={td}>{sys.cpu}</td>
              <td style={td}>{sys.ram}</td>
              <td style={td}>{sys.ip_address}</td>
              <td style={td}>{new Date(sys.last_seen).toLocaleString()}</td>
              <td style={td}>
                <button onClick={() => {
                  setSelectedSystem(sys);
                  fetchSoftware(sys.id);
                }}>
                  View Software
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Software Modal */}
      {selectedSystem && (
        <div style={{
          position: 'fixed', top: 0, left: 0, width: '100%',
          height: '100%', background: 'rgba(0,0,0,0.6)',
          display: 'flex', justifyContent: 'center', alignItems: 'center'
        }}>
          <div style={{
            background: 'white', padding: '2rem', width: '60%',
            maxHeight: '80%', overflowY: 'auto', borderRadius: '8px'
          }}>
            <h3>🔍 Installed Software - {selectedSystem.hostname}</h3>
            <table style={{ width: '100%', marginTop: '1rem' }}>
              <thead>
                <tr>
                  <th style={th}>Name</th>
                  <th style={th}>Version</th>
                  <th style={th}>Installed On</th>
                </tr>
              </thead>
              <tbody>
                {software.map((sw, index) => (
                  <tr key={index}>
                    <td style={td}>{sw.name}</td>
                    <td style={td}>{sw.version}</td>
                    <td style={td}>{sw.installed_on}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <button onClick={() => {
              setSelectedSystem(null);
              setSoftware([]);
            }} style={{ marginTop: '1rem' }}>
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

const th = { padding: '10px', borderBottom: '1px solid #ccc' };
const td = { padding: '10px', borderBottom: '1px solid #eee' };

export default App;
