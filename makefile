VENV := venv
all: venv

$(VENV)/bin/activate: requirements.dev.lock
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.dev.lock

venv: $(VENV)/bin/activate

run: venv
	./$(VENV)/bin/python3 app.py

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

test: venv
	pytest

.PHONY: all venv run clean
