# FPL AI Model - Project Structure

## 📁 Complete Directory Tree

```
fpl-ai-model/
│
├── 📄 README.md                          # Project overview
├── 📄 START_HERE.md                      # ⭐ Quick reference guide
├── 📄 GETTING_STARTED.md                 # Setup instructions
├── 📄 IMPLEMENTATION_PLAN.md             # 10-phase roadmap
├── 📄 PROJECT_SUMMARY.md                 # Architecture & features
├── 📄 .gitignore                         # Git exclusions
│
├── 📁 backend/                           # Python FastAPI Backend
│   ├── 📄 main.py                        # ⭐ FastAPI application entry
│   ├── 📄 config.py                      # Configuration management
│   ├── 📄 requirements.txt               # Python dependencies
│   ├── 📄 .env.example                   # Environment template
│   ├── 📄 .env                           # Environment config (create from .env.example)
│   │
│   ├── 📁 api/                           # API Layer
│   │   ├── 📄 __init__.py
│   │   └── 📁 routes/                    # API Endpoints
│   │       ├── 📄 __init__.py
│   │       ├── 📄 ocr.py                 # Image upload & OCR
│   │       ├── 📄 predictions.py         # Player predictions
│   │       ├── 📄 transfers.py           # Transfer suggestions
│   │       └── 📄 teams.py               # Team analysis
│   │
│   ├── 📁 services/                      # Business Logic
│   │   ├── 📄 __init__.py
│   │   ├── 📄 fpl_api.py                 # ⭐ FPL API integration
│   │   ├── 📄 ocr_service.py             # ⭐ OCR processing
│   │   └── 📄 data_cache.py              # Redis caching
│   │
│   ├── 📁 models/                        # Data Models
│   │   ├── 📄 __init__.py
│   │   └── 📄 fpl_models.py              # ⭐ Pydantic models
│   │
│   ├── 📁 ml/                            # Machine Learning
│   │   ├── 📄 __init__.py
│   │   ├── 📁 models/                    # ML model implementations
│   │   ├── 📁 training/                  # Training scripts
│   │   └── 📁 evaluation/                # Model evaluation
│   │
│   ├── 📁 utils/                         # Utilities
│   │   └── 📄 __init__.py
│   │
│   ├── 📁 tests/                         # Backend tests
│   ├── 📁 logs/                          # Application logs
│   ├── 📁 uploads/                       # Uploaded images
│   └── 📁 models/                        # Trained ML models
│
├── 📁 frontend/                          # React Frontend
│   ├── 📄 package.json                   # Node dependencies
│   ├── 📄 vite.config.js                 # Vite configuration
│   ├── 📄 index.html                     # HTML template
│   │
│   └── 📁 src/                           # Source code
│       ├── 📄 main.jsx                   # ⭐ React entry point
│       ├── 📄 App.jsx                    # ⭐ Main app component
│       ├── 📄 index.css                  # ⭐ Design system
│       │
│       ├── 📁 components/                # Reusable Components
│       │   ├── 📄 Navbar.jsx             # Navigation bar
│       │   └── 📄 Navbar.css             # Navbar styles
│       │
│       ├── 📁 pages/                     # Page Components
│       │   ├── 📄 Home.jsx               # ⭐ Landing page
│       │   ├── 📄 Home.css               # Home page styles
│       │   ├── 📄 TeamAnalysis.jsx       # Upload & analyze
│       │   ├── 📄 TeamAnalysis.css       # Analysis styles
│       │   ├── 📄 Predictions.jsx        # Predictions view
│       │   ├── 📄 Transfers.jsx          # Transfer suggestions
│       │   └── 📄 History.jsx            # History tracking
│       │
│       ├── 📁 services/                  # API Services
│       │   └── 📄 api.js                 # ⭐ API client
│       │
│       ├── 📁 utils/                     # Utilities
│       └── 📁 assets/                    # Static assets
│
├── 📁 docker/                            # Docker Configuration
│   ├── 📄 Dockerfile.backend             # Backend container
│   ├── 📄 Dockerfile.frontend            # Frontend container
│   └── 📄 docker-compose.yml             # Full stack orchestration
│
├── 📁 scripts/                           # Utility Scripts
│   └── 📄 quickstart.sh                  # ⭐ Quick start script
│
├── 📁 tests/                             # Test Suites
│   ├── 📁 backend/                       # Backend tests
│   └── 📁 frontend/                      # Frontend tests
│
└── 📁 .github/                           # GitHub Configuration
    └── 📁 workflows/                     # CI/CD workflows (future)
```

