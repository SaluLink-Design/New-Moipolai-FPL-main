# FPL AI Model - Getting Started Guide

Welcome to the FPL AI Model project! This guide will help you get up and running quickly.

## 📦 What's Been Built

### Phase 1: Foundation ✅
The initial project structure has been created with:

#### Backend (Python + FastAPI)
- ✅ FastAPI application with CORS and middleware
- ✅ Configuration management with Pydantic
- ✅ FPL API client with caching
- ✅ Redis cache manager
- ✅ OCR service (EasyOCR/Tesseract support)
- ✅ Comprehensive Pydantic models
- ✅ API routes (OCR, Predictions, Transfers, Teams)
- ✅ Logging and error handling

#### Frontend (React + Vite)
- ✅ React 18 with Vite build system
- ✅ Premium dark theme design system
- ✅ Responsive navigation with glassmorphism
- ✅ Stunning home page with animations
- ✅ Team analysis page with image upload
- ✅ API service layer with Axios
- ✅ React Router setup

#### DevOps
- ✅ Docker configuration (backend, frontend, Redis)
- ✅ Docker Compose orchestration
- ✅ Quick start script
- ✅ .gitignore configuration

## 🚀 Quick Start

### Option 1: Quick Start Script (Recommended)

```bash
# Make the script executable
chmod +x scripts/quickstart.sh

# Run it
./scripts/quickstart.sh
```

This will:
1. Check prerequisites (Python, Node.js)
2. Set up backend virtual environment
3. Install all dependencies
4. Start both backend and frontend servers

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Start server
uvicorn main:app --reload --port 8000
```

Backend will be available at: **http://localhost:8000**
API docs at: **http://localhost:8000/docs**

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: **http://localhost:5173**

### Option 3: Docker

```bash
cd docker
docker-compose up -d
```

## 📁 Project Structure

```
fpl-ai-model/
├── backend/                    # Python FastAPI backend
│   ├── api/
│   │   └── routes/            # API endpoints
│   │       ├── ocr.py         # Image upload & OCR
│   │       ├── predictions.py # Player predictions
│   │       ├── transfers.py   # Transfer suggestions
│   │       └── teams.py       # Team analysis
│   ├── ml/                    # ML models (to be implemented)
│   ├── models/
│   │   └── fpl_models.py      # Pydantic data models
│   ├── services/
│   │   ├── fpl_api.py         # FPL API client
│   │   ├── data_cache.py      # Redis cache manager
│   │   └── ocr_service.py     # OCR processing
│   ├── config.py              # Configuration
│   ├── main.py                # FastAPI app
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── Navbar.jsx     # Navigation component
│   │   ├── pages/
│   │   │   ├── Home.jsx       # Landing page
│   │   │   ├── TeamAnalysis.jsx # Upload & analyze
│   │   │   ├── Predictions.jsx
│   │   │   ├── Transfers.jsx
│   │   │   └── History.jsx
│   │   ├── services/
│   │   │   └── api.js         # API client
│   │   ├── App.jsx            # Main app component
│   │   ├── main.jsx           # Entry point
│   │   └── index.css          # Design system
│   ├── package.json
│   └── vite.config.js
│
├── docker/                     # Docker configuration
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
│
├── scripts/
│   └── quickstart.sh          # Quick start script
│
├── IMPLEMENTATION_PLAN.md     # Detailed implementation plan
└── README.md                  # Project documentation
```

## 🎯 Current Features

### Working Features ✅
1. **Backend API**
   - Health check endpoints
   - FPL API integration (live data fetching)
   - OCR image upload endpoint
   - Route structure for predictions, transfers, teams

2. **Frontend UI**
   - Premium dark theme design
   - Responsive navigation
   - Beautiful landing page with animations
   - Team analysis page with image upload
   - Smooth transitions and micro-animations

3. **Infrastructure**
   - Redis caching (optional, graceful degradation)
   - Docker containerization
   - Environment configuration
   - Logging system

### In Progress 🚧
1. **OCR Processing**
   - Image preprocessing ✅
   - Text extraction ✅
   - Player name matching ✅
   - Team validation ✅
   - *Needs: Testing with real FPL screenshots*

2. **ML Models**
   - Feature engineering framework
   - Model training pipeline
   - Prediction generation
   - *Status: Architecture defined, implementation needed*

3. **Transfer Optimization**
   - Constraint validation
   - Transfer generation
   - Scoring algorithm
   - *Status: API structure ready, logic needed*

## 📝 Next Steps

### Immediate (This Week)
1. **Test OCR with Real Screenshots**
   ```bash
   # Upload your FPL screenshot at:
   http://localhost:5173/analyze
   ```

2. **Verify FPL API Integration**
   ```bash
   # Check API docs:
   http://localhost:8000/docs
   
   # Test endpoints:
   curl http://localhost:8000/health
   ```

3. **Review Design**
   - Check the home page design
   - Test responsive layouts
   - Verify animations

### Short-term (Next 2 Weeks)
1. **Feature Engineering**
   - Implement feature calculation functions
   - Create feature store
   - Add data validation

2. **ML Model Development**
   - Collect historical FPL data
   - Train baseline models
   - Implement prediction pipeline

3. **Frontend Enhancements**
   - Build prediction table component
   - Create transfer suggestion cards
   - Add loading states and error handling

### Medium-term (Next Month)
1. **Transfer Optimization**
   - Implement constraint solver
   - Build transfer generation logic
   - Add multi-transfer strategies

2. **Explainability**
   - Integrate SHAP
   - Generate explanations
   - Create insight visualizations

3. **Testing & Polish**
   - Unit tests
   - Integration tests
   - UI/UX improvements

## 🔧 Configuration

### Environment Variables

The backend uses environment variables for configuration. Copy `.env.example` to `.env` and customize:

```bash
# Key settings to configure:
ENV=development
DATABASE_URL=sqlite:///./fpl_ai.db
REDIS_HOST=localhost  # Set to 'redis' for Docker
OCR_ENGINE=easyocr    # or 'tesseract'
```

### Optional: Redis Setup

Redis is optional but recommended for caching. The app will work without it.

**Install Redis:**
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis

# Or use Docker
docker run -d -p 6379:6379 redis:7-alpine
```

