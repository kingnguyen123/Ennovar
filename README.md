# Ennovar - Retail Sales Forecasting System

Ennovar is a comprehensive retail sales forecasting and analytics platform that combines machine learning predictions with real-time sales data visualization. The system provides inventory management insights, sales predictions, and interactive dashboards for retail business intelligence.

## 🎯 Features

- **Sales Forecasting**: Predict future sales based on historical data using AutoGluon ML models
- **Interactive Dashboard**: Real-time sales visualization with React and TailwindCSS
- **Multi-dimensional Filtering**: Filter data by category, subcategory, size, and timeframe
- **RESTful API**: Flask-based backend API for data access
- **SQLite Database**: Efficient data storage with 6.4M+ transaction records
- **Responsive UI**: Modern, mobile-friendly interface

## 🏗️ Project Structure

```
Ennovar/
├── app.py                  # Main Flask application entry point
├── backend/                # Backend API and utilities
│   ├── routes/            # API route blueprints
│   │   ├── products.py    # Product filtering endpoints
│   │   ├── sales.py       # Sales data endpoints
│   │   └── forecast.py    # Forecasting endpoints (placeholder)
│   └── utils/             # Utility functions
│       └── database.py    # Database query functions
├── frontend/              # React dashboard application
│   ├── src/
│   │   ├── App.jsx        # Main application component
│   │   └── components/    # React components
│   ├── package.json       # Frontend dependencies
│   └── vite.config.js     # Vite build configuration
├── database/              # Database setup and configuration
│   ├── database.db        # SQLite database file
│   ├── setup_database.py  # Database initialization script
│   └── DATABASE_SETUP.md  # Database documentation
├── model/                 # Machine learning models and notebooks
│   ├── retail_model.ipynb # ML model training notebook
│   └── Process_data.ipynb # Data processing notebook
└── test/                  # Test files
    └── test.py

```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/kingnguyen123/Ennovar.git
cd Ennovar
```

2. Install Python dependencies:
```bash
pip install -r requirement.txt
```

3. Set up the database (if needed):
```bash
python database/setup_database.py
```

4. Start the Flask backend:
```bash
python app.py
```

The backend API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📊 Technology Stack

### Backend
- **Flask**: Web framework for API endpoints
- **Flask-CORS**: Cross-origin resource sharing
- **SQLite**: Database for data storage
- **Pandas**: Data manipulation and analysis
- **AutoGluon**: Machine learning for forecasting

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool and development server
- **TailwindCSS**: Utility-first CSS framework

### ML/Data Science
- **AutoGluon**: Automated machine learning
- **Pandas**: Data processing
- **NumPy**: Numerical computations
- **Matplotlib**: Data visualization

## 📚 Documentation

- [API Documentation](docs/API.md) - Detailed API endpoint documentation
- [Database Setup](database/DATABASE_SETUP.md) - Database schema and setup guide
- [Architecture](docs/ARCHITECTURE.md) - System architecture overview
- [Frontend Guide](docs/FRONTEND.md) - Frontend component documentation
- [ML Models](docs/MODEL.md) - Machine learning model documentation

## 🔌 API Overview

The backend provides RESTful API endpoints for:

- **Product Filters**: `/api/products/categories`, `/api/products/sub_categories`, `/api/products/size`
- **Sales Data**: `/api/sales/subcategory`, `/api/sales/year-range`
- **Forecasting**: (Coming soon)

See [API.md](docs/API.md) for complete API documentation.

## 🗄️ Database

The system uses SQLite with the following main tables:
- **products**: Product catalog with categories and pricing
- **transactions**: Sales transaction records (6.4M+ records)
- **stores**: Store location information
- **discounts**: Discount campaign data

See [DATABASE_SETUP.md](database/DATABASE_SETUP.md) for detailed database documentation.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is private and proprietary.

## 👥 Authors

- King Nguyen (@kingnguyen123)

## 🙏 Acknowledgments

- AutoGluon team for the excellent ML framework
- React and Vite communities for modern web development tools
