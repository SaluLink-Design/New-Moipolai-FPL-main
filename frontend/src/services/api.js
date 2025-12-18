import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Request interceptor
api.interceptors.request.use(
    (config) => {
        // Add auth token if available
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Response interceptor
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Handle unauthorized
            localStorage.removeItem('token')
        }
        return Promise.reject(error)
    }
)

// API Methods
export const apiService = {
    // Health check
    healthCheck: () => api.get('/health'),

    // OCR endpoints
    uploadTeamImage: (formData) =>
        api.post('/api/ocr/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        }),

    validateTeam: (teamData) => api.post('/api/ocr/validate', teamData),

    // Predictions endpoints
    getPredictions: (gameweek) =>
        api.get('/api/predictions', { params: { gameweek } }),

    getPlayerPrediction: (playerId, gameweek) =>
        api.get(`/api/predictions/player/${playerId}`, { params: { gameweek } }),

    // Transfers endpoints
    getTransferSuggestions: (teamData) =>
        api.post('/api/transfers/suggestions', teamData),

    evaluateTransfer: (transferData) =>
        api.post('/api/transfers/evaluate', transferData),

    // Teams endpoints
    getTeamAnalysis: (teamData) => {
        const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
        const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

        if (!supabaseUrl || !supabaseKey) {
            console.error('Supabase credentials not configured:', { supabaseUrl, supabaseKey: supabaseKey ? 'present' : 'missing' });
            return Promise.reject(new Error('Supabase credentials not configured'));
        }

        const apiUrl = `${supabaseUrl}/functions/v1/analyze-team`;
        console.log('Calling Edge Function:', apiUrl);

        return axios.post(apiUrl, teamData, {
            headers: {
                'Authorization': `Bearer ${supabaseKey}`,
                'Content-Type': 'application/json',
            },
        });
    },

    getCaptainSuggestion: (teamData) =>
        api.post('/api/teams/captain', teamData),

    getBenchOrder: (teamData) =>
        api.post('/api/teams/bench', teamData),

    // FPL data endpoints
    getCurrentGameweek: () => api.get('/api/fpl/gameweek/current'),

    getPlayers: () => api.get('/api/fpl/players'),

    getFixtures: (gameweek) =>
        api.get('/api/fpl/fixtures', { params: { gameweek } }),
}

export default api
