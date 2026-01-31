import { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import DragDrop from '../components/DragDrop';
import { Loader2, CheckCircle, AlertTriangle, CloudSun, Leaf, TrendingUp, Calendar, Zap, Shield, Activity } from 'lucide-react';

const Home = () => {
    const { user } = useAuth();
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [date, setDate] = useState(new Date());

    useEffect(() => {
        const timer = setInterval(() => setDate(new Date()), 60000);
        return () => clearInterval(timer);
    }, []);

    const handlePredict = async () => {
        if (!file) return;

        setLoading(true);
        setError(null);
        setResult(null);

        const formData = new FormData();
        formData.append("image", file);

        try {
            const token = localStorage.getItem("token");
            const res = await axios.post(`${import.meta.env.VITE_API_URL}/api/predict`, formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                    "Authorization": `Bearer ${token}`
                }
            });
            setResult(res.data);
        } catch (err) {
            setError(err.response?.data?.message || "Prediction failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container" style={{ padding: '40px 20px', maxWidth: '1000px' }}>

            {/* Header Section */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '40px' }}>
                <div>
                    <h1 style={{ fontSize: '2.5rem', marginBottom: '5px', color: '#2F855A' }}>
                        Welcome back, {user?.name?.split(' ')[0] || 'Farmer'}!
                    </h1>
                    <p style={{ color: '#718096', fontSize: '1.1rem' }}>
                        <Calendar size={18} style={{ display: 'inline', marginRight: '8px' }} />
                        {date.toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
                    </p>
                </div>
                <div className="glass-card" style={{ padding: '10px 20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <CloudSun color="#ECC94B" size={24} />
                    <div>
                        <div style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>26°C</div>
                        <div style={{ fontSize: '0.8rem', color: '#718096' }}>Partly Cloudy</div>
                    </div>
                </div>
            </div>

            {/* Main Action Area */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '30px', marginBottom: '50px' }}>

                {/* Left Column: Upload */}
                <div style={{ gridColumn: result ? 'span 1' : 'span 2' }}>
                    <div className="glass-card" style={{ padding: '30px' }}>
                        <h2 style={{ fontSize: '1.5rem', marginBottom: '20px', color: '#2D3748' }}>Scan Your Crop</h2>
                        <DragDrop onFileSelect={setFile} />

                        {file && !loading && !result && (
                            <div style={{ textAlign: 'center', marginTop: '30px' }}>
                                <button onClick={handlePredict} className="btn btn-primary" style={{ width: '100%', fontSize: '1.2rem', padding: '15px' }}>
                                    Analyze Leaf
                                </button>
                            </div>
                        )}

                        {loading && (
                            <div style={{ textAlign: 'center', marginTop: '40px' }}>
                                <Loader2 className="animate-spin" size={48} style={{ color: '#48BB78', margin: '0 auto' }} />
                                <p style={{ marginTop: '15px', color: '#718096' }}>Consulting AI Agronomist...</p>
                            </div>
                        )}

                        {error && (
                            <div style={{ marginTop: '20px', padding: '15px', background: '#FFF5F5', color: '#C53030', borderRadius: '10px', display: 'flex', gap: '10px', alignItems: 'center' }}>
                                <AlertTriangle size={20} />
                                <div>{error}</div>
                            </div>
                        )}
                    </div>
                </div>

                {/* Right Column: Result (if exists) or Info */}
                {result && (
                    <div className="glass-card animate-fade-in" style={{ padding: '30px', textAlign: 'center', borderLeft: `6px solid ${result.status === 'success' ? '#48BB78' : '#F56565'}` }}>
                        <h2 style={{ color: '#2D3748', marginBottom: '20px' }}>Diagnosis Report</h2>

                        <div style={{ margin: '30px 0' }}>
                            {result.status === 'success' ? (
                                <CheckCircle size={64} style={{ color: '#48BB78', margin: '0 auto 15px' }} />
                            ) : (
                                <AlertTriangle size={64} style={{ color: '#F56565', margin: '0 auto 15px' }} />
                            )}

                            <h3 style={{ fontSize: '2rem', margin: '10px 0', color: '#2D3748', lineHeight: '1.2' }}>
                                {result.prediction.replace(/_/g, ' ')}
                            </h3>

                            <div style={{ display: 'inline-block', padding: '5px 15px', borderRadius: '20px', background: result.status === 'success' ? '#F0FFF4' : '#FFF5F5', color: result.status === 'success' ? '#2F855A' : '#C53030', fontWeight: 'bold' }}>
                                Confidence: {result.confidence}%
                            </div>
                        </div>

                        {result.status !== 'success' && (
                            <div style={{ textAlign: 'left', background: '#FFF', padding: '15px', borderRadius: '10px', marginBottom: '20px' }}>
                                <h4 style={{ margin: '0 0 10px 0', display: 'flex', alignItems: 'center', gap: '5px' }}>
                                    <Leaf size={16} /> Recommended Action:
                                </h4>
                                <p style={{ fontSize: '0.9rem', color: '#4A5568', margin: 0 }}>
                                    Isolate the affected plant immediately. Check for pests on the underside of leaves. Apply appropriate organic fungicide or neem oil as needed.
                                </p>
                            </div>
                        )}

                        <button onClick={() => { setFile(null); setResult(null); }} className="btn btn-outline" style={{ width: '100%' }}>
                            Scan Another Plant
                        </button>
                    </div>
                )}
            </div>

            {/* Dashboard Widgets */}
            <h3 style={{ color: '#4A5568', marginBottom: '20px', fontSize: '1.3rem' }}>Farming Insights</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>

                {/* Market Prices */}
                <div className="glass-card" style={{ padding: '20px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '15px' }}>
                        <h4 style={{ margin: 0, color: '#2D3748' }}>Market Prices</h4>
                        <TrendingUp size={20} color="#48BB78" />
                    </div>
                    <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                        <PriceItem name="Tomato" price="$1.20/kg" change="+5%" />
                        <PriceItem name="Potato" price="$0.80/kg" change="-2%" />
                        <PriceItem name="Corn" price="$1.50/kg" change="+1.2%" />
                    </ul>
                </div>

                {/* Farming Tip */}
                <div className="glass-card" style={{ padding: '20px', background: 'linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(240,255,244,0.9) 100%)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '15px' }}>
                        <h4 style={{ margin: 0, color: '#2D3748' }}>Daily Tip</h4>
                        <Leaf size={20} color="#38B2AC" />
                    </div>
                    <p style={{ fontSize: '0.95rem', color: '#4A5568', lineHeight: '1.5' }}>
                        <strong>Crop Rotation:</strong> Rotating corn with legumes helps replenish nitrogen in the soil naturally, reducing fertilizer costs.
                    </p>
                </div>

                {/* App Stats */}
                <div className="glass-card" style={{ padding: '20px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '15px' }}>
                        <h4 style={{ margin: 0, color: '#2D3748' }}>System Status</h4>
                        <Activity size={20} color="#4299E1" />
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                        <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#48BB78' }}></div>
                        <span style={{ fontSize: '0.9rem', color: '#4A5568' }}>AI Model: Useable</span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#48BB78' }}></div>
                        <span style={{ fontSize: '0.9rem', color: '#4A5568' }}>Database: Connected</span>
                    </div>
                </div>

            </div>
        </div>
    );
};

// Sub-component for Price List
const PriceItem = ({ name, price, change }) => (
    <li style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #E2E8F0', padding: '10px 0' }}>
        <span style={{ fontWeight: '500', color: '#4A5568' }}>{name}</span>
        <div style={{ textAlign: 'right' }}>
            <div style={{ fontWeight: 'bold', color: '#2D3748' }}>{price}</div>
            <div style={{ fontSize: '0.8rem', color: change.startsWith('+') ? '#48BB78' : '#F56565' }}>{change}</div>
        </div>
    </li>
);

export default Home;
