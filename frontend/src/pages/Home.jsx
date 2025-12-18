import { Link } from 'react-router-dom'
import { Upload, TrendingUp, Brain, Zap, Target, Shield } from 'lucide-react'
import './Home.css'

const Home = () => {
    const features = [
        {
            icon: Brain,
            title: 'AI-Powered Predictions',
            description: 'Multi-model ensemble using XGBoost, CatBoost, and neural networks for accurate point predictions.',
            color: 'var(--color-primary)'
        },
        {
            icon: Upload,
            title: 'Screenshot Upload',
            description: 'Simply upload your FPL team screenshot. Our OCR extracts your squad automatically.',
            color: 'var(--color-secondary)'
        },
        {
            icon: TrendingUp,
            title: 'Smart Transfers',
            description: 'Get optimal transfer suggestions that maximize expected points while respecting FPL rules.',
            color: 'var(--color-accent)'
        },
        {
            icon: Target,
            title: 'Captain Picks',
            description: 'Data-driven captain recommendations based on form, fixtures, and expected minutes.',
            color: 'var(--color-info)'
        },
        {
            icon: Zap,
            title: 'Real-time Data',
            description: 'Live FPL API integration ensures predictions are always based on the latest information.',
            color: 'var(--color-warning)'
        },
        {
            icon: Shield,
            title: 'Explainable AI',
            description: 'Understand why each prediction is made with clear explanations and confidence scores.',
            color: 'var(--color-success)'
        },
    ]

    const stats = [
        { value: '65%+', label: 'Ranking Correlation' },
        { value: '95%+', label: 'OCR Accuracy' },
        { value: '70%+', label: 'Transfer ROI' },
        { value: '<2s', label: 'Response Time' },
    ]

    return (
        <div className="home">
            {/* Hero Section */}
            <section className="hero">
                <div className="hero-background">
                    <div className="gradient-orb orb-1"></div>
                    <div className="gradient-orb orb-2"></div>
                    <div className="gradient-orb orb-3"></div>
                </div>

                <div className="container hero-content">
                    <div className="hero-text fade-in">
                        <h1 className="hero-title">
                            Dominate FPL with
                            <span className="gradient-text"> AI-Powered </span>
                            Insights
                        </h1>
                        <p className="hero-subtitle">
                            Upload your team screenshot and get intelligent predictions, optimal transfer suggestions,
                            and data-driven captain picks powered by machine learning.
                        </p>
                        <div className="hero-actions">
                            <Link to="/analyze" className="btn btn-primary btn-lg">
                                <Upload size={20} />
                                Analyze My Team
                            </Link>
                            <Link to="/predictions" className="btn btn-outline btn-lg">
                                <TrendingUp size={20} />
                                View Predictions
                            </Link>
                        </div>
                    </div>

                    <div className="hero-image slide-up">
                        <div className="hero-card glass-strong">
                            <div className="hero-card-header">
                                <Brain size={32} className="hero-card-icon" />
                                <div>
                                    <h3>FPL AI Model</h3>
                                    <p className="text-secondary">Gameweek Predictions</p>
                                </div>
                            </div>
                            <div className="hero-card-stats">
                                <div className="stat-item">
                                    <span className="stat-value gradient-text">8.4</span>
                                    <span className="stat-label">Expected Points</span>
                                </div>
                                <div className="stat-item">
                                    <span className="stat-value" style={{ color: 'var(--color-secondary)' }}>92%</span>
                                    <span className="stat-label">Start Probability</span>
                                </div>
                                <div className="stat-item">
                                    <span className="stat-value" style={{ color: 'var(--color-accent)' }}>High</span>
                                    <span className="stat-label">Confidence</span>
                                </div>
                            </div>
                            <div className="hero-card-footer">
                                <span className="badge badge-success">✓ Optimal Transfer</span>
                                <span className="badge badge-info">Captain Pick</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Stats Section */}
            <section className="stats-section">
                <div className="container">
                    <div className="stats-grid">
                        {stats.map((stat, index) => (
                            <div key={index} className="stat-card card-glass">
                                <div className="stat-card-value gradient-text">{stat.value}</div>
                                <div className="stat-card-label">{stat.label}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="features-section">
                <div className="container">
                    <div className="section-header">
                        <h2 className="section-title">Powerful Features</h2>
                        <p className="section-subtitle">
                            Everything you need to make informed FPL decisions
                        </p>
                    </div>

                    <div className="features-grid">
                        {features.map((feature, index) => (
                            <div key={index} className="feature-card card-glass">
                                <div className="feature-icon" style={{ color: feature.color }}>
                                    <feature.icon size={32} />
                                </div>
                                <h3 className="feature-title">{feature.title}</h3>
                                <p className="feature-description">{feature.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* How It Works Section */}
            <section className="how-it-works">
                <div className="container">
                    <div className="section-header">
                        <h2 className="section-title">How It Works</h2>
                        <p className="section-subtitle">
                            Get AI-powered insights in three simple steps
                        </p>
                    </div>

                    <div className="steps-grid">
                        <div className="step-card card-glass">
                            <div className="step-number gradient-text">1</div>
                            <h3>Upload Screenshot</h3>
                            <p>Take a screenshot of your FPL team and upload it to our platform.</p>
                        </div>

                        <div className="step-card card-glass">
                            <div className="step-number gradient-text">2</div>
                            <h3>AI Analysis</h3>
                            <p>Our ML models analyze your team and predict player performance.</p>
                        </div>

                        <div className="step-card card-glass">
                            <div className="step-number gradient-text">3</div>
                            <h3>Get Insights</h3>
                            <p>Receive transfer suggestions, captain picks, and detailed explanations.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="cta-section">
                <div className="container">
                    <div className="cta-card glass-strong">
                        <h2 className="cta-title">Ready to Boost Your FPL Rank?</h2>
                        <p className="cta-subtitle">
                            Join thousands of managers using AI to make smarter FPL decisions
                        </p>
                        <Link to="/analyze" className="btn btn-primary btn-lg">
                            <Upload size={20} />
                            Start Analyzing Now
                        </Link>
                    </div>
                </div>
            </section>
        </div>
    )
}

export default Home
