# Ticketing System

A comprehensive ticketing system built with FastAPI backend and React/TypeScript frontend, featuring role-based access control, SLA tracking, contract management, weighted pricing, email notifications, and PDF/CSV reporting.

## Features

### Core Functionality
- **Role-Based Access Control**: Three user roles (Admin, Agent, Client) with specific permissions
- **Ticket Management**: Complete CRUD operations for tickets with status tracking
- **SLA Tracking**: Automatic SLA assignment and breach monitoring based on priority
- **Contract Management**: Create and manage client contracts with included tickets
- **Weighted Pricing**: Automatic ticket pricing based on priority and contract terms
- **Email Notifications**: Automated email alerts for ticket events
- **Reporting**: PDF and CSV export functionality for tickets and contracts

### Technical Features
- **FastAPI Backend**: Modern, fast Python web framework with automatic API documentation
- **React Frontend**: TypeScript-based SPA with React Router for navigation
- **PostgreSQL Database**: Robust relational database for data persistence
- **Redis**: Caching and queue management support
- **Docker**: Full containerization with docker-compose for easy deployment
- **CI/CD**: GitHub Actions workflow for automated testing and building

## Architecture

### Backend Structure
```
backend/
├── app/
│   ├── core/           # Core configurations (database, security, config)
│   ├── models/         # SQLAlchemy database models
│   ├── schemas/        # Pydantic schemas for validation
│   ├── routers/        # API endpoints
│   ├── services/       # Business logic (email, PDF, CSV, ticket services)
│   └── main.py         # FastAPI application entry point
├── requirements.txt
└── Dockerfile
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/     # React components
│   │   ├── auth/       # Login/Register components
│   │   ├── common/     # Layout and ProtectedRoute
│   │   ├── tickets/    # Ticket management components
│   │   └── dashboard/  # Dashboard component
│   ├── contexts/       # React contexts (Auth)
│   ├── services/       # API service layer
│   ├── types/          # TypeScript type definitions
│   └── pages/          # Page components
├── package.json
└── Dockerfile
```

## Getting Started

### Prerequisites
- Docker and Docker Compose
- (Optional) Python 3.11+ and Node.js 18+ for local development

### Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/zyadaboalyazed/ticketing_website.git
cd ticketing_website
```

2. Create environment files:
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your settings

# Frontend
cp frontend/.env.example frontend/.env
```

3. Start all services:
```bash
docker-compose up -d
```

4. Access the application:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your settings
npm run dev
```

## API Documentation

The backend provides automatic interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key API Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info
- `GET /auth/users` - List all users (Admin only)

#### Tickets
- `GET /tickets` - List tickets (filtered by role)
- `POST /tickets` - Create new ticket
- `GET /tickets/{id}` - Get ticket details
- `PUT /tickets/{id}` - Update ticket
- `DELETE /tickets/{id}` - Delete ticket (Admin only)

#### Contracts
- `GET /contracts` - List contracts
- `POST /contracts` - Create contract (Admin only)
- `GET /contracts/{id}` - Get contract details
- `PUT /contracts/{id}` - Update contract (Admin only)
- `DELETE /contracts/{id}` - Delete contract (Admin only)

#### SLAs
- `GET /slas` - List SLAs
- `POST /slas` - Create SLA (Admin only)
- `GET /slas/{id}` - Get SLA details
- `PUT /slas/{id}` - Update SLA (Admin only)
- `DELETE /slas/{id}` - Delete SLA (Admin only)

#### Reports
- `GET /reports/tickets/pdf` - Download tickets as PDF
- `GET /reports/tickets/csv` - Download tickets as CSV
- `GET /reports/contracts/pdf` - Download contracts as PDF (Admin only)
- `GET /reports/contracts/csv` - Download contracts as CSV (Admin only)

## User Roles and Permissions

### Admin
- Full access to all features
- Manage users, tickets, contracts, and SLAs
- View all reports
- Delete tickets and contracts

### Agent
- View and manage assigned tickets
- Update ticket status and assignments
- Generate ticket reports

### Client
- Create new tickets
- View own tickets
- Update own ticket details (limited)

## Ticket Pricing

Tickets are automatically priced based on:
1. **Base Price**: $50 per ticket
2. **Priority Weight**:
   - Low: 1.0x
   - Medium: 1.5x
   - High: 2.0x
   - Critical: 3.0x
3. **Contract Terms**:
   - Tickets within contract limits: Free
   - Extra tickets: Contract's extra ticket price

Example: A high-priority ticket = $50 × 2.0 = $100

## SLA Management

SLAs are automatically assigned based on ticket priority:
- Each SLA defines response and resolution times
- System monitors ticket age against SLA deadlines
- Breached SLAs trigger admin notifications
- Dashboard shows SLA breach status

## Email Notifications

Automated emails are sent for:
- Ticket creation (to client)
- Ticket assignment (to agent and client)
- Status updates (to client)
- SLA breaches (to admins)

Configure SMTP settings in `backend/.env`:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Database Schema

### Users
- id, email, username, full_name, hashed_password
- role (admin/agent/client), is_active
- created_at, updated_at

### Tickets
- id, title, description, priority, status
- client_id, assigned_agent_id, contract_id, sla_id
- base_price, weight_multiplier, final_price
- created_at, updated_at, resolved_at, closed_at
- due_date, sla_breached

### Contracts
- id, name, description, client_id
- start_date, end_date, monthly_fee
- included_tickets, price_per_extra_ticket
- is_active, created_at, updated_at

### SLAs
- id, name, description, priority
- response_time_hours, resolution_time_hours

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

### Using Docker Compose
```bash
docker-compose up -d
```

### Manual Deployment

1. Set up PostgreSQL and Redis servers
2. Configure environment variables
3. Deploy backend:
```bash
cd backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```
4. Build and deploy frontend:
```bash
cd frontend
npm run build
# Serve dist/ folder with nginx or any static file server
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password
EMAIL_FROM=noreply@ticketing.com
REDIS_URL=redis://redis:6379/0
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- GitHub Issues: https://github.com/zyadaboalyazed/ticketing_website/issues
- Email: support@example.com

## Acknowledgments

Built with:
- FastAPI - Modern Python web framework
- React - JavaScript library for building user interfaces
- TypeScript - Typed superset of JavaScript
- PostgreSQL - Advanced open source database
- Docker - Containerization platform
