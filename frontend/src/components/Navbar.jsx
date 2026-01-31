import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Leaf, LogOut, History, User } from 'lucide-react';

const Navbar = () => {
    const { user, logout } = useAuth();
    const location = useLocation();

    const isActive = (path) => location.pathname === path ? "text-green-700 font-bold" : "text-gray-600";

    return (
        <nav className="glass-card" style={{
            margin: '20px',
            padding: '15px 30px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            position: 'sticky',
            top: '20px',
            zIndex: 100
        }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <div style={{
                        background: 'linear-gradient(135deg, #48BB78, #2F855A)',
                        padding: '8px',
                        borderRadius: '10px',
                        color: 'white'
                    }}>
                        <Leaf size={24} />
                    </div>
                    <span style={{ fontSize: '1.5rem', fontWeight: '700', color: '#2F855A' }}>AgriScan</span>
                </Link>
            </div>

            <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
                {user ? (
                    <>
                        <Link to="/" className={isActive('/')}>Predict</Link>
                        <Link to="/history" className={isActive('/history')} style={{ display: 'flex', gap: '5px', alignItems: 'center' }}>
                            History
                        </Link>

                        <div style={{ width: '1px', height: '24px', background: '#CBD5E0' }}></div>

                        <span style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: '500' }}>
                            <User size={18} /> {user.name}
                        </span>

                        <button onClick={logout} className="btn-outline" style={{ padding: '8px 16px', fontSize: '0.9rem', display: 'flex', gap: '8px', alignItems: 'center' }}>
                            <LogOut size={16} /> Logout
                        </button>
                    </>
                ) : (
                    <>
                        <Link to="/login" className="btn btn-outline">Login</Link>
                        <Link to="/register" className="btn btn-primary">Get Started</Link>
                    </>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
