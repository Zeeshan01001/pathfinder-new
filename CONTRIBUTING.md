# Contributing to PathFinder

Thank you for your interest in contributing to PathFinder! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/pathfinder.git
cd pathfinder
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
python -m unittest discover tests
```

## Making Changes

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and test them thoroughly
3. Write or update tests as needed
4. Update documentation if required
5. Commit your changes:
```bash
git commit -m "Add: brief description of your changes"
```

## Pull Request Process

1. Push to your fork and submit a pull request
2. Wait for review and address any feedback
3. Once approved, your PR will be merged

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and concise

## Adding Features

When adding new features:
- Update the README.md if needed
- Add appropriate tests
- Update documentation
- Add example usage if applicable

## Questions?

Feel free to open an issue for any questions or concerns. 