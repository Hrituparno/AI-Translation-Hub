#!/bin/bash

# Startup script for IndiaTranslate
# Starts both API and UI servers

echo "🚀 Starting IndiaTranslate..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Start API server in background
echo "📡 Starting API server on port 8000..."
uvicorn api.main:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# Wait for API to start
sleep 3

# Start Streamlit UI
echo "🎨 Starting UI on port 8501..."
streamlit run ui/app.py --server.port 8501 &
UI_PID=$!

echo ""
echo "✅ IndiaTranslate is running!"
echo ""
echo "📡 API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🎨 UI: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for interrupt
trap "kill $API_PID $UI_PID; exit" INT
wait
