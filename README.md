# Health Chatbot
An AI-powered healthcare support system utilizing a three-model architecture for accurate, safe, and research-backed health assistance.

## Features
- Intelligent health assistance with research-backed responses
- Multi-platform support (Web & WhatsApp)
- Real-time health tips and recommendations
- Secure human handoff capabilities
- Vector database for efficient knowledge management

## Technical Architecture

**AI Models**
- Gemini Flash (Query Analysis)
  - Temperature: 0.3
  - Response time: 1-2s
  - Fast query decomposition
- Perplexity Sonar (Research)
  - Context window: 128k tokens
  - Real-time data retrieval
- Gemini Pro (Response)
  - Temperature: 0.7
  - Enhanced prompting

## Tech Stack
- Frontend: Streamlit
- Backend: Flask with RESTful API
- Database: ChromaDB
- Integration: Twilio for WhatsApp
- AI: Google Gemini and Perplexity Sonar

## Installation

```bash
# Clone the repository
git clone https://github.com/vinayakvthayil/Health_Chatbot
```

## Usage

```bash
# Run the web interface
python app.py

# Run WhatsApp integration
python whatsapp_bot.py
```

## System Components

**Frontend Features**
- Interactive chat interface
- Health tips display
- Assessment interface
- Feedback system

**Backend Features**
- Vector database integration
- Knowledge base management
- Chat history tracking
- Multi-layer safety system

## Safety Features
- Content filtering
- Intent detection
- Source credibility checks
- Medical disclaimer injection
- Warning generation
