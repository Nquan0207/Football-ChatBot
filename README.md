# 🤖 AI Chatbot with RAG

A high-performance, asynchronous chatbot application with Retrieval-Augmented Generation (RAG) capabilities, built with modern technologies.

## 🚀 Features

- **High-Performance Backend**: FastAPI with Python 3.12 and async/await
- **RAG Integration**: OpenAI + LangChain for intelligent document retrieval
- **Modern Frontend**: React + TypeScript + Vite + Tailwind CSS + shadcn/ui
- **Containerized**: Docker & Docker Compose for easy deployment
- **Vector Database**: ChromaDB for efficient document storage and retrieval
- **Real-time Chat**: WebSocket-ready architecture
- **Document Upload**: Support for multiple document formats
- **Session Management**: Persistent chat sessions
- **Health Monitoring**: Built-in health checks and monitoring

## 🏗️ Architecture

```
chatbot/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration & logging
│   │   ├── models/         # Pydantic models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript types
│   │   └── lib/            # Utility functions
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml      # Multi-container setup
└── README.md
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance web framework
- **Python 3.12** - Latest Python version
- **Uvicorn** - ASGI server
- **Pydantic v2** - Data validation
- **OpenAI** - LLM integration
- **LangChain** - RAG framework
- **ChromaDB** - Vector database
- **PostgreSQL** - Primary database
- **Redis** - Caching layer

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library
- **Axios** - HTTP client
- **React Router** - Navigation

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- OpenAI API key

### 1. Clone the Repository
```bash
git clone <repository-url>
cd chatbot
```

### 2. Set Environment Variables
```bash
# Copy environment files
cp backend/env.example backend/.env
cp frontend/env.example frontend/.env

# Edit backend/.env and add your OpenAI API key
OPENAI_API_KEY=your-openai-api-key-here
```

### 3. Start the Application
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📚 API Endpoints

### Chat Endpoints
- `POST /api/v1/chat/message` - Send a message
- `GET /api/v1/chat/history/{session_id}` - Get chat history
- `DELETE /api/v1/chat/history/{session_id}` - Clear chat history

### RAG Endpoints
- `POST /api/v1/rag/documents` - Upload documents
- `GET /api/v1/rag/stats` - Get RAG statistics
- `POST /api/v1/rag/search` - Search documents

### Health Endpoints
- `GET /health` - Health check
- `GET /api/v1/health/ready` - Readiness check

## 🔧 Development

### Backend Development
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📦 Docker Commands

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and start
docker-compose up -d --build

# View specific service logs
docker-compose logs -f backend

# Access container shell
docker-compose exec backend bash
docker-compose exec frontend sh
```

## 🔒 Security

- Environment variables for sensitive data
- CORS configuration
- Input validation with Pydantic
- Rate limiting (can be added)
- JWT authentication (can be added)

## 📊 Monitoring

- Health checks for all services
- Structured logging
- Performance metrics
- Error tracking

## 🚀 Deployment

### Production Deployment
1. Set production environment variables
2. Use production Docker images
3. Configure reverse proxy (Nginx)
4. Set up SSL certificates
5. Configure monitoring and logging

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your-production-openai-key
SECRET_KEY=your-production-secret-key

# Optional
DATABASE_URL=your-production-database-url
REDIS_URL=your-production-redis-url
LOG_LEVEL=INFO
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the health endpoints

## 🔮 Roadmap

- [ ] User authentication
- [ ] Multi-language support
- [ ] Advanced RAG features
- [ ] WebSocket real-time chat
- [ ] File upload improvements
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] Advanced monitoring 