## 🧪 Testing

### Test Backend
```bash
cd backend
source venv/bin/activate

# Run tests (when implemented)
pytest

# Test API manually
curl http://localhost:8000/
curl http://localhost:8000/health
```

### Test Frontend
```bash
cd frontend

# Run tests (when implemented)
npm test

# Build for production
npm run build
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🎨 Design System

The frontend uses a premium dark theme with:
- **Colors:** Purple primary, green secondary, orange accent
- **Typography:** Inter (body), Outfit (headings)
- **Effects:** Glassmorphism, gradients, smooth animations
- **Responsive:** Mobile-first design

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version (need 3.9+)
python3 --version

# Reinstall dependencies
pip install -r requirements.txt

# Check logs
tail -f logs/app.log
```

### Frontend won't start
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node version (need 18+)
node --version
```

### OCR not working
```bash
# Install Tesseract (if using tesseract engine)
brew install tesseract  # macOS
sudo apt install tesseract-ocr  # Ubuntu

# Or switch to EasyOCR in .env
OCR_ENGINE=easyocr
```

## 📖 Learning Resources

- **FastAPI:** https://fastapi.tiangolo.com/
- **React:** https://react.dev/
- **FPL API:** https://fantasy.premierleague.com/api/bootstrap-static/
- **XGBoost:** https://xgboost.readthedocs.io/
- **EasyOCR:** https://github.com/JaidedAI/EasyOCR

## 🤝 Contributing

See `IMPLEMENTATION_PLAN.md` for the full development roadmap.

## 📄 License

MIT License - See LICENSE file for details

---

**Ready to build the future of FPL AI? Let's go! 🚀⚽🤖**
