# Ticketing System

A comprehensive ticketing system built with Python FastAPI backend and React/TypeScript frontend, featuring role-based access control, SLA tracking, contract management, weighted pricing, email notifications, and PDF/CSV reporting.

## Features

### Core Features
- **Role-Based Access Control**: Three user roles (Admin, Agent, Client) with different permissions
- **Ticket Management**: Create, update, track, and manage support tickets
- **SLA Tracking**: Automatic SLA monitoring and breach notifications
- **Contract Management**: Manage client contracts with custom pricing and SLA settings
- **Weighted Pricing**: Calculate costs based on hours worked and contract terms
- **Email Notifications**: Automatic notifications for ticket events
- **PDF/CSV Reporting**: Generate detailed reports for tickets and analytics

### User Roles

#### Admin
- Full system access
- Manage users, contracts, and all tickets
- Access to reporting and analytics
- Configure system settings

#### Agent
- Manage assigned tickets
- View and update ticket status
- Access to all open tickets
- Create and manage contracts

#### Client
- Create new tickets
- View own tickets
- Add comments to tickets
- Track ticket progress

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Primary database
- **Redis**: Caching and session management
- **JWT**: Authentication and authorization
- **Alembic**: Database migrations
- **ReportLab**: PDF generation
- **Pandas**: CSV/Excel report generation

### Frontend
- **React 18**: UI framework
- **TypeScript**: Type-safe JavaScript
- **React Router**: Navigation
- **Axios**: HTTP client
- **CSS3**: Styling

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD pipeline

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/zyadaboalyazed/ticketing_website.git
cd ticketing_website
```

2. Start the services:
```bash
docker-compose up -d
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```bash
echo "REACT_APP_API_URL=http://localhost:8000" > .env
```

4. Start development server:
```bash
npm start
```

## API Documentation

Once the backend is running, access the interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Main Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get access token

#### Users
- `GET /users/me` - Get current user info
- `GET /users/` - List all users (Admin only)
- `PUT /users/{id}` - Update user (Admin only)

#### Tickets
- `GET /tickets/` - List tickets (role-based filtering)
- `POST /tickets/` - Create new ticket
- `GET /tickets/{id}` - Get ticket details
- `PUT /tickets/{id}` - Update ticket
- `POST /tickets/{id}/comments` - Add comment
- `GET /tickets/{id}/comments` - Get ticket comments

#### Contracts
- `GET /contracts/` - List contracts
- `POST /contracts/` - Create contract (Agent/Admin)
- `GET /contracts/{id}` - Get contract details
- `PUT /contracts/{id}` - Update contract (Agent/Admin)

#### Reports
- `GET /reports/tickets/pdf` - Generate PDF report
- `GET /reports/tickets/csv` - Generate CSV report

## Configuration

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=noreply@ticketing.com

# Redis
REDIS_URL=redis://redis:6379/0
```

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
```

## Database Schema

### Users
- id, email, username, password, role, is_active
- Roles: admin, agent, client

### Tickets
- id, title, description, priority, status
- creator_id, assignee_id, contract_id
- SLA tracking fields
- Pricing fields (hours, rate, cost)

### Contracts
- id, name, description, client_id
- Pricing (base_rate, hourly_rate, included_hours, overage_rate)
- SLA settings (response_time, resolution_time)

### Ticket Comments
- id, ticket_id, user_id, content
- is_internal flag for agent/admin-only comments

## Features Walkthrough

### SLA Tracking
- SLA due dates are automatically calculated based on contract settings
- System monitors SLA breaches in real-time
- Email notifications sent when SLA is breached
- Visual indicators on tickets for SLA status

### Weighted Pricing
- Base rate from contract
- Hourly rate for work performed
- Included hours in contract (no extra charge)
- Overage rate for hours beyond included
- Automatic cost calculation

### Email Notifications
- Ticket created notification to creator
- Ticket assigned notification to assignee
- Status change notifications
- SLA breach alerts to admins
- HTML email templates

### Reporting
- Filter tickets by status, priority, date range
- Generate PDF reports with summary and details
- Export to CSV for data analysis
- Include cost analysis and SLA metrics

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

### Using Docker

1. Build images:
```bash
docker-compose build
```

2. Deploy:
```bash
docker-compose up -d
```

3. Check status:
```bash
docker-compose ps
```

### Production Considerations
- Use strong SECRET_KEY
- Configure proper CORS origins
- Set up SSL/TLS certificates
- Configure email service (SMTP)
- Set up database backups
- Configure monitoring and logging
- Use environment-specific configurations

## CI/CD

GitHub Actions workflow includes:
- Backend tests with PostgreSQL
- Frontend build verification
- Docker image building
- Security scanning
- Automated deployment (configure as needed)

## Security

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control
- SQL injection protection (SQLAlchemy)
- CORS configuration
- Input validation with Pydantic
- Security headers

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
- Documentation: See `/docs` directory

## Roadmap

Future enhancements:
- Real-time notifications with WebSockets
- Advanced analytics dashboard
- Mobile application
- Knowledge base integration
- Multi-language support
- Advanced search and filtering
- Ticket templates
- Custom fields
- Integration with third-party services