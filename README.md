# Mini App - FastAPI + DBZero Template

A template FastAPI application with DBZero database integration, designed to provide a quick start for building applications with persistent data storage.

## 🚀 Features

- **FastAPI** - Modern, fast web framework for building APIs
- **DBZero Integration** - Persistent database storage with automatic connection management
- **Docker Support** - Containerized deployment using local DBZero package
- **Configuration Management** - Environment-based configuration with Pydantic
- **Health Checks** - Built-in health monitoring endpoints
- **API Documentation** - Automatic OpenAPI/Swagger documentation

## 📁 Project Structure

```
mini_app/
├── mini_app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application with endpoints
│   ├── config.py            # Configuration management
│   └── settings.py          # Pydantic settings model
├── packages/                # Local DBZero package directory
│   └── dbzeroce-0.0.1-cp311-cp311-linux_x86_64.whl
├── Dockerfile               # Docker build using local package
├── docker-compose.yml       # Development docker compose
├── build_and_run.sh         # Build and run script
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project metadata
└── README.md               # This file
```

## 🛠️ Prerequisites

1. **DBZero Local Package**: The DBZero wheel file is located in the `packages/` directory
2. **Docker**: For containerized deployment
3. **Linux with Python 3.11**: Required for local development (DBZero package is built for Linux x86_64)

## 🏃 Quick Start

### Option 1: Using the Build Script (Recommended)

The easiest way to get started:

```bash
# Build and run the application
./build_and_run.sh

# Or step by step:
./build_and_run.sh --build    # Build image only
./build_and_run.sh --run      # Run container only
./build_and_run.sh --logs     # View logs
./build_and_run.sh --stop     # Stop container
./build_and_run.sh --clean    # Clean up everything
```

### Option 2: Using Docker Compose

For development with automatic code reloading:

```bash
# Start the application
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Option 3: Manual Docker Commands

```bash
# Build the image
docker build -t mini_app .

# Run the container
docker run -d \
  --name mini_app_container \
  -p 8080:8080 \
  -v mini_app_data:/mini_app_data \
  mini_app
```

### Option 4: Local Development (Linux + Python 3.11 only)

For local development without Docker (Linux systems with Python 3.11):

```bash
# Install dependencies
pip install -r requirements.txt

# Install DBZero from local package
pip install packages/dbzeroce-0.0.1-cp311-cp311-linux_x86_64.whl

# Run the application
python -m mini_app.main
```

**Note**: Local development is only supported on Linux systems with Python 3.11 due to the compiled nature of the DBZero package.

## 🌐 Accessing the Application

Once running, the application is available at:

- **Main Application**: http://localhost:8080
- **API Documentation**: http://localhost:8080/docs
- **Alternative API Docs**: http://localhost:8080/redoc
- **Health Check**: http://localhost:8080/healthcheck

## 📡 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/`      | Root endpoint with basic information |
| GET    | `/healthcheck` | Health check with DBZero status |

### Example API Usage

```bash
# Health check
curl http://localhost:8080/healthcheck

# Root endpoint
curl http://localhost:8080/

# API Documentation
curl http://localhost:8080/docs
```

## ⚙️ Configuration

The application uses environment variables for configuration. Create a `.env` file in the root directory:

```env
# Database Configuration
INSTANCE_TYPE=R/W
CACHE_SIZE=1
DB_DIR=/mini_app_data/

# Application Configuration
APP_NAME=Mini App
APP_VERSION=0.1.0
DEBUG=true

# Server Configuration
HOST=0.0.0.0
PORT=8080
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `INSTANCE_TYPE` | `R/W` | Database instance type (`READONLY` or `R/W`) |
| `CACHE_SIZE` | `1` | Cache size in GiB |
| `DB_DIR` | `/mini_app_data/` | Database directory path |
| `DEBUG` | `true` | Enable debug mode |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8080` | Server port |

## 🏗️ Development

### Project Structure Explained

- **`mini_app/main.py`**: Main FastAPI application with all endpoints and DBZero integration
- **`mini_app/config.py`**: Configuration management and DBZero setup
- **`mini_app/settings.py`**: Pydantic models for settings validation
- **`packages/`**: Directory containing the local DBZero wheel package
- **`Dockerfile`**: Docker build configuration using local DBZero package
- **`build_and_run.sh`**: Convenient script for building and running with package validation

### Adding New Endpoints

1. Add your endpoint to `mini_app/main.py`
2. Use the existing DBZero connection pattern
3. Add appropriate Pydantic models for request/response
4. Update this README with new endpoint documentation

### DBZero Integration Pattern

```python
# In your endpoint functions:
try:
    # Ensure connection is active
    Connection.assure_initialized()
    
    # Your DBZero operations here
    # Example: read/write operations
    
    return result
except Exception as e:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Operation failed: {str(e)}"
    )
```

## 🐳 Docker Details

### Multi-stage Build

The Dockerfile uses a multi-stage build:

1. **Stage 1**: Copies DBZero package from `dbzero_ce_package` image
2. **Stage 2**: Sets up the application environment and copies the package

### Volumes

- **`mini_app_data`**: Persistent storage for DBZero database files
- **Source code mount** (in docker-compose): For development hot-reloading

### Health Checks

The container includes health checks that verify:
- Application is responding
- DBZero connection is healthy
- API endpoints are accessible

## 🔧 Troubleshooting

### Common Issues

1. **DBZero package not found**
   ```
   ERROR: DBZero package image 'dbzero_ce_package' not found!
   ```
   **Solution**: Build the DBZero package first (see Prerequisites)

2. **Port already in use**
   ```
   Error: Port 8080 is already in use
   ```
   **Solution**: Stop existing containers or change the port in configuration

3. **Permission denied on script**
   ```
   Permission denied: ./build_and_run.sh
   ```
   **Solution**: Make script executable: `chmod +x build_and_run.sh`

4. **Container fails to start**
   **Solution**: Check logs with `./build_and_run.sh --logs`

### Viewing Logs

```bash
# Using the script
./build_and_run.sh --logs

# Using Docker directly
docker logs -f mini_app_container

# Using Docker Compose
docker-compose logs -f
```

### Debugging

For debugging, you can run the container in interactive mode:

```bash
docker run -it --rm \
  -p 8080:8080 \
  -v mini_app_data:/mini_app_data \
  mini_app /bin/bash
```

## 📝 License

This is a template project. Add your license information here.

## 🤝 Contributing

This is a template project. Add your contribution guidelines here.

## 📞 Support

For issues related to:
- **DBZero**: Check the DBZero documentation
- **FastAPI**: Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
- **This template**: Create an issue in the project repository

---

**Happy coding! 🎉**
