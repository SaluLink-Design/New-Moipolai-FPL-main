# 🚂 Railway Deployment Checklist

Use this checklist to ensure a smooth deployment to Railway.

## ✅ Pre-Deployment Checklist

### 1. Code Preparation
- [ ] All code is committed to Git
- [ ] `.env` file is in `.gitignore` (never commit secrets!)
- [ ] `requirements.txt` is up to date
- [ ] All imports are working locally
- [ ] Health check endpoint (`/health`) is accessible

### 2. Environment Variables Ready
- [ ] `SUPABASE_URL` - Get from Supabase dashboard
- [ ] `SUPABASE_ANON_KEY` - Get from Supabase dashboard
- [ ] `SECRET_KEY` - Generate using: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] `CORS_ORIGINS` - Your frontend URL(s)
- [ ] Optional: `SENTRY_DSN` for error tracking
- [ ] Optional: Database URL if using Railway PostgreSQL

### 3. Railway Account Setup
- [ ] Created account at https://railway.app
- [ ] GitHub connected (if deploying from GitHub)
- [ ] Payment method added (for usage beyond free tier)

## 🚀 Deployment Steps

### Option A: GitHub Deployment (Recommended)

- [ ] **Step 1**: Push code to GitHub
  ```bash
  git add .
  git commit -m "Add Railway deployment configuration"
  git push origin main
  ```

- [ ] **Step 2**: Create Railway project
  - Go to https://railway.app
  - Click "New Project"
  - Select "Deploy from GitHub repo"
  - Choose your repository

- [ ] **Step 3**: Configure project
  - Set root directory: `backend`
  - Railway will auto-detect Python and use nixpacks

- [ ] **Step 4**: Add environment variables
  - Go to Variables tab
  - Add all required variables (see section 2 above)
  - Set `ENV=production`
  - Set `API_RELOAD=false`

- [ ] **Step 5**: Deploy
  - Railway automatically deploys on push
  - Monitor build logs for errors

- [ ] **Step 6**: Generate domain
  - Go to Settings → Networking
  - Click "Generate Domain"
  - Copy your public URL

### Option B: Railway CLI Deployment

- [ ] **Step 1**: Install Railway CLI
  ```bash
  npm i -g @railway/cli
  ```

- [ ] **Step 2**: Login
  ```bash
  railway login
  ```

- [ ] **Step 3**: Initialize project
  ```bash
  cd backend
  railway init
  ```

- [ ] **Step 4**: Deploy
  ```bash
  railway up
  ```

- [ ] **Step 5**: Set environment variables
  ```bash
  railway variables set ENV=production
  railway variables set API_RELOAD=false
  railway variables set SUPABASE_URL=your_url
  railway variables set SUPABASE_ANON_KEY=your_key
  railway variables set SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
  railway variables set CORS_ORIGINS=https://your-frontend.com
  ```

- [ ] **Step 6**: Generate domain
  ```bash
  railway domain
  ```

### Option C: Use Deploy Script

- [ ] **Step 1**: Run the script
  ```bash
  cd backend
  ./deploy-railway.sh
  ```

- [ ] **Step 2**: Follow interactive prompts
  - Choose deployment method
  - Enter environment variables when prompted
  - Script handles the rest!

## ✅ Post-Deployment Verification

### 1. Test API Endpoints
- [ ] Visit `https://your-app.railway.app/` (should return health status)
- [ ] Visit `https://your-app.railway.app/health` (detailed health check)
- [ ] Visit `https://your-app.railway.app/docs` (API documentation)

### 2. Test API Functionality
```bash
# Health check
curl https://your-app.railway.app/health

# Test FPL endpoint (if available)
curl https://your-app.railway.app/api/fpl/bootstrap-static
```

### 3. Check Logs
```bash
# Using Railway CLI
railway logs

# Or view in Railway dashboard
```

### 4. Monitor Performance
- [ ] Check Railway dashboard metrics
- [ ] Monitor response times
- [ ] Check memory usage
- [ ] Verify no errors in logs

## 🔧 Optional Enhancements

### Add Database
- [ ] Add PostgreSQL: `railway add postgresql`
- [ ] Update `DATABASE_URL` in your app
- [ ] Run migrations if needed

### Add Redis Cache
- [ ] Add Redis: `railway add redis`
- [ ] Update Redis config in your app
- [ ] Test caching functionality

### Set Up Monitoring
- [ ] Add Sentry for error tracking
- [ ] Set `SENTRY_DSN` environment variable
- [ ] Test error reporting

### Custom Domain
- [ ] Purchase domain (if needed)
- [ ] Add custom domain in Railway settings
- [ ] Update DNS records
- [ ] Update `CORS_ORIGINS` with new domain

### CI/CD Setup
- [ ] Enable auto-deploy on push
- [ ] Set up staging environment
- [ ] Configure deployment notifications

## 🔒 Security Checklist

- [ ] `SECRET_KEY` is strong and unique
- [ ] `.env` file is not committed to Git
- [ ] CORS is restricted to your frontend domain(s) only
- [ ] `API_RELOAD=false` in production
- [ ] HTTPS is enabled (Railway does this automatically)
- [ ] Sensitive data is not logged
- [ ] Rate limiting is configured (if needed)
- [ ] Authentication is properly implemented

## 📱 Update Frontend

- [ ] Update frontend API URL to Railway URL
- [ ] Test frontend → backend communication
- [ ] Update CORS settings if needed
- [ ] Deploy frontend changes

## 🎯 Success Criteria

Your deployment is successful when:
- ✅ API responds at Railway URL
- ✅ `/health` endpoint returns healthy status
- ✅ `/docs` shows API documentation
- ✅ No errors in Railway logs
- ✅ Frontend can communicate with backend
- ✅ All API endpoints work as expected

## 📊 Monitoring & Maintenance

### Daily
- [ ] Check Railway dashboard for errors
- [ ] Monitor resource usage

### Weekly
- [ ] Review logs for issues
- [ ] Check for dependency updates
- [ ] Monitor costs

### Monthly
- [ ] Update dependencies
- [ ] Review and optimize performance
- [ ] Check security advisories

## 🆘 Troubleshooting

If something goes wrong, check:

1. **Build fails**
   - Review build logs in Railway dashboard
   - Check `requirements.txt` for incompatible packages
   - Verify Python version in `runtime.txt`

2. **App crashes on startup**
   - Check environment variables are set correctly
   - Review application logs: `railway logs`
   - Verify `PORT` is being used correctly

3. **Health check fails**
   - Ensure app binds to `0.0.0.0` not `localhost`
   - Check `/health` endpoint is accessible
   - Review healthcheck timeout settings

4. **Slow builds**
   - Use `requirements.railway.txt` (lighter dependencies)
   - Comment out heavy ML libraries if not needed
   - Enable build caching in Railway

## 📚 Resources

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Your Deployment Guide**: `RAILWAY_DEPLOYMENT.md`
- **Setup Summary**: `RAILWAY_SETUP_SUMMARY.md`

---

**Need help?** Check `RAILWAY_DEPLOYMENT.md` for detailed troubleshooting or join Railway Discord for support.

**Ready to deploy?** Start with the Pre-Deployment Checklist above! 🚀
