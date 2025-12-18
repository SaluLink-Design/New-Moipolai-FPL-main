# FPL AI Model - Implementation Plan

## Project Overview
An automated prediction and recommendation engine for Fantasy Premier League that:
1. Extracts user's team from screenshots using OCR
2. Predicts gameweek points using ML models
3. Suggests optimal transfers respecting FPL constraints
4. Provides actionable insights with confidence scores

---

## Phase 1: Project Setup & Infrastructure (Week 1)

### 1.1 Backend Setup
- [ ] Initialize Python FastAPI project
- [ ] Set up project structure (models, services, routes, utils)
- [ ] Configure environment variables and secrets
- [ ] Set up Redis for caching
- [ ] Create Docker configuration
- [ ] Set up logging and monitoring

### 1.2 Frontend Setup
- [ ] Initialize React + Vite project
- [ ] Set up Tailwind CSS or custom CSS
- [ ] Create component structure
- [ ] Set up routing (React Router)
- [ ] Configure API client (Axios/Fetch)
- [ ] Set up state management (Context API or Zustand)

### 1.3 Development Environment
- [ ] Set up virtual environment (Python)
- [ ] Install core dependencies
- [ ] Configure linting and formatting (Black, ESLint, Prettier)
- [ ] Set up Git repository and .gitignore
- [ ] Create development and production configs

---

## Phase 2: Data Pipeline (Week 2-3)

### 2.1 FPL API Integration
**Priority: HIGH**

**Files to create:**
- `backend/services/fpl_api.py` - FPL API client
- `backend/services/data_cache.py` - Redis caching layer
- `backend/models/fpl_models.py` - Pydantic models for FPL data

**Tasks:**
- [ ] Implement FPL API endpoints wrapper:
  - `/bootstrap-static/` - General game data
  - `/fixtures/` - Fixture data
  - `/element-summary/{player_id}/` - Player history
  - `/entry/{team_id}/` - Team data
- [ ] Create caching strategy (TTL-based)
- [ ] Implement data refresh scheduler (APScheduler)
- [ ] Build data validation layer
- [ ] Create snapshot system for deadline-day data

**Key Data Points:**
- Player stats (form, minutes, ICT, points history)
- Fixtures and difficulty ratings
- Injury/availability status
- Ownership, transfers in/out
- Price changes
- Team strength metrics

### 2.2 Data Storage
- [ ] Design database schema (PostgreSQL/SQLite)
- [ ] Create models for:
  - Players
  - Teams
  - Fixtures
  - Historical predictions
  - User teams
- [ ] Set up migrations (Alembic)
- [ ] Implement data ingestion pipeline

---

## Phase 3: OCR & Image Processing (Week 3-4)

### 3.1 OCR Implementation
**Priority: HIGH**

**Files to create:**
- `backend/services/ocr_service.py` - OCR processing
- `backend/services/team_parser.py` - Team extraction logic
- `backend/utils/image_preprocessing.py` - Image enhancement

**Tasks:**
- [ ] Implement image preprocessing:
  - Resize and normalize
  - Enhance contrast
  - Detect team layout regions
- [ ] Integrate OCR engine (Tesseract/EasyOCR/PaddleOCR)
- [ ] Extract player cards:
  - Player name
  - Club badge/name
  - Position
  - Points scored
- [ ] Implement fuzzy matching (RapidFuzz):
  - Match extracted names to FPL database
  - Handle common OCR errors
  - Validate team composition
- [ ] Create validation UI for user confirmation

### 3.2 Team Validation
- [ ] Build validation rules:
  - 15 players total
  - Formation constraints (GK:1, DEF:3-5, MID:2-5, FWD:1-3)
  - Budget constraints
  - Max 3 players per team
- [ ] Create correction interface for OCR errors
- [ ] Store validated teams

---

## Phase 4: Feature Engineering (Week 4-5)

### 4.1 Feature Pipeline
**Priority: HIGH**

**Files to create:**
- `backend/ml/feature_engineering.py` - Feature creation
- `backend/ml/feature_store.py` - Feature caching
- `backend/utils/stats_calculator.py` - Statistical calculations

**Tasks:**
- [ ] Implement feature categories:

#### Player Form Features
- [ ] Recent form (last 3, 5, 10 games)
- [ ] Points per game trends
- [ ] Minutes played consistency
- [ ] Home vs away performance split

#### Fixture Features
- [ ] Fixture difficulty rating (FDR)
- [ ] Opponent defensive strength
- [ ] Opponent attacking strength
- [ ] Home/away advantage
- [ ] Recent opponent form

#### Advanced Stats (if available)
- [ ] Expected goals (xG)
- [ ] Expected assists (xA)
- [ ] Expected goals involvement (xGI)
- [ ] Shots on target
- [ ] Key passes

