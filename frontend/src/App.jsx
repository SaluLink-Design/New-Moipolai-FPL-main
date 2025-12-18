import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import TeamAnalysis from './pages/TeamAnalysis'
import Predictions from './pages/Predictions'
import Transfers from './pages/Transfers'
import History from './pages/History'
import Navbar from './components/Navbar'

function App() {
    return (
        <Router>
            <div className="app">
                <Navbar />
                <main>
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/analyze" element={<TeamAnalysis />} />
                        <Route path="/predictions" element={<Predictions />} />
                        <Route path="/transfers" element={<Transfers />} />
                        <Route path="/history" element={<History />} />
                    </Routes>
                </main>
            </div>
        </Router>
    )
}

export default App
