import { useState } from 'react'
import { Upload, Loader } from 'lucide-react'
import { apiService } from '../services/api'
import './TeamAnalysis.css'

const TeamAnalysis = () => {
    const [selectedFile, setSelectedFile] = useState(null)
    const [preview, setPreview] = useState(null)
    const [loading, setLoading] = useState(false)
    const [analysis, setAnalysis] = useState(null)
    const [error, setError] = useState(null)

    const handleFileSelect = (e) => {
        const file = e.target.files[0]
        if (file) {
            setSelectedFile(file)
            const reader = new FileReader()
            reader.onloadend = () => {
                setPreview(reader.result)
            }
            reader.readAsDataURL(file)
            setError(null)
            setAnalysis(null)
        }
    }

    const handleAnalyze = async () => {
        if (!selectedFile) return

        setLoading(true)
        setError(null)

        try {
            const formData = new FormData()
            formData.append('file', selectedFile)

            const { data: ocrData } = await apiService.uploadTeamImage(formData)

            if (!ocrData.success || ocrData.matched_players.length < 15) {
                setError('Could not detect all players. Please try a clearer screenshot.')
                setLoading(false)
                return
            }

            const playerIds = ocrData.matched_players.map(p => p.id)

            const { data: analysisData } = await apiService.getTeamAnalysis({
                players: playerIds,
                free_transfers: 1,
                bank: 0.0
            })

            setAnalysis(analysisData)

        } catch (err) {
            console.error('Error analyzing team:', err)

            // Better error messages
            let errorMessage = 'Failed to analyze team. Please try again.'

            if (err.code === 'ECONNABORTED') {
                errorMessage = 'Request timed out. The server is taking longer than expected. Please try again in a moment.'
            } else if (err.response?.status === 400) {
                errorMessage = err.response?.data?.detail || 'Invalid team data. Please check your screenshot and try again.'
            } else if (err.response?.status === 500) {
                errorMessage = 'Server error. Please try again later.'
            } else if (err.message === 'Network Error') {
                errorMessage = 'Network error. Please check your connection and try again.'
            } else if (err.response?.data?.detail) {
                errorMessage = err.response.data.detail
            }

            setError(errorMessage)
        } finally {
            setLoading(false)
        }
    }

    const handleDemoAnalysis = async () => {
        setLoading(true)
        setError(null)

        try {
            const demoPlayerIds = [
                352, 333, 141, 308, 5,
                254, 405, 88, 427, 306, 14,
                286, 328, 251, 195
            ]

            const { data: analysisData } = await apiService.getTeamAnalysis({
                players: demoPlayerIds,
                free_transfers: 1,
                bank: 0.5
            })

            setAnalysis(analysisData)

        } catch (err) {
            console.error('Error analyzing demo team:', err)

            // Better error messages
            let errorMessage = 'Failed to analyze team. Please try again.'

            if (err.code === 'ECONNABORTED') {
                errorMessage = 'Request timed out. The server is taking longer than expected. Please try again in a moment.'
            } else if (err.response?.status === 400) {
                errorMessage = err.response?.data?.detail || 'Invalid team data.'
            } else if (err.response?.status === 500) {
                errorMessage = 'Server error. Please try again later.'
            } else if (err.message === 'Network Error') {
                errorMessage = 'Network error. Please check your connection and try again.'
            } else if (err.response?.data?.detail) {
                errorMessage = err.response.data.detail
            }

            setError(errorMessage)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="team-analysis">
            <div className="container">
                <div className="page-header">
                    <h1>Analyze Your Team</h1>
                    <p className="text-secondary">
                        Upload a screenshot of your FPL team to get AI-powered insights
                    </p>
                    <button
                        className="btn btn-outline"
                        onClick={handleDemoAnalysis}
                        disabled={loading}
                        style={{ marginTop: '1rem' }}
                    >
                        {loading ? 'Analyzing...' : 'Try Demo Analysis'}
                    </button>
                </div>

                <div className="upload-section">
                    <div className="upload-card card-glass">
                        <input
                            type="file"
                            id="file-upload"
                            accept="image/*"
                            onChange={handleFileSelect}
                            style={{ display: 'none' }}
                        />

                        {!preview ? (
                            <label htmlFor="file-upload" className="upload-area">
                                <Upload size={48} className="upload-icon" />
                                <h3>Upload Team Screenshot</h3>
                                <p className="text-secondary">
                                    Click to browse or drag and drop your FPL team image
                                </p>
                                <span className="badge badge-info">PNG, JPG up to 10MB</span>
                            </label>
                        ) : (
                            <div className="preview-area">
                                <img src={preview} alt="Team preview" className="preview-image" />
                                <div className="preview-actions">
                                    <button className="btn btn-primary" onClick={handleAnalyze} disabled={loading}>
                                        {loading ? (
                                            <>
                                                <Loader size={16} className="spinner" />
                                                Analyzing...
                                            </>
                                        ) : (
                                            'Analyze Team'
                                        )}
                                    </button>
                                    <button
                                        className="btn btn-outline"
                                        onClick={() => {
                                            setPreview(null)
                                            setSelectedFile(null)
                                            setAnalysis(null)
                                            setError(null)
                                        }}
                                        disabled={loading}
                                    >
                                        Change Image
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>

                    {error && <div className="alert alert-error">{error}</div>}
                </div>

                {analysis && (
                    <div className="analysis-results">
                        <div className="results-header">
                            <h2>Team Analysis Results</h2>
                        </div>

                        <div className="stats-grid">
                            <div className="stat-card card">
                                <h3>Team Value</h3>
                                <p className="stat-value">£{analysis.team_value}m</p>
                            </div>
                            <div className="stat-card card">
                                <h3>Predicted Points</h3>
                                <p className="stat-value">{analysis.predicted_gameweek_points}</p>
                            </div>
                            <div className="stat-card card">
                                <h3>Bench Points</h3>
                                <p className="stat-value">{analysis.predicted_bench_points}</p>
                            </div>
                            <div className="stat-card card">
                                <h3>Free Transfers</h3>
                                <p className="stat-value">{analysis.free_transfers}</p>
                            </div>
                        </div>

                        <div className="suggestions-section">
                            <div className="card">
                                <h3>Captain Suggestion</h3>
                                {analysis.captain_suggestion && (
                                    <div className="captain-card">
                                        <div className="player-info">
                                            <span className="player-name">{analysis.captain_suggestion.player_name}</span>
                                            <span className="player-position">{analysis.captain_suggestion.position}</span>
                                        </div>
                                        <div className="prediction-info">
                                            <span className="expected-points">{analysis.captain_suggestion.expected_points} pts</span>
                                        </div>
                                    </div>
                                )}
                            </div>

                            <div className="card">
                                <h3>Transfer Suggestions</h3>
                                {analysis.transfer_suggestions && analysis.transfer_suggestions.length > 0 ? (
                                    <div className="transfers-list">
                                        {analysis.transfer_suggestions.map((transfer, index) => (
                                            <div key={index} className="transfer-card">
                                                <div className="transfer-details">
                                                    <div className="transfer-out">
                                                        <span className="label">Out:</span>
                                                        <span className="player-name">{transfer.player_out_name}</span>
                                                    </div>
                                                    <div className="transfer-in">
                                                        <span className="label">In:</span>
                                                        <span className="player-name">{transfer.player_in_name}</span>
                                                    </div>
                                                </div>
                                                <div className="transfer-stats">
                                                    <span className="badge badge-success">+{transfer.expected_points_gain} pts</span>
                                                    <span className="badge badge-info">{transfer.risk_level} risk</span>
                                                    {transfer.net_cost_change !== 0 && (
                                                        <span className={`badge ${transfer.net_cost_change > 0 ? 'badge-warning' : 'badge-success'}`}>
                                                            £{Math.abs(transfer.net_cost_change)}m
                                                        </span>
                                                    )}
                                                </div>
                                                <p className="transfer-reasoning">{transfer.reasoning}</p>
                                            </div>
                                        ))}
                                    </div>
                                ) : (
                                    <p className="text-secondary">No transfer suggestions at this time.</p>
                                )}
                            </div>
                        </div>
                    </div>
                )}

                <div className="info-section">
                    <h2>How to Get Your Team Screenshot</h2>
                    <div className="info-grid">
                        <div className="info-card card">
                            <div className="info-number">1</div>
                            <h3>Open FPL App/Website</h3>
                            <p>Navigate to your team's "Pitch" view</p>
                        </div>
                        <div className="info-card card">
                            <div className="info-number">2</div>
                            <h3>Take Screenshot</h3>
                            <p>Capture your full team including bench</p>
                        </div>
                        <div className="info-card card">
                            <div className="info-number">3</div>
                            <h3>Upload Here</h3>
                            <p>Upload the image and let AI do the rest</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default TeamAnalysis