#### Team Context Features
- [ ] Team attacking strength
- [ ] Team defensive strength
- [ ] Clean sheet probability
- [ ] Goals scored/conceded trends

#### Player-Specific Features
- [ ] Position-specific metrics
- [ ] Price and value (points per million)
- [ ] Ownership percentage
- [ ] Transfer trends (in/out)
- [ ] Rotation risk score
- [ ] Injury/suspension status

#### Manager Behavior Features
- [ ] Manager rotation patterns
- [ ] Predicted minutes
- [ ] Starting XI probability

### 4.2 Feature Store
- [ ] Create feature computation pipeline
- [ ] Implement feature versioning
- [ ] Set up feature caching
- [ ] Build feature validation tests

---

## Phase 5: ML Model Development (Week 5-7)

### 5.1 Model Architecture
**Priority: CRITICAL**

**Files to create:**
- `backend/ml/models/point_predictor.py` - Points prediction model
- `backend/ml/models/minutes_predictor.py` - Minutes/start probability
- `backend/ml/models/ensemble.py` - Model ensemble
- `backend/ml/training/trainer.py` - Training pipeline
- `backend/ml/evaluation/evaluator.py` - Model evaluation

**Tasks:**

#### 5.1.1 Points Prediction Model
- [ ] Collect historical training data (3+ seasons)
- [ ] Implement regression models:
  - XGBoost regressor
  - CatBoost regressor
  - LightGBM regressor
  - Neural network (PyTorch/TensorFlow)
- [ ] Create position-specific models (GK, DEF, MID, FWD)
- [ ] Implement ensemble strategy (weighted average/stacking)
- [ ] Output: Expected points (mean, floor, ceiling)

#### 5.1.2 Minutes Prediction Model
- [ ] Binary classification (start/bench)
- [ ] Regression for expected minutes
- [ ] Incorporate:
  - Injury news
  - Manager press conferences (if available)
  - Recent rotation patterns
  - Fixture congestion
- [ ] Output: Start probability, expected minutes

#### 5.1.3 Model Training
- [ ] Create train/validation/test splits (time-based)
- [ ] Implement cross-validation strategy
- [ ] Hyperparameter tuning (Optuna/GridSearch)
- [ ] Feature importance analysis (SHAP)
- [ ] Model versioning and tracking (MLflow)

#### 5.1.4 Model Evaluation
- [ ] Metrics:
  - MAE, RMSE for point predictions
  - Spearman correlation for ranking
  - ROC-AUC for start probability
  - Top-K accuracy (top 10 players)
- [ ] Backtesting framework
- [ ] Performance monitoring dashboard

### 5.2 Prediction Pipeline
- [ ] Real-time prediction API endpoint
- [ ] Batch prediction for all players
- [ ] Confidence interval calculation
- [ ] Prediction caching and updates

---

## Phase 6: Transfer Optimization Engine (Week 7-8)

### 6.1 Transfer Logic
**Priority: CRITICAL**

**Files to create:**
- `backend/services/transfer_optimizer.py` - Transfer optimization
- `backend/services/constraint_validator.py` - FPL rules validation
- `backend/utils/combinatorics.py` - Transfer combination generator

**Tasks:**

#### 6.1.1 Constraint Implementation
- [ ] Budget constraints
- [ ] Formation rules (3-4-3, 3-5-2, 4-3-3, 4-4-2, 4-5-1, 5-3-2, 5-4-1)
- [ ] Free transfer logic (1-2 FT, -4 hit per extra)
- [ ] Max 3 players per club
- [ ] Position requirements (GK:2, DEF:5, MID:5, FWD:3)

#### 6.1.2 Transfer Generation
- [ ] Single transfer combinations
- [ ] Double transfer combinations
- [ ] Multi-transfer strategies (with hits)
- [ ] Wildcard scenarios
- [ ] Free Hit scenarios
- [ ] Bench Boost optimization
- [ ] Triple Captain selection

#### 6.1.3 Scoring Algorithm
- [ ] Expected points gain calculation
- [ ] Risk-adjusted scoring
- [ ] Long-term value consideration (next 3-5 GWs)
- [ ] Team balance metrics
- [ ] Differential scoring (ownership consideration)

### 6.2 Recommendation Categories
- [ ] Best overall transfer
- [ ] Best differential (low ownership)
- [ ] Best budget option
- [ ] Best long-term pick (fixture run)
- [ ] Safe/low-risk pick
- [ ] High-upside gamble

### 6.3 Captain & Bench Optimization
- [ ] Captain recommendation (highest EV)
- [ ] Vice-captain selection
- [ ] Bench order optimization:
  - First bench: highest expected minutes
  - Consider formation flexibility
  - Auto-sub scenarios

