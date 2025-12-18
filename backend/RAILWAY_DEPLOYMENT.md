# Railway Deployment Guide for FPL AI Backend

## Prerequisites
- Railway account (sign up at https://railway.app)
- GitHub repository (optional but recommended)

## Deployment Steps

### Option 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add Railway deployment configuration"
   git push origin main
   ```

2. **Connect to Railway**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Select the `backend` directory as the root path

3. **Configure Environment Variables**
   In Railway dashboard, go to your project → Variables and add:
   
   ```
   ENV=production
   API_HOST=0.0.0.0
   API_PORT=$PORT
   API_RELOAD=false
   
   # Database (if using PostgreSQL on Railway)
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   
   # Supabase
   SUPABASE_URL=your_supabase_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   
   # Redis (if using Redis on Railway)
   REDIS_HOST=${{Redis.REDIS_HOST}}
   REDIS_PORT=${{Redis.REDIS_PORT}}
   REDIS_PASSWORD=${{Redis.REDIS_PASSWORD}}
   
   # Security
   SECRET_KEY=generate_a_secure_random_key_here
   
   # CORS (add your frontend URL)
   CORS_ORIGINS=https://your-frontend-url.com,http://localhost:5173
   
   # Logging
   LOG_LEVEL=INFO
   LOG_FILE=
   
   # Optional: Sentry for error tracking
   SENTRY_DSN=your_sentry_dsn
   ```

4. **Deploy**
   - Railway will automatically detect the Procfile and deploy
   - Monitor the build logs
   - Once deployed, you'll get a public URL

### Option 2: Deploy using Railway CLI

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize and Deploy**
   ```bash
   cd backend
   railway init
   railway up
   ```

4. **Add Environment Variables**
   ```bash
   railway variables set ENV=production
   railway variables set API_RELOAD=false
   # Add other variables as needed
   ```

5. **Generate Domain**
   ```bash
   railway domain
   ```

## Post-Deployment

### 1. Verify Deployment
Visit your Railway URL + `/health` to check if the API is running:
```
https://your-app.railway.app/health
```

### 2. Test API Documentation
Access the auto-generated API docs:
```
https://your-app.railway.app/docs
```

### 3. Monitor Logs
```bash
railway logs
```

Or view them in the Railway dashboard.

## Adding Additional Services

### PostgreSQL Database
```bash
railway add postgresql
```
This automatically sets `DATABASE_URL` environment variable.

### Redis Cache
```bash
railway add redis
```
This automatically sets Redis connection variables.

## Troubleshooting

### Build Fails
- Check `requirements.txt` for incompatible packages
- Ensure Python version in `runtime.txt` is supported
- Check Railway build logs for specific errors

### App Crashes on Startup
- Verify all required environment variables are set
- Check that `PORT` environment variable is being used
- Review application logs in Railway dashboard

### Health Check Fails
- Ensure `/health` endpoint is accessible
- Check healthcheck timeout settings in `railway.json`
- Verify the app is binding to `0.0.0.0` not `localhost`

### Large Dependencies (PyTorch, etc.)
If build times out due to large ML libraries:
1. Consider using a smaller model or lazy loading
2. Increase build timeout in Railway settings
3. Use pre-built wheels when possible

## Scaling

Railway automatically scales based on your plan. To optimize:

1. **Enable caching** - Use Redis for FPL API responses
2. **Optimize cold starts** - Lazy load ML models
3. **Use async operations** - FastAPI supports async/await
4. **Monitor performance** - Use Railway metrics dashboard

## Cost Optimization

- Use Railway's free tier for development
- Enable sleep mode for non-production environments
- Monitor resource usage in dashboard
- Consider using Railway's PostgreSQL instead of Supabase if cost is a concern

## Security Best Practices

1. **Never commit `.env` files**
2. **Use strong SECRET_KEY** - Generate with:
   ```python
   import secrets
   secrets.token_urlsafe(32)
   ```
3. **Restrict CORS origins** - Only allow your frontend domain
4. **Use HTTPS only** - Railway provides this by default
5. **Enable Sentry** - For production error tracking

## Continuous Deployment

Railway automatically redeploys when you push to your connected GitHub branch:
```bash
git add .
git commit -m "Update feature"
git push origin main
# Railway automatically deploys
```

## Useful Commands

```bash
# View logs
railway logs

# Open project in browser
railway open

# Connect to database
railway connect postgres

# Run commands in Railway environment
railway run python manage.py migrate

# Check deployment status
railway status
```

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Railway Status: https://status.railway.app
