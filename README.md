# YouTube Downloader

A modern YouTube downloader built with **FastAPI**, **FFmpeg**, and a frontend designed for a simple and clean downloading experience.

## Features

* YouTube video downloading
* Video information and metadata analysis
* Multiple media formats
* Audio/video processing with FFmpeg
* Input URL validation
* Automatic download-file cleanup
* REST API built with FastAPI
* Dockerized backend
* CORS support for frontend integration
* API documentation through Swagger UI
* Automated backend tests

## Tech Stack

### Backend

* Python 3.11
* FastAPI
* Uvicorn
* Pydantic
* FFmpeg
* yt-dlp
* Pytest

### Frontend

* React
* Vite
* JavaScript
* CSS

### Deployment

* Docker
* GitHub
* Render — backend
* Vercel — frontend

## Project Structure

```text
youtube-downloader/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── test_analyze.py
│   │   ├── test_download.py
│   │   ├── test_health.py
│   │   └── test_validators.py
│   │
│   └── downloads/
│
├── frontend/
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Running Locally

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd youtube-downloader
```

### 2. Create a virtual environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the backend

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## Docker

The backend is containerized and includes FFmpeg for media processing.

### Build the image

From the project root:

```bash
docker build -t youtube-downloader .
```

### Run the container

```bash
docker run --rm -p 8000:8000 youtube-downloader
```

The application will then be available at:

```text
http://localhost:8000
```

## Environment Variables

Environment-specific configuration should be stored in `.env` files locally and configured through the deployment platform in production.

Example:

```env
PROJECT_NAME=YouTube Downloader
API_V1_STR=/api/v1
ALLOWED_ORIGINS=http://localhost:5173
```

For the frontend, the production backend URL can be provided through a Vercel environment variable:

```env
VITE_API_URL=https://your-backend-url.onrender.com
```

Never commit real secrets or private environment variables to GitHub.

## API

The backend exposes versioned API routes under:

```text
/api/v1
```

The available endpoints can be explored through the FastAPI Swagger interface:

```text
/docs
```

The API provides functionality for:

* Health checks
* Video analysis
* Download requests
* Download validation
* Media processing

## Testing

Run the backend tests from the project root:

```bash
pytest backend/tests
```

For a more detailed output:

```bash
pytest -v backend/tests
```

## Docker Deployment

The backend is designed to be deployed as a Docker Web Service.

The production architecture is:

```text
User
 │
 ▼
Frontend
 │
 │ HTTPS
 ▼
FastAPI Backend
 │
 ├── YouTube Service
 │
 ├── Download Service
 │
 └── FFmpeg
 │
 ▼
Processed Media
```

The backend can be deployed to **Render**, while the frontend can be deployed separately to **Vercel**.

## Important Note About Downloads

Downloaded media files are treated as temporary application data rather than permanent storage.

The application includes cleanup functionality to prevent the download directory from continuously accumulating media files.

Production deployments should not rely on the container filesystem as permanent storage.

## Development

Contributions and improvements are welcome.

Before submitting changes:

1. Create a feature branch.
2. Make your changes.
3. Run the test suite.
4. Verify the Docker build.
5. Commit your changes.
6. Push the branch.
7. Open a pull request.

Example:

```bash
git checkout -b feature/your-feature
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature
```

## License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

## Disclaimer

This project is intended for legitimate use. Users are responsible for ensuring that their use of downloaded content complies with applicable laws, copyright requirements, and the terms of service of the platforms and content owners involved.
