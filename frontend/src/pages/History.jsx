import { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { Trash2, Calendar } from 'lucide-react';

const History = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    const handleDelete = async (id) => {
        if (!confirm("Are you sure you want to delete this record?")) return;

        try {
            const token = localStorage.getItem("token");
            await axios.delete(`http://localhost:5000/api/history/${id}`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setHistory(history.filter(item => item.id !== id));
        } catch (error) {
            console.error("Failed to delete item", error);
            alert("Failed to delete item");
        }
    };

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const token = localStorage.getItem("token");
                const res = await axios.get("http://localhost:5000/api/history", {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setHistory(res.data);
            } catch (error) {
                console.error("Failed to fetch history", error);
            } finally {
                setLoading(false);
            }
        };
        fetchHistory();
    }, []);

    return (
        <div className="container" style={{ padding: '40px 20px' }}>
            <h1 style={{ fontSize: '2rem', marginBottom: '30px', color: '#2F855A', display: 'flex', alignItems: 'center', gap: '15px' }}>
                <Calendar /> Prediction History
            </h1>

            {loading ? (
                <p>Loading history...</p>
            ) : history.length === 0 ? (
                <div className="glass-card" style={{ padding: '40px', textAlign: 'center', color: '#718096' }}>
                    <p>No history found. Start analyzing leaves!</p>
                </div>
            ) : (
                <div className="glass-card" style={{ overflow: 'hidden' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead style={{ background: 'rgba(72, 187, 120, 0.1)' }}>
                            <tr>
                                <th style={{ padding: '15px', textAlign: 'left', color: '#2F855A' }}>Date</th>
                                <th style={{ padding: '15px', textAlign: 'left', color: '#2F855A' }}>Image</th>
                                <th style={{ padding: '15px', textAlign: 'left', color: '#2F855A' }}>Prediction</th>
                                <th style={{ padding: '15px', textAlign: 'left', color: '#2F855A' }}>Confidence</th>
                                <th style={{ padding: '15px', textAlign: 'left', color: '#2F855A' }}>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.map((item) => (
                                <tr key={item.id} style={{ borderBottom: '1px solid rgba(0,0,0,0.05)' }}>
                                    <td style={{ padding: '15px', color: '#4A5568' }}>
                                        {new Date(item.created_at).toLocaleDateString()}
                                    </td>
                                    <td style={{ padding: '15px' }}>
                                        <img
                                            src={`http://localhost:5000/uploads/${item.image_path}`}
                                            alt="Thumbnail"
                                            style={{ width: '50px', height: '50px', objectFit: 'cover', borderRadius: '8px' }}
                                        />
                                    </td>
                                    <td style={{ padding: '15px', fontWeight: '500', color: '#2D3748' }}>{item.prediction}</td>
                                    <td style={{ padding: '15px', color: '#4A5568' }}>
                                        <span style={{
                                            padding: '4px 8px',
                                            background: item.confidence > 80 ? '#C6F6D5' : '#FED7D7',
                                            color: item.confidence > 80 ? '#22543D' : '#822727',
                                            borderRadius: '12px',
                                            fontSize: '0.85rem'
                                        }}>
                                            {item.confidence.toFixed(1)}%
                                        </span>
                                    </td>
                                    <td style={{ padding: '15px' }}>
                                        <button
                                            onClick={() => handleDelete(item.id)}
                                            style={{
                                                background: 'none',
                                                border: 'none',
                                                color: '#E53E3E',
                                                cursor: 'pointer',
                                                padding: '5px',
                                                borderRadius: '4px',
                                                transition: 'background 0.2s'
                                            }}
                                            onMouseEnter={(e) => e.target.style.background = '#FED7D7'}
                                            onMouseLeave={(e) => e.target.style.background = 'none'}
                                        >
                                            <Trash2 size={18} />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default History;