---

## Phase 7: Explainability & Insights (Week 8-9)

### 7.1 Explanation Engine
**Files to create:**
- `backend/services/explainer.py` - Model explanation service
- `backend/utils/narrative_generator.py` - Natural language explanations

**Tasks:**
- [ ] Implement SHAP for feature importance
- [ ] Generate per-prediction explanations:
  - Key factors driving prediction
  - Recent form narrative
  - Fixture analysis
  - Rotation risk explanation
- [ ] Create confidence scores
- [ ] Build comparison views (player A vs player B)

### 7.2 Insights Dashboard
- [ ] Form trends visualization
- [ ] Fixture difficulty charts
- [ ] Price change predictions
- [ ] Ownership trends
- [ ] Template team analysis

---

## Phase 8: Frontend Development (Week 9-11)

### 8.1 Core Components
**Files to create:**
- `src/components/ImageUpload.jsx` - Team screenshot upload
- `src/components/TeamDisplay.jsx` - Parsed team visualization
- `src/components/PredictionTable.jsx` - Player predictions
- `src/components/TransferSuggestions.jsx` - Transfer recommendations
- `src/components/CaptainPicker.jsx` - Captain selection
- `src/components/BenchOptimizer.jsx` - Bench order
- `src/components/ExplanationPanel.jsx` - Model explanations

### 8.2 Pages
- `src/pages/Home.jsx` - Landing page
- `src/pages/TeamAnalysis.jsx` - Main analysis flow
- `src/pages/Predictions.jsx` - All player predictions
- `src/pages/Transfers.jsx` - Transfer suggestions
- `src/pages/History.jsx` - Past predictions & accuracy

### 8.3 Features
- [ ] Drag-and-drop image upload
- [ ] Team validation interface
- [ ] Interactive transfer selection
- [ ] Filtering and sorting predictions
- [ ] Save/load team configurations
- [ ] Export recommendations (PDF/CSV)

### 8.4 Design System
- [ ] Create design tokens (colors, spacing, typography)
- [ ] Build reusable components
- [ ] Implement responsive layouts
- [ ] Add loading states and animations
- [ ] Error handling and user feedback
- [ ] Premium, modern aesthetic (gradients, glassmorphism)

---

## Phase 9: Integration & Testing (Week 11-12)

### 9.1 API Integration
- [ ] Connect frontend to backend APIs
- [ ] Implement error handling
- [ ] Add loading states
- [ ] Set up API retry logic
- [ ] Configure CORS

### 9.2 Testing
- [ ] Backend unit tests (pytest)
- [ ] Frontend component tests (Vitest/Jest)
- [ ] Integration tests
- [ ] E2E tests (Playwright)
- [ ] Model performance tests
- [ ] Load testing

### 9.3 Quality Assurance
- [ ] OCR accuracy validation
- [ ] Prediction accuracy monitoring
- [ ] Transfer logic verification
- [ ] Constraint validation testing
- [ ] User acceptance testing

---

## Phase 10: Deployment & Monitoring (Week 12-13)

### 10.1 Deployment
- [ ] Containerize application (Docker)
- [ ] Set up CI/CD pipeline (GitHub Actions)
- [ ] Deploy to cloud (AWS/GCP/Azure):
  - Backend: ECS/Cloud Run/App Service
  - Frontend: S3+CloudFront/Cloud Storage/Blob Storage
  - Database: RDS/Cloud SQL/Azure Database
  - Redis: ElastiCache/Memorystore/Azure Cache
- [ ] Configure domain and SSL
- [ ] Set up CDN

### 10.2 Monitoring & Maintenance
- [ ] Application monitoring (Sentry/DataDog)
- [ ] Model performance tracking
- [ ] Prediction accuracy dashboard
- [ ] Automated model retraining
- [ ] Scheduled data updates (cron jobs)
- [ ] Alerting for failures

### 10.3 Scheduled Jobs
- [ ] Daily: Update player stats and fixtures
- [ ] Hourly (deadline day): Refresh all data
- [ ] Weekly: Retrain models with new data
- [ ] Pre-gameweek: Generate predictions
- [ ] Post-gameweek: Evaluate prediction accuracy

---

## Technology Stack

### Backend
- **Framework:** FastAPI
- **ML:** XGBoost, CatBoost, LightGBM, PyTorch/TensorFlow
- **OCR:** Tesseract/EasyOCR/PaddleOCR
- **Fuzzy Matching:** RapidFuzz
- **Caching:** Redis
- **Database:** PostgreSQL
- **Task Queue:** Celery + Redis
- **Scheduler:** APScheduler
- **Monitoring:** MLflow, Sentry

