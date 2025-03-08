# Drivenets Authentication Demo with React, FastAPI, and Nginx

This project demonstrates a simple authentication system with the following components:

1. **React Client**: A frontend application for user login and accessing protected data
2. **Auth Service**: A Python FastAPI service that handles authentication and token generation
3. **Backend Service**: A Python FastAPI service that provides protected data
4. **Nginx**: A reverse proxy that routes requests between the client and services

## Architecture

- The React client is served as static files by Nginx
- Nginx routes API requests to the appropriate backend services
- The backend service validates authentication tokens with the auth service

## Routes

1. `/auth/login` - Client login endpoint
2. `/validate` - Internal endpoint for token validation
3. `/api/data` - Protected backend endpoint that requires authentication

## Getting Started

### Prerequisites

- Docker and Docker Compose 

### Running the Application

1. Clone this repository
2. Build the React client:
   ```bash
   ./build-client.sh
   ```
3. Run the application with Docker Compose:
   ```bash
   # For Docker Compose v2 
   docker compose up --build
   ```
4. Access the application at http://localhost:3001 

## Test Credentials

The application comes with two test users:

- Username: `user1`, Password: `password1`
- Username: `user2`, Password: `password2`

## Project Structure

```
.
├── client/                 # React frontend source code
├── auth-service/           # Authentication service (FastAPI)
├── backend-service/        # Backend API service (FastAPI)
├── nginx/                  # Nginx configuration
└── docker-compose.yml      # Docker Compose configuration
```

## Nginx Configuration

This project includes two separate nginx configurations that serve different purposes:

1. **Main Nginx** (`./nginx/nginx.conf`):
   - Used by the nginx service defined in docker-compose.yml
   - Serves as the primary reverse proxy for the entire application
   - Routes requests to the appropriate backend services
   - Serves the React static files from the mounted volume
   - Includes configurations for FastAPI documentation endpoints

2. **Client Nginx** (`./client/nginx/default.conf`):
   - Defined in the client's Dockerfile
   - Not actively used in the default docker-compose setup
   - Provides a standalone deployment option for the client
   - Would be used if I build and run the client container separately
   - Contains simpler routing rules that proxy to the main nginx

This dual configuration provides flexibility in deployment options:
- The integrated approach (using main nginx) is simpler for development
- The standalone client approach would be useful for production scenarios where I might want to scale or deploy components separately


## Security Notes

This is a demonstration project and includes several simplifications that would not be appropriate for a production environment:

- Hardcoded credentials 
- Simple token validation (should implement proper OAuth/OIDC)
- Basic error handling
- No HTTPS configuration

