# Chat NHM

A modern, AI-powered portfolio website where visitors can ask natural language questions about your work, skills, and experience. Built with Django, Vue.js, and powered by RAG (Retrieval-Augmented Generation) for intelligent responses.

## Features

- **Conversational Interface**: Natural language chat interface powered by OpenAI GPT-4
- **RAG-Powered Responses**: Contextual answers based on your actual portfolio content
- **Multi-Modal Content**: Images, videos, project showcases, and interactive elements
- **Real-Time Chat**: Instant responses with typing indicators and message history
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Admin Interface**: Easy content management through Django admin

## Tech Stack

### Backend
- **Django** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database with pgvector for embeddings
- **OpenAI API** - Language model and embeddings
- **LangChain** - RAG implementation
- **Celery** - Background task processing
- **Redis** - Caching and message broker

### Frontend
- **Vue.js 3** - Frontend framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Pinia** - State management
- **Vite** - Build tool

### Deployment
- **Heroku** - Hosting platform
- **Cloudinary** - Media storage and optimization

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL
- Redis (for development)

### 1. Backend Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd chat-nhm

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Generate embeddings for your content
python manage.py generate_embeddings

# Start development server
python manage.py runserver
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Visit http://localhost:5173 to see your conversational portfolio!

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Required
SECRET_KEY=your-django-secret-key
OPENAI_API_KEY=your-openai-api-key

# Optional for development
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/portfolio_db
CLOUDINARY_CLOUD_NAME=your-cloudinary-name
CLOUDINARY_API_KEY=your-cloudinary-key
CLOUDINARY_API_SECRET=your-cloudinary-secret
```

### Content Management

1. Access Django admin at http://localhost:8000/admin
2. Add your personal information, projects, skills, and experiences
3. Run `python manage.py generate_embeddings` to create searchable content

## Deployment to Heroku

### 1. Prepare for Deployment

```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-portfolio-name

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# Add Redis addon
heroku addons:create heroku-redis:mini

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set OPENAI_API_KEY="your-openai-key"
heroku config:set DEBUG=False
```

### 2. Deploy

```bash
# Deploy to Heroku
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Generate embeddings
heroku run python manage.py generate_embeddings
```

### 3. Frontend Build

Build and serve the frontend:

```bash
cd frontend
npm run build
# Copy dist/ contents to Django static files or serve separately
```

## Architecture

### RAG Implementation

1. **Content Ingestion**: Portfolio content is processed into embeddings
2. **Query Processing**: User questions are converted to embeddings
3. **Retrieval**: Relevant content is found using cosine similarity
4. **Generation**: LLM generates contextual responses with references
5. **Multi-Modal Enhancement**: Responses include images, videos, and links

### Database Schema

- **Projects**: Portfolio projects with media and case studies
- **Skills**: Technical and soft skills with proficiency levels
- **Experience**: Work history and achievements
- **Chat Sessions**: Conversation history and analytics
- **Embeddings**: Vector representations for semantic search

## Customization

### Adding New Content Types

1. Create model in `content/models.py`
2. Add admin interface in `content/admin.py`
3. Update embedding service in `rag_service/embedding_service.py`
4. Create frontend components for display

### Styling

- Modify `frontend/src/style.css` for global styles
- Update `frontend/tailwind.config.js` for theme customization
- Component styles are in individual `.vue` files

## Commands

```bash
# Django management commands
python manage.py generate_embeddings           # Generate all embeddings
python manage.py generate_embeddings --content-type=project  # Specific type

# Frontend commands
npm run dev          # Development server
npm run build        # Production build
npm run preview      # Preview production build
```

## API Endpoints

### Chat API
- `POST /api/chat/sessions/` - Create new chat session
- `GET /api/chat/sessions/{id}/` - Get session details
- `POST /api/chat/sessions/{id}/send_message/` - Send message

### Content API
- `GET /api/content/projects/` - List projects
- `GET /api/content/skills/` - List skills
- `GET /api/content/experience/` - List experience
- `GET /api/content/profile/profile/` - Get personal info

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or support, please open an issue on GitHub or contact the maintainer.
