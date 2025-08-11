# Automotive Parts Pricing API

A FastAPI-based REST API for fetching automotive parts pricing information including installation costs, SRP (Suggested Retail Price), and insurance values. Now deployed and ready for production use!

## 🚀 Live Demo

Once deployed on Render, your API will be available at: `https://your-app-name.onrender.com`

## Features

- ✅ Complete automotive parts database with 16+ parts
- ✅ **Separate JSON data file** for easy data management
- ✅ **Auto-save functionality** - changes persist to JSON file
- ✅ **Production ready** - Configured for Render deployment
- ✅ **CORS enabled** - Ready for frontend integration
- ✅ Data reload capabilities
- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ Search parts by ID or name
- ✅ RESTful API design
- ✅ Pydantic models for request/response validation
- ✅ Error handling with custom exception handlers
- ✅ Health check endpoint
- ✅ Interactive API documentation (Swagger UI)
- ✅ Pre-populated database with real automotive parts data

## 🚀 Deployment on Render

This API is ready for deployment on Render. Follow these steps:

### Method 1: Using GitHub Integration (Recommended)

1. **Push to GitHub**: 
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Automotive Parts API"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to [Render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will automatically detect the configuration from `render.yaml`

### Method 2: Manual Configuration

If you prefer manual setup:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment**: Python 3.9

### Environment Variables

No additional environment variables are required. The app uses:
- `PORT` (automatically provided by Render)
- Auto-creates JSON data file if missing

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Project Structure

```
prices api/
├── main.py                  # FastAPI application
├── auto_parts_data.json     # Automotive parts database (JSON)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Data Management

The application uses a separate JSON file (`auto_parts_data.json`) to store automotive parts data. This provides several benefits:

- **Easy editing**: You can modify the data directly in the JSON file
- **Data persistence**: All changes via API are automatically saved
- **Version control**: Easy to track changes to the data
- **Backup/restore**: Simple to backup or restore the entire dataset

The API comes pre-loaded with the following automotive parts:

| ID | Part Name | Installation Cost | SRP | Insurance |
|----|-----------|------------------|-----|-----------|
| 1 | Back Door | ₱2,000.00 | ₱5,500.00 | ₱8,800.00 |
| 2 | Cargo | ₱5,500.00 | ₱11,000.00 | ₱17,800.00 |
| 3 | Door | ₱2,000.00 | ₱5,500.00 | ₱8,800.00 |
| 4 | Door Glass | ₱2,000.00 | ₱5,500.00 | ₱8,800.00 |
| 5 | Fender | ₱2,000.00 | ₱5,800.00 | ₱9,200.00 |
| 6 | Front Bumper | ₱1,500.00 | ₱3,500.00 | ₱5,600.00 |
| 7 | Front Grille | ₱1,500.00 | ₱3,500.00 | ₱5,600.00 |
| 8 | Headlamp | ₱1,500.00 | ₱3,500.00 | ₱5,600.00 |
| 9 | Hood | ₱2,000.00 | ₱4,000.00 | ₱6,400.00 |
| 10 | Side Mirror | ₱500.00 | ₱1,000.00 | ₱1,600.00 |
| 11 | Sliding Door | ₱2,000.00 | ₱5,800.00 | ₱9,200.00 |
| 12 | Stepboard | ₱1,500.00 | ₱3,500.00 | ₱5,600.00 |
| 13 | Tail Gate | ₱2,000.00 | ₱4,000.00 | ₱6,400.00 |
| 14 | Tail Lamp | ₱1,500.00 | ₱3,500.00 | ₱5,600.00 |
| 15 | Windshield | ₱500.00 | ₱1,800.00 | ₱3,500.00 |
| 16 | Sliding Panel | ₱2,000.00 | ₱5,800.00 | ₱7,200.00 |

## API Endpoints

### Basic Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check

### Data Management Endpoints
- `POST /reload-data` - Reload data from JSON file
- `POST /save-data` - Manually save current data to JSON file

### Automotive Parts CRUD Operations
- `GET /parts` - Get all automotive parts
- `GET /parts/{part_id}` - Get part by ID
- `GET /parts/name/{part_name}` - Search parts by name (case-insensitive)
- `POST /parts` - Create new automotive part (auto-saves to JSON)
- `PUT /parts/{part_id}` - Update part by ID (auto-saves to JSON)
- `DELETE /parts/{part_id}` - Delete part by ID (auto-saves to JSON)

## Example Usage

### Get all parts
```bash
curl -X GET "http://localhost:8000/parts"
```

### Get part by ID
```bash
curl -X GET "http://localhost:8000/parts/1"
```

### Search parts by name
```bash
curl -X GET "http://localhost:8000/parts/name/door"
```

### Reload data from JSON file
```bash
curl -X POST "http://localhost:8000/reload-data"
```

### Manually save data to JSON file
```bash
curl -X POST "http://localhost:8000/save-data"
```

### Create a new part
```bash
curl -X POST "http://localhost:8000/parts" \
     -H "Content-Type: application/json" \
     -d '{
       "thinsmith": "Rear Spoiler",
       "cost_installation_personal": 1200.00,
       "srp": 2800.00,
       "insurance": 4500.00
     }'
```

### Update a part
```bash
curl -X PUT "http://localhost:8000/parts/1" \
     -H "Content-Type: application/json" \
     -d '{
       "srp": 6000.00,
       "insurance": 9500.00
     }'
```

### Delete a part
```bash
curl -X DELETE "http://localhost:8000/parts/1"
```

## Data Models

### AutoPart
- `id`: Integer (auto-generated)
- `thinsmith`: String (part name)
- `cost_installation_personal`: Float (installation cost)
- `srp`: Float (suggested retail price)
- `insurance`: Float (insurance value)

## Response Examples

### Get all parts response:
```json
[
  {
    "id": 1,
    "thinsmith": "Back Door",
    "cost_installation_personal": 2000.0,
    "srp": 5500.0,
    "insurance": 8800.0
  },
  {
    "id": 2,
    "thinsmith": "Cargo",
    "cost_installation_personal": 5500.0,
    "srp": 11000.0,
    "insurance": 17800.0
  }
]
```

### Search by name response:
```json
[
  {
    "id": 1,
    "thinsmith": "Back Door",
    "cost_installation_personal": 2000.0,
    "srp": 5500.0,
    "insurance": 8800.0
  },
  {
    "id": 3,
    "thinsmith": "Door",
    "cost_installation_personal": 2000.0,
    "srp": 5500.0,
    "insurance": 8800.0
  }
]
```

## Production Considerations

For production use, consider:
- Implementing authentication and authorization
- Adding input validation and sanitization
- Setting up a proper database (PostgreSQL, MySQL, etc.)
- Implementing pagination for large datasets
- Adding logging and monitoring
- Setting up proper error handling
- Adding unit and integration tests
- Implementing rate limiting
- Adding API versioning
