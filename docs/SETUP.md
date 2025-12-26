# Setup and Installation Guide

This guide provides step-by-step instructions for setting up the Ennovar retail sales forecasting system on your local machine.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Prerequisites](#prerequisites)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Database Setup](#database-setup)
6. [Running the Application](#running-the-application)
7. [Development Environment](#development-environment)
8. [Troubleshooting](#troubleshooting)
9. [Production Deployment](#production-deployment)

---

## System Requirements

### Minimum Requirements

- **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **RAM**: 8 GB (16 GB recommended for ML model training)
- **Storage**: 5 GB free space (10 GB+ for full dataset)
- **CPU**: Multi-core processor (4+ cores recommended)

### Software Requirements

- **Python**: 3.11 or higher
- **Node.js**: 18.0 or higher
- **npm**: 9.0 or higher (comes with Node.js)
- **Git**: Latest version

---

## Prerequisites

### 1. Install Python 3.11+

**Windows**:
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Verify installation:
```bash
python --version
```

**macOS**:
```bash
# Using Homebrew
brew install python@3.11

# Verify
python3 --version
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install python3.11 python3-pip python3-venv

# Verify
python3 --version
```

### 2. Install Node.js and npm

**Windows/macOS**:
1. Download from [nodejs.org](https://nodejs.org/)
2. Run installer
3. Verify installation:
```bash
node --version
npm --version
```

**Linux (Ubuntu/Debian)**:
```bash
# Using NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version
npm --version
```

### 3. Install Git

**Windows**: Download from [git-scm.com](https://git-scm.com/)

**macOS**:
```bash
brew install git
```

**Linux**:
```bash
sudo apt-get install git
```

---

## Backend Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kingnguyen123/Ennovar.git
cd Ennovar
```

### 2. Create Python Virtual Environment

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirement.txt
```

**Dependencies installed**:
- `flask` - Web framework
- `flask-cors` - CORS support
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `autogluon` - Machine learning
- `matplotlib` - Visualization
- `holidays` - Holiday detection
- `transformers` - NLP models
- `datasets` - Dataset utilities
- `einops` - Tensor operations
- `tqdm` - Progress bars
- `pyyaml` - YAML parsing
- `boto3` - AWS SDK

**Note**: AutoGluon installation may take several minutes as it includes many dependencies.

### 4. Verify Backend Installation

```bash
python -c "import flask; print('Flask:', flask.__version__)"
python -c "import pandas; print('Pandas:', pandas.__version__)"
python -c "import autogluon; print('AutoGluon installed successfully')"
```

---

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Node.js Dependencies

```bash
npm install
```

**Dependencies installed**:
- `react` - UI framework
- `react-dom` - React DOM rendering
- `vite` - Build tool
- `@vitejs/plugin-react` - React plugin for Vite
- `tailwindcss` - CSS framework
- `postcss` - CSS processing
- `autoprefixer` - CSS vendor prefixes

### 3. Verify Frontend Installation

```bash
npm list react
npm list vite
```

---

## Database Setup

### Option 1: Use Existing Database

If `database/database.db` exists, you can use it directly. Skip to [Running the Application](#running-the-application).

### Option 2: Create New Database

If you need to set up the database from CSV files:

1. **Prepare Data Files**

Place CSV files in the `data/` directory:
```
data/
├── products.csv
├── transactions.csv
├── stores.csv
└── discounts.csv
```

2. **Run Database Setup Script**

**Note**: Run this command from the project root directory.

```bash
# From project root
python database/setup_database.py
```

Expected output:
```
✓ Connected to database: /path/to/database.db
✓ Created 'products' table
✓ Created 'discounts' table
✓ Created 'stores' table
✓ Created 'transactions' table
✓ All tables created successfully

Loading CSV files into database...
✓ Loaded 17940 rows into 'products' table
✓ Loaded 181 rows into 'discounts' table
✓ Loaded 35 rows into 'stores' table
✓ Loaded 6416827 rows into 'transactions' table
✓ Database setup complete
```

3. **Verify Database**

```bash
# Open SQLite shell
sqlite3 database/database.db

# Check tables
.tables

# Check row counts
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM transactions;

# Exit
.exit
```

---

## Running the Application

### 1. Start Backend Server

**Terminal 1** (from project root):
```bash
# Activate virtual environment (if not already active)
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Start Flask server
python app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

**✅ Backend is now running on http://localhost:5000**

### 2. Start Frontend Server

**Terminal 2** (from project root):
```bash
cd frontend
npm run dev
```

Expected output:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**✅ Frontend is now running on http://localhost:5173**

### 3. Access the Application

Open your browser and navigate to:
```
http://localhost:5173
```

You should see the Ennovar dashboard!

---

## Development Environment

### Recommended IDE Setup

**Visual Studio Code**:
1. Install VS Code from [code.visualstudio.com](https://code.visualstudio.com/)
2. Install recommended extensions:
   - Python
   - Pylance
   - ES7+ React/Redux/React-Native snippets
   - Tailwind CSS IntelliSense
   - ESLint
   - Prettier

**PyCharm** (Alternative for Python):
- Professional or Community edition
- Good for backend development

### Environment Variables (Optional)

Create `.env` files for configuration:

**Backend** (`.env` in project root):
```env
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_PATH=database/database.db
```

**Frontend** (`frontend/.env.development`):
```env
VITE_API_BASE_URL=http://localhost:5000
```

### Git Configuration

Set up Git for development:
```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create a new branch for development
git checkout -b feature/your-feature-name
```

---

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# Reinstall dependencies
pip install -r requirement.txt
```

---

**Issue**: `sqlite3.OperationalError: no such table: products`

**Solution**:
```bash
# Run database setup
python database/setup_database.py
```

---

**Issue**: Port 5000 already in use

**Solution**:
```bash
# Option 1: Change port in app.py
# app.run(debug=True, port=5001)

# Option 2: Kill process on port 5000 (macOS/Linux)
lsof -ti:5000 | xargs kill -9

# Option 2: Kill process on port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

**Issue**: AutoGluon installation fails

**Solution**:
```bash
# Install AutoGluon with specific dependencies
pip install autogluon.timeseries

# Or install minimal version
pip install autogluon.core autogluon.features autogluon.tabular
```

---

### Frontend Issues

**Issue**: `npm ERR! code ENOENT`

**Solution**:
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

**Issue**: Port 5173 already in use

**Solution**:
```bash
# Vite will automatically try the next available port
# Or specify a different port in vite.config.js:

export default defineConfig({
  server: {
    port: 3000
  }
})
```

---

**Issue**: Blank page or React errors

**Solution**:
```bash
# Clear Vite cache
rm -rf node_modules/.vite

# Rebuild
npm run dev
```

---

**Issue**: API calls fail with CORS errors

**Solution**:
1. Ensure Flask-CORS is installed: `pip install flask-cors`
2. Verify CORS is enabled in `app.py`:
```python
from flask_cors import CORS
CORS(app)
```

---

### Database Issues

**Issue**: Database locked error

**Solution**:
```bash
# Ensure no other processes are accessing the database
# Close any SQLite browser tools
# Restart the Flask application
```

---

**Issue**: Large database file (>1GB)

**Solution**:
```bash
# Vacuum the database to reclaim space
sqlite3 database/database.db "VACUUM;"
```

---

## Production Deployment

### Backend Deployment

1. **Use Production WSGI Server**

Install Gunicorn:
```bash
pip install gunicorn
```

Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Configure Environment**

Create `.env.production`:
```env
FLASK_ENV=production
DATABASE_PATH=/var/www/ennovar/database/database.db
```

3. **Use PostgreSQL (Recommended)**

For production, migrate from SQLite to PostgreSQL:
```bash
pip install psycopg2-binary
```

### Frontend Deployment

1. **Build for Production**

```bash
cd frontend
npm run build
```

2. **Deploy Static Files**

Upload `dist/` folder to:
- Netlify
- Vercel
- AWS S3 + CloudFront
- GitHub Pages

3. **Configure Environment**

Create `frontend/.env.production`:
```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

### Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirement.txt .
RUN pip install -r requirement.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t ennovar-backend .
docker run -p 5000:5000 ennovar-backend
```

---

## Next Steps

After successful setup:

1. **Read Documentation**
   - [API Documentation](API.md)
   - [Architecture](ARCHITECTURE.md)
   - [Frontend Guide](FRONTEND.md)
   - [ML Models](MODEL.md)

2. **Explore the Code**
   - Backend routes in `backend/routes/`
   - Frontend components in `frontend/src/components/`
   - Database utilities in `backend/utils/database.py`

3. **Test the API**
   - Use curl or Postman to test endpoints
   - Check API documentation for examples

4. **Customize**
   - Modify components
   - Add new features
   - Train ML models

---

## Support

For issues or questions:
- Check [Troubleshooting](#troubleshooting) section
- Review [GitHub Issues](https://github.com/kingnguyen123/Ennovar/issues)
- Contact: @kingnguyen123

---

## Quick Reference

```bash
# Activate virtual environment
source venv/bin/activate         # macOS/Linux
venv\Scripts\activate             # Windows

# Start backend (port 5000)
python app.py

# Start frontend (port 5173)
cd frontend && npm run dev

# Run tests
python test/test.py

# Build frontend for production
cd frontend && npm run build

# Database setup
python database/setup_database.py
```
