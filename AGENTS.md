# AI-Assisted Development Workflow

This document describes how AI tools were used to accelerate development while maintaining code quality and TDD discipline.

## 🎯 Core Principles

1. **AI as accelerator, not replacement:** AI helps with boilerplate, scaffolding, and pattern application—but critical decisions (architecture, design, validation) remain human-driven.
2. **TDD discipline maintained:** Every feature begins with a failing test, regardless of AI involvement.
3. **Code review before merge:** All AI-generated code is reviewed for correctness, style, and maintainability.
4. **Traceability:** Development approach is documented in git commits and `docs/ai-workflow.md`.

## 🚀 Development Rhythm

- **Write test:** Define behavior first (human or AI scaffolds, human reviews)
- **Implement:** AI generates code to pass the test, human reviews for correctness
- **Refactor:** Clean up naming, remove duplication (collaborative)
- **Commit:** Small, atomic commits that tell a clear story
- **Repeat:** For each feature or component

## 🛠️ Where AI Excels

- CRUD scaffolding (endpoints, validators, error handling)
- Test fixture factories and builders
- React component structure and boilerplate
- SQL optimization suggestions and indexing strategy
- Documentation generation (docstrings, README sections)
- Naming suggestions and code cleanup

## ✅ Quality Checkpoints

All code must pass before integration:
- ✓ Functional tests (pytest, Vitest)
- ✓ Static analysis (ruff, mypy, eslint, tsc)
- ✓ Type checking (full coverage)
- ✓ Manual code review
- ✓ Performance benchmarks (if applicable)

---

See `docs/ai-workflow.md` for specific prompts, iterations, and development decisions.
