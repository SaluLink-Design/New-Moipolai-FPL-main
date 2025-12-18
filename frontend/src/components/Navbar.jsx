import { Link, useLocation } from 'react-router-dom'
import { Brain, TrendingUp, Users, History, Menu, X } from 'lucide-react'
import { useState } from 'react'
import './Navbar.css'

const Navbar = () => {
    const location = useLocation()
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

    const navItems = [
        { path: '/', label: 'Home', icon: Brain },
        { path: '/analyze', label: 'Analyze', icon: Users },
        { path: '/predictions', label: 'Predictions', icon: TrendingUp },
        { path: '/transfers', label: 'Transfers', icon: TrendingUp },
        { path: '/history', label: 'History', icon: History },
    ]

    return (
        <nav className="navbar glass-strong">
            <div className="container navbar-container">
                <Link to="/" className="navbar-brand">
                    <Brain className="brand-icon" size={32} />
                    <span className="brand-text gradient-text">FPL AI</span>
                </Link>

                <div className={`navbar-menu ${mobileMenuOpen ? 'active' : ''}`}>
                    {navItems.map(({ path, label, icon: Icon }) => (
                        <Link
                            key={path}
                            to={path}
                            className={`navbar-link ${location.pathname === path ? 'active' : ''}`}
                            onClick={() => setMobileMenuOpen(false)}
                        >
                            <Icon size={18} />
                            <span>{label}</span>
                        </Link>
                    ))}
                </div>

                <button
                    className="navbar-toggle"
                    onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                    aria-label="Toggle menu"
                >
                    {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
                </button>
            </div>
        </nav>
    )
}

export default Navbar
