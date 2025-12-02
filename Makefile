test:
    pytest tests/

unit_test:
    pytest -m "not performance" tests/

perf_test:
    pytest -m performance tests/perf_test.py

coverage:
    coverage run -m pytest tests/
    coverage report -m

lint:
    ruff check triangulator tests

doc:
    pdoc3 triangulator --html --output-dir docs
