# Kommo AI‑Chatbot

A self‑hosted FastAPI microservice + embeddable widget that serves an  
AI‑powered assistant using Google's Gemini API.
---
## 🚀 Getting Started

### 1. Prerequisites

- Clone the repository.
- Create a `.env` file and add your Gemini API key: `GEMINI_API_KEY=your_api_key_here`.
- Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

### 2. Running with Docker Compose (Recommended)

This is the easiest way to get the application running:

```bash
# Build and run the service
docker-compose up --build

# To run in the background
docker-compose up --build -d
```

The application will be available at http://localhost:8000.

### 3. Running Locally (for Development)

If you prefer to run the application directly on your machine for development purposes:

```bash
# 1. Create a virtual environment (e.g., named .venv). This only needs to be done once.
python3 -m venv .venv

# 2. Activate the environment. You must do this in every new terminal session before
#    running any other commands.
source .venv/bin/activate

# 3. Install all dependencies into the activated environment.
pip install -r requirements.txt

# 4. Set your Gemini API key as an environment variable:
export GEMINI_API_KEY=your_api_key_here

# 5. Run the FastAPI server from the activated environment.
uvicorn app.main:app --reload --reload-exclude ".venv/*"

# When you are finished, stop the server by pressing Ctrl+C in the terminal,
# then exit the virtual environment by typing:
deactivate
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Required: Your Gemini API key
GEMINI_API_KEY=your_api_key_here

# Optional: Override default settings
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///./app.db
```

### Bot Instructions

To customize your chatbot's behavior, create a `data/bot_instructions.txt` file. This file should contain instructions that will be sent to Gemini as a system prompt.

Example:
```
You are a helpful customer support assistant for our company.
Always be polite and professional.
Provide accurate information based on our knowledge base.
```

## 📱 Features

- **AI Chat Interface**: Powered by Google's Gemini API
- **User Management**: Authentication system with JWT tokens
- **Admin Dashboard**: User management and analytics
- **Chat History**: Persistent conversation storage
- **Customizable Instructions**: Dynamic system prompts
- **Embeddable Widget**: Can be integrated into other applications

## 🏗️ Architecture

- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: SQLite (can be changed to PostgreSQL/MySQL)
- **AI**: Google Gemini API
- **Frontend**: HTML templates with JavaScript
- **Authentication**: JWT-based with bcrypt password hashing

## 🚀 Deployment

### Docker

The application includes Docker support for easy deployment:

```bash
# Build and run
docker-compose up --build

# Production build
docker build -t kommo-chatbot .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key kommo-chatbot
```

### Environment Variables for Production

Make sure to set these environment variables in production:

- `GEMINI_API_KEY`: Your Gemini API key
- `SECRET_KEY`: A strong secret key for JWT signing
- `DATABASE_URL`: Your production database URL

## 📊 Usage

1. **Access the Application**: Navigate to http://localhost:8000
2. **Create an Account**: Use the signup page or create a user via command line
3. **Customize Instructions**: Edit `data/bot_instructions.txt` to customize bot behavior
4. **Start Chatting**: Use the chat interface to interact with your AI assistant

### Creating Users

To create a user from the command line:

```bash
python create_user.py
```

### Emergency Password Reset

If you forget a user's password, you can reset it using:

```bash
python update_user.py
```

## 🔒 Security

- JWT-based authentication
- Bcrypt password hashing
- Session management
- Input validation and sanitization

## 📝 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For support and questions, please open an issue on GitHub.