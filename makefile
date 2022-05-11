VENV := venv
all: venv

$(VENV)/bin/activate: requirements.dev.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.dev.txt

venv: $(VENV)/bin/activate

run: venv
	./$(VENV)/bin/python3 app.py

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	kill `cat server.PID`

test: venv
	./$(VENV)/bin/python3 app.py & echo $$! > server.PID;
	./$(VENV)/bin/python3 -m pytest
	kill `cat server.PID`

.PHONY: all venv run clean
