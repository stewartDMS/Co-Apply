#!/bin/bash
# Test deployment script for Co-Apply
# This script tests the Flask API locally before deploying to Vercel

set -e

echo "🧪 Testing Co-Apply Deployment"
echo "=============================="
echo ""

# Check Python version
echo "1️⃣  Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "   ✅ Python $python_version"
echo ""

# Install dependencies if needed
echo "2️⃣  Checking dependencies..."
if ! python -c "import flask" 2>/dev/null; then
    echo "   Installing Flask..."
    pip install flask requests -q
fi
echo "   ✅ Dependencies OK"
echo ""

# Start Flask server in background
echo "3️⃣  Starting Flask server..."
export FLASK_APP=api/index.py
python -m flask run --port 5000 > /tmp/flask.log 2>&1 &
FLASK_PID=$!
echo "   Flask PID: $FLASK_PID"

# Wait for server to start
sleep 3

# Check if server is running
if ! curl -s http://127.0.0.1:5000/api/health > /dev/null; then
    echo "   ❌ Failed to start Flask server"
    kill $FLASK_PID 2>/dev/null || true
    exit 1
fi
echo "   ✅ Flask server started"
echo ""

# Run tests
echo "4️⃣  Running API tests..."
if python test_api.py; then
    echo ""
    echo "=============================="
    echo "✅ All tests passed!"
    echo "=============================="
    echo ""
    echo "Your API is ready for deployment to Vercel!"
    echo "Visit http://127.0.0.1:5000 to see the landing page"
    echo ""
    echo "To deploy:"
    echo "  1. Install Vercel CLI: npm install -g vercel"
    echo "  2. Run: vercel"
    echo "  3. Follow the prompts"
    echo ""
    TEST_RESULT=0
else
    echo ""
    echo "=============================="
    echo "❌ Tests failed"
    echo "=============================="
    echo ""
    TEST_RESULT=1
fi

# Clean up
echo "Stopping Flask server..."
kill $FLASK_PID 2>/dev/null || true

exit $TEST_RESULT
