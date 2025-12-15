.PHONY: test unit_test perf_test coverage lint doc clean

test:
	cd triangulator_project && PYTHONPATH=. python3 -m pytest tests/

unit_test:
	cd triangulator_project && PYTHONPATH=. python3 -m pytest -m "not performance" tests/

perf_test:
	cd triangulator_project && PYTHONPATH=. python3 -m pytest -m performance tests/

coverage:
	cd triangulator_project && PYTHONPATH=. coverage run --omit=tests/test_perf.py -m pytest -m "not performance" tests/
	cd triangulator_project && PYTHONPATH=. coverage report -m
	cd triangulator_project && PYTHONPATH=. coverage html

lint:
	cd triangulator_project && python3 -m ruff check triangulator tests

doc:
	cd triangulator_project && PYTHONPATH=. pdoc3 triangulator --html --output-dir docs

clean:
	rm -rf .pytest_cache .coverage htmlcov docs
	cd triangulator_project && rm -rf .pytest_cache .coverage htmlcov docs
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
