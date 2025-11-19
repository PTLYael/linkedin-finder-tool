# Lead LinkedIn Profile Checker

## Overview
This is a Flask web application that automates finding LinkedIn profiles and job titles for a list of people. Users upload an Excel file with a "Full Name" column, and the app uses the Tavily API for web searches and OpenAI's GPT model to identify LinkedIn profiles, extract job roles, and provide confidence scores.

## Current State
- **Language**: Python 3.11
- **Framework**: Flask (web application)
- **Port**: 5000 (frontend)
- **Status**: Setup complete, awaiting API keys

## Recent Changes (November 19, 2025)
- Installed Python 3.11 and all required dependencies
- Updated port from 7860 to 5000 for Replit compatibility
- Created .gitignore for Python project
- Configured workflow to run Flask application
- Created project documentation

## Project Architecture
### Structure
- `name.py` - Main Flask application with routes and logic
- `templates/index.html` - Upload form for Excel files
- `requirements.txt` - Python dependencies

### Dependencies
- Flask - Web framework
- OpenAI - GPT model integration for profile analysis
- Pandas - Excel file reading/writing
- Openpyxl - Excel file engine
- Requests - HTTP requests to Tavily API

### External Services
- **OpenAI API**: Used to analyze search results and extract LinkedIn profile information
- **Tavily API**: Used to perform web searches for LinkedIn profiles

### How It Works
1. User uploads Excel file with "Full Name" column
2. For each name, the app searches LinkedIn using Tavily API
3. OpenAI analyzes the search results to extract:
   - LinkedIn profile URL
   - Job role/title
   - Confidence score (0-100)
4. Results are exported to a new Excel file for download

## Required Environment Variables
- `OPENAI_API_KEY` - OpenAI API key for GPT model access
- `TAVILY_API_KEY` - Tavily API key for web search functionality
- `PORT` - Server port (defaults to 5000)

## User Preferences
None documented yet.
