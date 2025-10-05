# Contributing to Blink OS

Thank you for your interest in contributing to Blink OS! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/Invincibleeeee/blinkOS/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Browser/OS information

### Suggesting Features

1. Check existing [Issues](https://github.com/Invincibleeeee/blinkOS/issues) for similar suggestions
2. Create a new issue with:
   - Clear use case
   - Expected behavior
   - Why this would be valuable

### Code Contributions

#### Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/blinkOS.git
cd blinkOS/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### Making Changes

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes following our code style:
   - Use functional components with hooks
   - Follow existing component structure
   - Use Tailwind CSS for styling
   - Keep components small and focused
   - Add comments for complex logic

3. Test your changes:
```bash
npm run build
npm run preview
```

4. Commit your changes:
```bash
git add .
git commit -m "feat: add amazing feature"
```

Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `test:` - Adding tests
- `chore:` - Maintenance tasks

5. Push to your fork:
```bash
git push origin feature/your-feature-name
```

6. Create a Pull Request:
   - Clear title and description
   - Reference related issues
   - Include screenshots for UI changes

### Code Style Guidelines

#### React/JavaScript
- Use ES6+ features
- Prefer const over let
- Use arrow functions
- Destructure props
- Use meaningful variable names

#### CSS/Tailwind
- Use Tailwind utilities first
- Custom CSS only when necessary
- Follow existing naming conventions
- Keep responsive design in mind

#### Components
```jsx
// Good example
import { motion } from 'framer-motion';
import { Icon } from 'lucide-react';

export default function Component({ title, description }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="bg-black text-white"
    >
      <h2 className="text-xl font-medium">{title}</h2>
      <p className="text-sm text-neutral-400">{description}</p>
    </motion.div>
  );
}
```

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged
4. Your contribution will be credited

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community

## Questions?

- Open an issue for discussion
- Check existing documentation
- Reach out to maintainers

Thank you for contributing to Blink OS! 🙏
