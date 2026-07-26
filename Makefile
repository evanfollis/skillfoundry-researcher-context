.PHONY: help check
help:
	@printf '%s\n' 'make check  Validate context/front door, compile operator scripts, and check patch hygiene'
check:
	python3 scripts/check_context.py
	python3 -m py_compile scripts/*.py
	git diff --check
