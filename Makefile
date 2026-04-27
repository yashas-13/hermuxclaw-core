# HermuXclaw-CORE Build System

.PHONY: run dev test clean help

run:
	python3 core/orchestrator.py

dev:
	python3 dashboard/app.py &
	python3 core/orchestrator.py

test:
	pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf *.optimized
	rm -rf storage/*.log

help:
	@echo "HermuXclaw-CORE Commands:"
	@echo "  make run   - Start the Orchestrator loop"
	@echo "  make dev   - Start Dashboard and Orchestrator"
	@echo "  make test  - Run the test suite"
	@echo "  make clean - Remove logs and temporary files"
