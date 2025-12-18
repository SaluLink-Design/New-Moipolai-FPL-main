#!/bin/bash

# Railway Deployment Script for FPL AI Backend
# This script helps you deploy your backend to Railway

set -e  # Exit on error

echo "🚂 Railway Deployment Helper for FPL AI Backend"
echo "================================================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI is not installed."
    echo ""
    echo "Would you like to install it? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "📦 Installing Railway CLI..."
        npm i -g @railway/cli
        echo "✅ Railway CLI installed successfully!"
    else
        echo "Please install Railway CLI manually:"
        echo "  npm i -g @railway/cli"
        echo ""
        echo "Or deploy via GitHub:"
        echo "  1. Push your code to GitHub"
        echo "  2. Go to https://railway.app"
        echo "  3. Create new project from GitHub repo"
        exit 1
    fi
fi

echo ""
echo "Choose deployment method:"
echo "  1) Deploy using Railway CLI (quick)"
echo "  2) Show GitHub deployment instructions"
echo "  3) Exit"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Deploying with Railway CLI..."
        echo ""
        
        # Login to Railway
        echo "📝 Logging in to Railway..."
        railway login
        
        # Initialize project
        echo ""
        echo "🔧 Initializing Railway project..."
        railway init
        
        # Deploy
        echo ""
        echo "📤 Deploying to Railway..."
        railway up
        
        # Set environment variables
        echo ""
        echo "⚙️  Setting environment variables..."
        echo ""
        echo "Please enter the following values (press Enter to skip):"
        echo ""
        
        read -p "SUPABASE_URL: " supabase_url
        if [ ! -z "$supabase_url" ]; then
            railway variables set SUPABASE_URL="$supabase_url"
        fi
        
        read -p "SUPABASE_ANON_KEY: " supabase_key
        if [ ! -z "$supabase_key" ]; then
            railway variables set SUPABASE_ANON_KEY="$supabase_key"
        fi
        
        # Generate secret key
        echo ""
        echo "🔐 Generating SECRET_KEY..."
        secret_key=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
        railway variables set SECRET_KEY="$secret_key"
        
        # Set production environment
        railway variables set ENV=production
        railway variables set API_RELOAD=false
        railway variables set LOG_LEVEL=INFO
        
        echo ""
        echo "🌐 Generating public domain..."
        railway domain
        
        echo ""
        echo "✅ Deployment complete!"
        echo ""
        echo "📊 View your deployment:"
        railway open
        
        echo ""
        echo "📝 View logs:"
        echo "  railway logs"
        echo ""
        echo "🔍 Test your API:"
        echo "  Visit: https://your-app.railway.app/health"
        echo "  API Docs: https://your-app.railway.app/docs"
        ;;
        
    2)
        echo ""
        echo "📚 GitHub Deployment Instructions"
        echo "=================================="
        echo ""
        echo "1. Push your code to GitHub:"
        echo "   git add ."
        echo "   git commit -m 'Add Railway deployment config'"
        echo "   git push origin main"
        echo ""
        echo "2. Go to https://railway.app and sign in"
        echo ""
        echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
        echo ""
        echo "4. Select your repository"
        echo ""
        echo "5. Set Root Directory to: backend"
        echo ""
        echo "6. Add environment variables in Railway dashboard:"
        echo "   - ENV=production"
        echo "   - API_RELOAD=false"
        echo "   - SUPABASE_URL=your_supabase_url"
        echo "   - SUPABASE_ANON_KEY=your_supabase_key"
        echo "   - SECRET_KEY=generate_random_key"
        echo "   - CORS_ORIGINS=https://your-frontend.com"
        echo ""
        echo "7. Railway will automatically deploy!"
        echo ""
        echo "8. Generate a public domain in Settings → Networking"
        echo ""
        echo "For detailed instructions, see: RAILWAY_DEPLOYMENT.md"
        ;;
        
    3)
        echo "Exiting..."
        exit 0
        ;;
        
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac

echo ""
echo "🎉 Done! Your backend should now be running on Railway."
echo ""
echo "Need help? Check out:"
echo "  - RAILWAY_DEPLOYMENT.md (detailed guide)"
echo "  - https://docs.railway.app"
echo "  - https://discord.gg/railway"
