# Railway PostgreSQL Database Project

A comprehensive Python application demonstrating PostgreSQL database connectivity and operations using Railway as the database hosting platform.

## 🚀 Features

- **Secure Database Connection**: Environment-based configuration with Railway PostgreSQL
- **Comprehensive Database Operations**: CRUD operations with error handling
- **Sample Data & Analytics**: Rich sample dataset with reporting capabilities
- **Relational Database Design**: Multiple tables with foreign key relationships
- **Advanced Queries**: Complex analytical queries and reporting

## 📋 Database Schema

### Tables

1. **users** - Main user information
   - id (SERIAL PRIMARY KEY)
   - username (VARCHAR, UNIQUE)
   - email (VARCHAR, UNIQUE)
   - full_name (VARCHAR)
   - age (INTEGER)
   - city (VARCHAR)
   - country (VARCHAR)
   - is_active (BOOLEAN)
   - salary (DECIMAL)
   - join_date (DATE)
   - department_id (INTEGER, FK)
   - created_at/updated_at (TIMESTAMP)

2. **departments** - Department information
   - id (SERIAL PRIMARY KEY)
   - name (VARCHAR, UNIQUE)
   - budget (DECIMAL)
   - location (VARCHAR)
   - created_at (TIMESTAMP)

3. **user_activities** - User activity tracking
   - id (SERIAL PRIMARY KEY)
   - user_id (INTEGER, FK)
   - activity_type (VARCHAR)
   - description (TEXT)
   - activity_date (DATE)
   - created_at (TIMESTAMP)

## 🛠️ Setup

### Prerequisites

- Python 3.12+
- uv (Python package manager)
- Railway PostgreSQL database

### Installation

1. Clone and navigate to the project:
   ```bash
   cd rail_db
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Configure environment variables:
   - Copy your Railway DATABASE_URL to `.env`
   - Format: `DATABASE_URL=postgresql://username:password@host:port/database`

### Running the Application

#### Basic Connection Test
```bash
uv run python main.py
```

#### Advanced Demo with Relationships
```bash
uv run python advanced_demo.py
```

## 📊 Sample Queries & Reports

The application includes several analytical queries:

- **User Demographics**: Age ranges, geographic distribution
- **Department Analytics**: Employee counts, salary ranges, budgets
- **Activity Tracking**: User engagement, activity patterns
- **Performance Metrics**: Top active users, department efficiency

## 🔧 Key Components

### `database.py`
- `DatabaseConnection`: Core connection handling
- `DatabaseManager`: Context manager for automatic cleanup
- Error handling and connection management

### `main.py`
- Basic connection testing
- Sample data insertion
- Basic analytical queries

### `advanced_demo.py`  
- `UserOperations`: Advanced database operations
- Relationship management
- Comprehensive reporting system

## 🔒 Security Features

- Environment variable configuration
- SQL injection prevention with parameterized queries
- Credential protection via `.gitignore`
- Connection pooling ready architecture

## 📈 Sample Data

The application includes:
- 10 sample users from different countries
- 5 departments with budgets and locations
- Random user activities for engagement tracking
- Realistic salary and demographic data

## 🚀 Next Steps

1. **Expand Schema**: Add more tables (projects, tasks, etc.)
2. **API Layer**: Build REST API endpoints
3. **Frontend**: Create web interface
4. **Analytics**: Add more complex reporting
5. **Performance**: Implement connection pooling
6. **Testing**: Add unit and integration tests

## 📝 Dependencies

- `psycopg2-binary`: PostgreSQL adapter
- `python-dotenv`: Environment variable management

## 🤝 Contributing

Feel free to extend this project with additional features, optimizations, or examples!