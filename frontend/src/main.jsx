import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

console.log('FPL AI App starting...');
console.log('Environment check:', {
    supabaseUrl: import.meta.env.VITE_SUPABASE_URL ? 'configured' : 'MISSING',
    supabaseKey: import.meta.env.VITE_SUPABASE_ANON_KEY ? 'configured' : 'MISSING',
    mode: import.meta.env.MODE
});

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
)
