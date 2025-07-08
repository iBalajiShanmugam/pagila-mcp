# 🎬 Pagila Database Q&A with Google GenAI

A natural language database query system that allows you to ask questions about the Pagila movie database using Google's Gemini AI. Built with LangChain, Streamlit, and PostgreSQL.

## ✨ Features

- 🤖 **Natural Language Queries**: Ask questions in plain English
- 📊 **Database Schema Explorer**: Browse tables and columns like pgAdmin
- 🎬 **Pagila Database**: Sample movie rental database with films, actors, customers
- 🔍 **Smart SQL Generation**: AI converts your questions to SQL automatically
- 🖥️ **Web Interface**: Clean Streamlit UI with sidebar schema explorer
- 🐳 **Docker Support**: PostgreSQL database runs in Docker

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker & Docker Compose
- Google AI API Key (free at [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone and setup**:
   ```bash
   git clone <your-repo>
   cd pagila-mcp
   ./setup.sh
   ```

2. **Get Google API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create free account and generate API key
   - Update `.env` file with your key:
     ```
     GOOGLE_API_KEY=your-api-key-here
     ```

3. **Run the application**:
   ```bash
   ./run_ui.sh
   ```

4. **Access the app**: Open http://localhost:8501

## 🎯 Usage Examples

### Sample Questions
- "How many movies are available?"
- "Show me some comedy movies"
- "List the top 5 actors with most films"
- "Which customer has rented the most films?"
- "What are the most popular movie categories?"
- "Show me all movies released after 2005"

### Database Schema
The Pagila database includes:
- **Films**: Movie catalog with titles, descriptions, ratings
- **Actors**: Actor information and film associations
- **Customers**: Customer data and rental history
- **Categories**: Movie genres and classifications
- **Rentals**: Rental transactions and payments
- **Inventory**: Store inventory and availability

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│  LangChain   │────│  Google GenAI   │
│                 │    │   Agent      │    │   (Gemini)      │
└─────────────────┘    └──────────────┘    └─────────────────┘
         │                       │
         │              ┌──────────────┐
         └──────────────│ PostgreSQL   │
                        │  (Docker)    │
                        └──────────────┘
```

## 📁 Project Structure

```
pagila-mcp/
├── app.py              # Main Streamlit application
├── main.py             # Terminal-based Q&A (optional)
├── docker-compose.yml  # PostgreSQL container setup
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── setup.sh           # Setup script
├── run_ui.sh          # Run web interface
├── run.sh             # Run terminal interface
└── pagila.sql         # Database schema and data
```

## 🔧 Configuration

### Environment Variables
```bash
# .env file
GOOGLE_API_KEY=your-google-api-key-here
DATABASE_URL=postgresql+psycopg2://balaji:balaji123@localhost:5432/pagila
```

### Database Connection
- **Host**: localhost:5432
- **Database**: pagila
- **Username**: balaji
- **Password**: balaji123

## 🚦 API Limits (Google GenAI Free Tier)

- **Model**: Gemini 2.0 Flash
- **Daily Requests**: 200 per day
- **Rate Limit**: 15 requests per minute
- **Tokens**: 1M per minute

## 🛠️ Development

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start database
docker compose up -d

# Load database (if needed)
docker exec -i pagila_db psql -U balaji -d pagila < pagila.sql

# Run application
streamlit run app.py
```

### Terminal Mode
For command-line usage:
```bash
./run.sh
```

## 🎨 UI Features

### Database Explorer (Left Sidebar)
- 📊 Database name and table count
- 🔍 Search/filter tables
- ▶️ Expandable table sections
- 📋 Column details with data types
- 🏷️ Required/Optional indicators

### Query Interface (Main Area)
- 🚀 Quick start sample questions
- 💬 Natural language input
- 📊 Formatted results display
- 💡 Usage tips and guidance

## 🔍 Troubleshooting

### Common Issues

1. **API Quota Exceeded**:
   - Wait 24 hours for quota reset
   - Check your Google AI Studio usage

2. **Database Connection Failed**:
   ```bash
   docker compose down -v
   docker compose up -d
   ```

3. **Empty Database**:
   ```bash
   docker exec -i pagila_db psql -U balaji -d pagila < pagila.sql
   ```

4. **Module Not Found**:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## 📊 Database Schema Overview

### Core Tables
- `film` - Movie catalog (1000 films)
- `actor` - Actor information (200 actors)
- `customer` - Customer data (599 customers)
- `category` - Movie genres (16 categories)
- `rental` - Rental transactions
- `payment` - Payment records
- `inventory` - Store inventory
- `staff` - Store staff
- `store` - Store locations

### Relationships
- Films ↔ Actors (many-to-many)
- Films ↔ Categories (many-to-many)
- Customers → Rentals → Payments
- Inventory → Rentals

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

- **Pagila Database**: Sample database for PostgreSQL
- **LangChain**: Framework for LLM applications
- **Google GenAI**: Gemini AI models
- **Streamlit**: Web app framework

---

**Happy Querying! 🎬✨**