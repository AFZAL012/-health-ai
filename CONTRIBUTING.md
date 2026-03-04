# Contributing to Medical Diagnosis Enhancement System

Thank you for your interest in contributing to this project!

## Development Setup

1. Follow the setup instructions in [README.md](README.md)
2. Create a new branch for your feature: `git checkout -b feature/your-feature-name`
3. Make your changes following the coding standards below

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Write docstrings for all functions, classes, and modules
- Maximum line length: 100 characters
- Use `black` for code formatting
- Use `flake8` for linting

Example:
```python
def analyze_symptoms(symptoms: List[str], user_id: Optional[int] = None) -> AnalysisResult:
    """Analyze symptoms and return disease predictions.
    
    Args:
        symptoms: List of symptom names
        user_id: Optional user ID for personalized analysis
        
    Returns:
        AnalysisResult containing predictions and recommendations
    """
    pass
```

### TypeScript (Frontend)

- Use TypeScript for all new code
- Follow Airbnb style guide
- Use functional components with hooks
- Use proper TypeScript types (avoid `any`)
- Maximum line length: 100 characters
- Use `prettier` for code formatting
- Use `eslint` for linting

Example:
```typescript
interface SymptomData {
  symptom: string;
  severity: 'mild' | 'moderate' | 'severe';
  duration: number;
}

const SymptomInput: React.FC<{ onSubmit: (data: SymptomData) => void }> = ({ onSubmit }) => {
  // Component implementation
};
```

## Testing Requirements

### Backend Tests

- Write unit tests for all new functions
- Write property-based tests for core logic
- Maintain minimum 80% code coverage
- Use pytest fixtures for test setup
- Mock external dependencies

Run tests:
```bash
cd backend
pytest
pytest --cov=. --cov-report=html
```

### Frontend Tests

- Write unit tests for all components
- Write integration tests for user flows
- Use React Testing Library
- Test accessibility features

Run tests:
```bash
cd frontend
npm test
npm run test:coverage
```

## Commit Message Format

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(auth): add JWT token refresh endpoint

Implement automatic token refresh to improve user experience.
Tokens are refreshed 5 minutes before expiration.

Closes #123
```

## Pull Request Process

1. Update documentation for any new features
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md with your changes
5. Request review from at least one maintainer
6. Address review comments
7. Squash commits before merging

## Code Review Guidelines

When reviewing code:
- Check for security vulnerabilities
- Verify test coverage
- Ensure documentation is updated
- Check for performance issues
- Verify accessibility compliance
- Test the changes locally

## Security

- Never commit sensitive data (passwords, API keys)
- Use environment variables for configuration
- Follow OWASP security guidelines
- Report security vulnerabilities privately

## Questions?

If you have questions, please:
1. Check existing documentation
2. Search closed issues
3. Open a new issue with the "question" label

Thank you for contributing!
