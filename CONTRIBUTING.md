# Contributing to Ticketing System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ticketing_website.git
   cd ticketing_website
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/zyadaboalyazed/ticketing_website.git
   ```
4. **Set up development environment**:
   ```bash
   ./quick-start.sh
   ```

## Development Workflow

1. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bugfix-name
   ```

2. **Make your changes** following the coding standards

3. **Test your changes**:
   ```bash
   # Backend tests
   cd backend
   pytest
   
   # Frontend tests
   cd frontend
   npm test
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   # or
   git commit -m "fix: resolve bug"
   ```

5. **Keep your branch updated**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

## Coding Standards

### Python (Backend)

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions small and focused
- Use meaningful variable names

Example:
```python
from typing import List
from sqlalchemy.orm import Session
from ..models import Ticket

def get_user_tickets(user_id: int, db: Session) -> List[Ticket]:
    """
    Retrieve all tickets for a specific user.
    
    Args:
        user_id: The ID of the user
        db: Database session
        
    Returns:
        List of Ticket objects
    """
    return db.query(Ticket).filter(Ticket.client_id == user_id).all()
```

### TypeScript/React (Frontend)

- Use functional components with hooks
- Use TypeScript for type safety
- Follow consistent naming conventions
- Keep components small and reusable
- Use meaningful prop names

Example:
```typescript
interface TicketCardProps {
  ticket: Ticket;
  onUpdate: (ticket: Ticket) => void;
}

const TicketCard: React.FC<TicketCardProps> = ({ ticket, onUpdate }) => {
  return (
    <div className="ticket-card">
      <h3>{ticket.title}</h3>
      <p>{ticket.description}</p>
    </div>
  );
};
```

### Commit Messages

Use conventional commits format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add email notifications for ticket updates
fix: resolve authentication token expiration issue
docs: update deployment guide with SSL instructions
```

## Testing

### Backend Testing

Location: `backend/tests/`

```bash
cd backend
pytest                           # Run all tests
pytest tests/test_api.py        # Run specific test file
pytest -v                       # Verbose output
pytest --cov=app               # With coverage
```

Write tests for:
- API endpoints
- Business logic
- Database operations
- Authentication/authorization

Example:
```python
def test_create_ticket():
    """Test ticket creation"""
    response = client.post(
        "/tickets",
        json={
            "title": "Test Ticket",
            "description": "Test Description",
            "priority": "medium"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Ticket"
```

### Frontend Testing

Location: `frontend/src/`

```bash
cd frontend
npm test              # Run tests
npm test -- --coverage # With coverage
```

Write tests for:
- Component rendering
- User interactions
- API calls
- State management

## Submitting Changes

### Pull Request Guidelines

1. **Title**: Use a clear, descriptive title
2. **Description**: Explain what changes you made and why
3. **Reference Issues**: Link related issues (e.g., "Fixes #123")
4. **Screenshots**: Include screenshots for UI changes
5. **Tests**: Ensure all tests pass
6. **Documentation**: Update docs if needed

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally
```

## Review Process

1. **Automated Checks**: CI/CD pipeline runs automatically
2. **Code Review**: Maintainers will review your code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, your PR will be merged

## Development Tips

### Backend Development

- Use virtual environment to isolate dependencies
- Run backend with `--reload` flag for auto-restart
- Use API documentation at `/docs` for testing
- Check logs for debugging

### Frontend Development

- Use React DevTools for debugging
- Hot reload is enabled in dev mode
- Check browser console for errors
- Use TypeScript strict mode

### Database Changes

If you need to modify database schema:

1. Update models in `backend/app/models/`
2. Create migration:
   ```bash
   alembic revision --autogenerate -m "description"
   ```
3. Review and edit the migration file
4. Apply migration:
   ```bash
   alembic upgrade head
   ```

## Getting Help

- **Documentation**: Check README.md and DEPLOYMENT.md
- **Issues**: Search existing issues or create a new one
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers at support@example.com

## Areas to Contribute

Looking for where to start? Here are some areas:

- **Bug Fixes**: Check open issues labeled "bug"
- **Features**: Look for issues labeled "enhancement"
- **Documentation**: Improve or add documentation
- **Tests**: Increase test coverage
- **UI/UX**: Improve user interface and experience
- **Performance**: Optimize code and queries
- **Accessibility**: Make the app more accessible

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project website (if applicable)

Thank you for contributing! 🎉
