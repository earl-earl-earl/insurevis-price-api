# Render Deployment Guide

## Quick Deploy Steps

1. **Create GitHub Repository**:
   - Create a new repository on GitHub
   - Push all files from the "prices api" folder to the repository

2. **Deploy on Render**:
   - Go to https://render.com
   - Sign up/Login with GitHub
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect the configuration

3. **Automatic Configuration**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3.9 (from runtime.txt)

## Files for Deployment

✅ main.py - FastAPI application
✅ requirements.txt - Dependencies
✅ Procfile - Process configuration
✅ render.yaml - Render configuration
✅ runtime.txt - Python version
✅ auto_parts_data.json - Data file
✅ .gitignore - Git ignore rules

## After Deployment

Your API will be available at:
- Base URL: `https://your-app-name.onrender.com`
- Documentation: `https://your-app-name.onrender.com/docs`
- Health Check: `https://your-app-name.onrender.com/health`

## Features

- Auto-scaling web service
- HTTPS enabled by default
- Automatic JSON data file creation
- CORS enabled for frontend integration
- Interactive API documentation
- Production-ready error handling
