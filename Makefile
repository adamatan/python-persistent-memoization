clean:
	rm -rf venv __pycache__

venv:
	python3 -m venv venv

test-watch:
	source venv/bin/activate && pip install pytest pytest-watch && ptw

test:
	source venv/bin/activate && pip install pytest pytest-watch && pytest -s --verbose

