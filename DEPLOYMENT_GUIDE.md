# 🚀 Deploy to Render (Beginner-Friendly)

This guide will help you deploy your Bell Canada B2B API to Render for free!

## 📋 Prerequisites

- A free Render account (sign up at https://render.com)
- Your project files ready

## 🎯 Step-by-Step Deployment

### Step 1: Create Render Account
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with your email or GitHub (optional)

### Step 2: Create New Web Service
1. In your Render dashboard, click "New +"
2. Select "Web Service"
3. Choose "Build and deploy from a Git repository" (we'll use manual deploy instead)

### Step 3: Manual Deployment (Easiest Method)
1. Click "New +" → "Web Service"
2. Choose "Deploy from existing code"
3. Give your service a name: `bell-canada-api`
4. Choose "Python" as the environment
5. Set the build command: `pip install -r requirements.txt`
6. Set the start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 4: Add PostgreSQL Database
1. In your Render dashboard, click "New +"
2. Select "PostgreSQL"
3. Name it: `bell-canada-db`
4. Choose the free plan
5. Note down the connection details

### Step 5: Connect Database to Your Service
1. Go back to your web service
2. Click "Environment" tab
3. Add environment variable:
   - Key: `DATABASE_URL`
   - Value: Copy from your PostgreSQL service (looks like: `postgresql://user:password@host:port/database`)

### Step 6: Upload Your Files
1. In your web service, go to "Manual Deploy" tab
2. Click "Upload Files"
3. Select all files from your `bell-canada-api` folder
4. Click "Deploy"

### Step 7: Wait for Deployment
1. Render will build and deploy your service
2. This takes 2-5 minutes
3. You'll see logs showing the deployment progress

### Step 8: Test Your API
1. Once deployed, click on your service URL
2. Add `/health` to test: `https://your-app.onrender.com/health`
3. Add `/docs` to see API documentation: `https://your-app.onrender.com/docs`

## 🔧 Troubleshooting

### Common Issues:

**1. Build Fails**
- Check that all files are uploaded
- Verify `requirements.txt` exists
- Check the build logs for errors

**2. Database Connection Fails**
- Verify `DATABASE_URL` environment variable is set
- Check that PostgreSQL service is running
- Ensure connection string format is correct

**3. API Returns Errors**
- Check the service logs
- Verify the database has data loaded
- Test the `/health` endpoint first

## 📞 Getting Help

- **Render Documentation**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Service Logs**: Check the "Logs" tab in your service dashboard

## 🎉 Success!

Once deployed, your API will be available at:
- **API Base**: `https://your-app-name.onrender.com`
- **Documentation**: `https://your-app-name.onrender.com/docs`
- **Health Check**: `https://your-app-name.onrender.com/health`

## 🔄 Updating Your API

To update your API:
1. Make changes to your local files
2. Go to your Render service
3. Click "Manual Deploy" → "Upload Files"
4. Select your updated files
5. Click "Deploy"

## 💰 Free Tier Limits

- **750 hours/month** (enough for 24/7 usage)
- **512MB RAM** per service
- **Shared CPU**
- **PostgreSQL**: 1GB storage, 90 days retention

Perfect for learning and practice! 🚀 