### Frontend
- **Framework:** React + Vite
- **Styling:** Tailwind CSS or Custom CSS
- **State:** Context API or Zustand
- **HTTP:** Axios
- **Charts:** Recharts or Chart.js
- **UI Components:** Headless UI or Radix UI

### DevOps
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Cloud:** AWS/GCP/Azure
- **Monitoring:** DataDog/CloudWatch

---

## Success Metrics

### Model Performance
- **Ranking Correlation:** Spearman ρ > 0.65
- **Top 10 Accuracy:** >70% of top 10 predicted players score in top 20
- **Start Probability:** >90% accuracy for predictable starters
- **Transfer ROI:** Positive expected value on 70%+ of suggestions

### System Performance
- **OCR Accuracy:** >95% correct player identification
- **API Response Time:** <2s for predictions
- **Uptime:** >99.5%
- **Data Freshness:** <1 hour lag from FPL API

### User Experience
- **Upload to Suggestions:** <30 seconds
- **Explanation Clarity:** User comprehension >80%
- **Mobile Responsive:** Full functionality on mobile

---

## Risk Mitigation

### Technical Risks
1. **OCR Accuracy Issues**
   - Mitigation: Multiple OCR engines, user validation step
   
2. **FPL API Rate Limits**
   - Mitigation: Aggressive caching, request throttling
   
3. **Model Overfitting**
   - Mitigation: Cross-validation, regularization, ensemble methods
   
4. **Data Quality**
   - Mitigation: Validation layers, anomaly detection

### Business Risks
1. **FPL API Changes**
   - Mitigation: Version monitoring, fallback data sources
   
2. **Prediction Accuracy**
   - Mitigation: Continuous monitoring, A/B testing, user feedback

---

## Next Steps

1. **Immediate (This Week):**
   - Set up project structure
   - Initialize backend and frontend
   - Implement FPL API client
   - Test OCR on sample images

2. **Short-term (Next 2 Weeks):**
   - Complete data pipeline
   - Build feature engineering
   - Start model development

3. **Medium-term (Next Month):**
   - Train and evaluate models
   - Build transfer optimization
   - Develop frontend UI

4. **Long-term (Next 2 Months):**
   - Integration and testing
   - Deployment
   - Monitoring and iteration

---

## File Structure

```
fpl-ai-model/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── predictions.py
│   │   │   ├── transfers.py
│   │   │   ├── teams.py
│   │   │   └── ocr.py
│   │   └── dependencies.py
│   ├── ml/
│   │   ├── models/
│   │   │   ├── point_predictor.py
│   │   │   ├── minutes_predictor.py
│   │   │   └── ensemble.py
│   │   ├── training/
│   │   │   ├── trainer.py
│   │   │   └── data_loader.py
│   │   ├── evaluation/
│   │   │   └── evaluator.py
│   │   └── feature_engineering.py
│   ├── services/
│   │   ├── fpl_api.py
│   │   ├── data_cache.py
│   │   ├── ocr_service.py
│   │   ├── team_parser.py
│   │   ├── transfer_optimizer.py
│   │   ├── constraint_validator.py
│   │   └── explainer.py
│   ├── models/
│   │   ├── fpl_models.py
│   │   └── db_models.py
│   ├── utils/
│   │   ├── image_preprocessing.py
│   │   ├── stats_calculator.py
│   │   └── combinatorics.py
│   ├── config.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ImageUpload.jsx
│   │   │   ├── TeamDisplay.jsx
│   │   │   ├── PredictionTable.jsx
│   │   │   ├── TransferSuggestions.jsx
│   │   │   ├── CaptainPicker.jsx
│   │   │   ├── BenchOptimizer.jsx
│   │   │   └── ExplanationPanel.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── TeamAnalysis.jsx
│   │   │   ├── Predictions.jsx
│   │   │   ├── Transfers.jsx
│   │   │   └── History.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── utils/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
├── tests/
│   ├── backend/
│   └── frontend/
├── scripts/
│   ├── train_model.py
│   ├── update_data.py
│   └── evaluate_predictions.py
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── .gitignore
├── README.md
└── IMPLEMENTATION_PLAN.md
```

---

## Conclusion

This is a comprehensive, production-ready plan for building the FPL AI Model. The system is designed to be:
- **Accurate:** Multi-model ensemble with continuous evaluation
- **Reliable:** Robust data pipeline with caching and validation
- **User-friendly:** Simple upload → suggestions workflow
- **Explainable:** Clear reasoning for all recommendations
- **Scalable:** Cloud-native architecture with monitoring

The phased approach allows for iterative development and testing, ensuring each component works before moving to the next.
