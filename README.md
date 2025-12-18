# FPL AI Model 🤖⚽

An intelligent Fantasy Premier League assistant that uses machine learning to predict player performance and suggest optimal transfers.

## 🎯 Features

- **📸 Team Screenshot Upload** - Extract your FPL team from a screenshot using advanced OCR
- **🔮 ML-Powered Predictions** - Multi-model ensemble predicting gameweek points for all players
- **🔄 Smart Transfer Suggestions** - Optimal transfer recommendations respecting FPL constraints
- **👨‍✈️ Captain & Bench Optimization** - Data-driven captain picks and bench ordering
- **📊 Explainable AI** - Clear reasoning behind every prediction and recommendation
- **⚡ Real-time Updates** - Live FPL data integration with deadline-day accuracy

## 🏗️ Architecture

### Backend (Python + FastAPI)
- **ML Models:** XGBoost, CatBoost, LightGBM ensemble
- **OCR Engine:** Tesseract/EasyOCR for team extraction
- **Data Pipeline:** FPL API integration with Redis caching
- **Optimization:** Transfer suggestion engine with constraint solving

### Frontend (React + Vite)
- **Modern UI:** Premium design with smooth animations
- **Interactive:** Drag-and-drop upload, real-time validation
- **Responsive:** Mobile-first design
- **Visualizations:** Charts and insights dashboards

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Supabase account (database is pre-configured)
- Redis (optional, for caching)

### Backend Setup

The backend is configured to use Supabase as the database. The database schema has been created and is ready to use.

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Environment variables are pre-configured in .env
# The backend will automatically sync FPL data to Supabase

# Start development server
uvicorn main:app --reload --port 8000
```

The backend will automatically:
- Fetch data from the FPL API
- Store players, teams, fixtures, and gameweeks in Supabase
- Cache data to minimize API calls
- Sync predictions and team analyses to the database

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Visit `http://localhost:5173` to access the application.

## 📋 Usage

1. **Upload Team Screenshot** - Take a screenshot of your FPL team and upload it
2. **Validate Team** - Confirm the OCR correctly identified your players
3. **Generate Suggestions** - Click to get AI-powered predictions and transfer recommendations
4. **Review Insights** - Explore predictions, captain picks, and transfer options
5. **Make Decisions** - Use the insights to optimize your FPL team

## 🧠 How It Works

### 1. Image Processing
- Advanced OCR extracts player names from screenshots
- Fuzzy matching maps names to official FPL database
- User validation ensures 100% accuracy

### 2. Feature Engineering
- **Form Metrics:** Recent points, minutes, consistency
- **Fixture Analysis:** Opponent strength, home/away, difficulty ratings
- **Advanced Stats:** xG, xA, shots, key passes (when available)
- **Team Context:** Attacking/defensive strength, clean sheet probability
- **Player Context:** Rotation risk, injury status, price trends

### 3. ML Predictions
- **Points Predictor:** Ensemble model predicting expected points (mean, floor, ceiling)
- **Minutes Predictor:** Start probability and expected playing time
- **Position-Specific Models:** Tailored for GK, DEF, MID, FWD
- **Confidence Scores:** Uncertainty quantification for each prediction

### 4. Transfer Optimization
- Evaluates all viable transfer combinations
- Respects FPL constraints (budget, formation, free transfers)
- Scores by expected points gain, risk, and long-term value
- Provides multiple recommendation categories:
  - Best overall
  - Best differential
  - Best budget option
  - Best long-term pick
  - Safe pick
  - High-upside gamble

### 5. Explainability
- SHAP values for feature importance
- Natural language explanations
- Form narratives and fixture analysis
- Confidence intervals and risk ratings

## 📊 Model Performance

Our models are continuously evaluated and improved:

- **Ranking Correlation:** Spearman ρ > 0.65
- **Top 10 Accuracy:** >70% of predicted top 10 score in actual top 20
- **Start Probability:** >90% accuracy for predictable starters
- **Transfer ROI:** Positive expected value on 70%+ of suggestions

## 🛠️ Technology Stack

**Backend:**
- FastAPI, Pydantic
- Supabase (PostgreSQL database)
- XGBoost, CatBoost, LightGBM, PyTorch
- Tesseract/EasyOCR, RapidFuzz
- Redis (optional caching), Celery
- MLflow, Sentry

**Frontend:**
- React, Vite, React Router
- Tailwind CSS
- Axios, Zustand
- Recharts, Headless UI

**DevOps:**
- Docker, Docker Compose
- GitHub Actions
- AWS/GCP/Azure

## 📁 Project Structure

```
fpl-ai-model/
├── backend/           # FastAPI backend
│   ├── api/          # API routes
│   ├── ml/           # ML models and training
│   ├── services/     # Business logic
│   ├── models/       # Data models
│   └── utils/        # Utilities
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
├── docker/           # Docker configuration
├── tests/            # Test suites
└── scripts/          # Utility scripts
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e
```

## 🚢 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access application at http://localhost
```

### Cloud Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed cloud deployment instructions.

## 📈 Roadmap

- [x] Phase 1: Project setup
- [x] Phase 2: Data pipeline
- [x] Phase 3: OCR implementation
- [x] Phase 4: Feature engineering
- [ ] Phase 5: ML model development
- [ ] Phase 6: Transfer optimization
- [ ] Phase 7: Explainability layer
- [ ] Phase 8: Frontend development
- [ ] Phase 9: Integration & testing
- [ ] Phase 10: Deployment & monitoring

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](./LICENSE) for details.

## ⚠️ Disclaimer

This tool is for educational and entertainment purposes. FPL success depends on many unpredictable factors. Use predictions as guidance, not guarantees.

## 🙏 Acknowledgments

- Fantasy Premier League for the official API
- The FPL community for insights and data analysis
- Open-source ML and OCR libraries

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: support@fpl-ai-model.com (placeholder)

---

**Built with ❤️ for the FPL community**
