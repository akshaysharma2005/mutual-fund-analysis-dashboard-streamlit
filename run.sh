#!/bin/bash
# Convenient one-click launcher for the Mutual Fund Streamlit Dashboard
echo "🚀 Launching Apex Mutual Fund Intelligence Dashboard..."

# Navigate to script directory
cd "$(dirname "$0")"

# Check if .venv exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install streamlit pandas plotly scikit-learn openpyxl altair numpy
fi

echo "✨ Starting Streamlit on http://localhost:8501..."
streamlit run app.py --server.port 8501 --browser.gatherUsageStats false