## 🌟 Key Files (⭐ marked above)

### Must-Read Documentation
1. **START_HERE.md** - Your first stop! Quick reference
2. **GETTING_STARTED.md** - Complete setup guide
3. **README.md** - Project overview

### Backend Essentials
1. **backend/main.py** - FastAPI application
2. **backend/services/fpl_api.py** - FPL data integration
3. **backend/services/ocr_service.py** - Image processing
4. **backend/models/fpl_models.py** - Data structures

### Frontend Essentials
1. **frontend/src/App.jsx** - Main application
2. **frontend/src/index.css** - Design system
3. **frontend/src/pages/Home.jsx** - Landing page
4. **frontend/src/services/api.js** - Backend communication

### Quick Start
1. **scripts/quickstart.sh** - One-command setup

## 📊 File Count by Category

| Category | Files | Purpose |
|----------|-------|---------|
| Documentation | 5 | Guides and references |
| Backend Python | 15+ | API and services |
| Frontend React | 15+ | UI components |
| Configuration | 8 | Docker, env, package |
| Scripts | 1 | Automation |
| **Total** | **50+** | **Complete app** |

## 🎯 Where to Start

### Day 1: Setup
1. Read `START_HERE.md`
2. Run `./scripts/quickstart.sh`
3. Visit http://localhost:5173

### Day 2: Explore
1. Check API docs at http://localhost:8000/docs
2. Review `backend/main.py`
3. Explore `frontend/src/pages/Home.jsx`

### Day 3: Understand
1. Read `IMPLEMENTATION_PLAN.md`
2. Study `backend/services/fpl_api.py`
3. Review `frontend/src/index.css`

### Week 1: Build
1. Test OCR with screenshots
2. Fetch FPL data
3. Plan ML models

## 🔍 Finding Things

### Need to...
- **Change API endpoints?** → `backend/api/routes/`
- **Modify UI design?** → `frontend/src/index.css`
- **Update data models?** → `backend/models/fpl_models.py`
- **Add new pages?** → `frontend/src/pages/`
- **Configure environment?** → `backend/.env`
- **Adjust Docker?** → `docker/docker-compose.yml`

### Looking for...
- **FPL API logic?** → `backend/services/fpl_api.py`
- **OCR processing?** → `backend/services/ocr_service.py`
- **Caching logic?** → `backend/services/data_cache.py`
- **Navigation?** → `frontend/src/components/Navbar.jsx`
- **Landing page?** → `frontend/src/pages/Home.jsx`
- **API client?** → `frontend/src/services/api.js`

## 📈 Growth Path

### Current Structure
```
backend/
├── api/          ✅ Routes defined
├── services/     ✅ Core services ready
├── models/       ✅ Data models complete
├── ml/           🔧 Ready for implementation
└── utils/        🔧 Ready for helpers
```

### Next Additions
```
backend/ml/
├── models/
│   ├── point_predictor.py      # To implement
│   ├── minutes_predictor.py    # To implement
│   └── ensemble.py             # To implement
├── training/
│   ├── trainer.py              # To implement
│   └── data_loader.py          # To implement
└── evaluation/
    └── evaluator.py            # To implement
```

## 🎨 Design System Location

All design tokens are in `frontend/src/index.css`:
- **Colors:** Lines 10-30
- **Spacing:** Lines 40-50
- **Typography:** Lines 60-75
- **Components:** Lines 100+

## 🚀 Quick Commands

```bash
# Start everything
./scripts/quickstart.sh

# Backend only
cd backend && source venv/bin/activate && uvicorn main:app --reload

# Frontend only
cd frontend && npm run dev

# Docker
cd docker && docker-compose up

# Install backend deps
cd backend && pip install -r requirements.txt

# Install frontend deps
cd frontend && npm install

# View API docs
open http://localhost:8000/docs

# View app
open http://localhost:5173
```

## 💡 Pro Tips

1. **Use the docs** - They're comprehensive!
2. **Start with START_HERE.md** - Best overview
3. **Check logs** - `backend/logs/app.log`
4. **Test incrementally** - One feature at a time
5. **Follow the plan** - `IMPLEMENTATION_PLAN.md`

---

**Happy coding! 🚀**
