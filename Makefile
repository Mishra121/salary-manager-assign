.PHONY: backend-start frontend-start test help kill-servers

# Colors for output
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help:
	@echo "$(CYAN)📋 Available Commands:$(NC)"
	@echo ""
	@echo "  $(GREEN)make backend-start$(NC)    - Seed database and start backend server (port 8000)"
	@echo "  $(GREEN)make frontend-start$(NC)   - Start frontend dev server (port 5173)"
	@echo "  $(GREEN)make test$(NC)             - Run all backend tests with pytest"
	@echo "  $(GREEN)make kill-servers$(NC)     - Kill all running backend and frontend servers"
	@echo "  $(GREEN)make help$(NC)             - Show this help message"
	@echo ""

backend-start:
	@echo "$(CYAN)🌱 Seeding database...$(NC)"
	cd backend && uv run python -m app.seed.seed_employees
	@echo ""
	@echo "$(CYAN)🚀 Starting backend server on http://localhost:8000$(NC)"
	cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend-start:
	@echo "$(CYAN)⚛️  Starting frontend dev server on http://localhost:5173$(NC)"
	cd frontend && npm run dev

test:
	@echo "$(CYAN)🧪 Running backend tests...$(NC)"
	cd backend && uv run pytest -v

kill-servers:
	@echo "$(YELLOW)🛑 Killing running servers...$(NC)"
	@lsof -ti:8000 | xargs kill -9 2>/dev/null || echo "No backend server running on port 8000"
	@lsof -ti:5173 | xargs kill -9 2>/dev/null || echo "No frontend server running on port 5173"
	@echo "$(GREEN)✅ Servers stopped!$(NC)"

.DEFAULT_GOAL := help
