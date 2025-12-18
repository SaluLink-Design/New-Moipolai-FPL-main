# 🚂 Railway Deployment - Quick Start

Your FPL AI backend is now **100% ready** for Railway deployment! 🎉

## 🎯 What You Need to Do

Choose **ONE** of these three methods:

### 🚀 Method 1: Interactive Script (Easiest!)
```bash
cd backend
./deploy-railway.sh
```
The script will guide you through everything!

### 🐙 Method 2: GitHub (Best for CI/CD)
```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy to Railway"
git push origin main

# 2. Go to railway.app → New Project → Deploy from GitHub
# 3. Select your repo, set root to "backend"
# 4. Add environment variables (see below)
# 5. Done! Railway auto-deploys
```

### 💻 Method 3: Railway CLI
```bash
# 1. Install CLI
npm i -g @railway/cli

# 2. Deploy
cd backend
railway login
railway init
railway up
railway domain

# 3. Set environment variables (see below)
```

## 🔑 Required Environment Variables

Set these in Railway dashboard or CLI:

```bash
ENV=production
API_RELOAD=false
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SECRET_KEY=your_secret_key_here  # Generate below
CORS_ORIGINS=https://your-frontend.com
```

### Generate SECRET_KEY:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## ✅ After Deployment

Test your API:
```bash
# Health check
curl https://your-app.railway.app/health

# API docs
open https://your-app.railway.app/docs
```

## 📚 Documentation

- **Quick Checklist**: `RAILWAY_CHECKLIST.md` ← Start here!
- **Detailed Guide**: `RAILWAY_DEPLOYMENT.md`
- **Setup Summary**: `RAILWAY_SETUP_SUMMARY.md`

## 🆘 Need Help?

1. Check `RAILWAY_CHECKLIST.md` for step-by-step guide
2. Review `RAILWAY_DEPLOYMENT.md` for troubleshooting
3. Join Railway Discord: https://discord.gg/railway

---

**Ready?** Run `./deploy-railway.sh` now! 🚀
