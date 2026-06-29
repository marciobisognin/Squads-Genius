# Coding Standards: AI-Business-Builder-Squad

## 1. Overview
These standards ensure that all AI-generated scripts, automation workflows, and code snippets within the `ai-business-builder-squad` are maintainable, secure, and efficient for both human developers and AI agents.

## 2. General Principles
- **Readability:** Code must be easy for both humans and AI agents to parse. Use clear, descriptive naming conventions.
- **Modularity:** Break logic into small, reusable functions or components. Avoid monolithic scripts.
- **DRY (Don't Repeat Yourself):** Abstract common logic into utility modules within the squad's config or source tree.
- **KISS (Keep It Simple, Stupid):** Prefer simple, readable logic over complex, clever optimizations unless performance is critical.

## 3. Language-Specific Standards
### Python
- **Style:** Follow PEP 8 guidelines.
- **Typing:** Use type hints for all function signatures to assist AI reasoning.
- **Documentation:** Use Google-style docstrings for all functions and classes.
- **Validation:** Use `pydantic` for data validation and settings management.

### JavaScript / TypeScript
- **Syntax:** Use ES6+ syntax (arrow functions, destructuring, template literals).
- **Formatting:** Use Prettier-compatible formatting.
- **Safety:** Prefer TypeScript for complex automation to ensure type safety.

## 4. Automation & Scripting
- **Error Handling:** Always implement try-except/try-catch blocks. Provide meaningful error messages and fallback states.
- **Logging:** Use standard logging libraries instead of `print()` or `console.log()` for production-ready automation.
- **Environment Variables:** Never hardcode API keys, credentials, or secrets. Use `.env` files or the AIOS secret management system.
- **Idempotency:** Ensure automation scripts can be run multiple times without causing unintended side effects.

## 5. AI & Prompt Engineering Standards
- **Prompt Delimiters:** When scripts generate prompts, use clear delimiters (e.g., `###`, `---`, or XML tags) to separate instructions from data.
- **Token Management:** Scripts must include logic to check or truncate input lengths to stay within LLM context windows.
- **Structured Output:** Prefer JSON or Markdown as the output format for AI-generated content to facilitate downstream parsing.

## 6. Version Control & Documentation
- **Commits:** Use Conventional Commits (e.g., `feat:`, `fix:`, `docs:`, `chore:`).
- **READMEs:** Every major automation script or component must have a corresponding Markdown file explaining its purpose, inputs, and outputs.