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
	docker stop redis_test
test: venv
	sudo yum install docker -y
	sudo service docker start
	sudo docker run --name redis_test -p 6379:6379 -d redis
	./$(VENV)/bin/python3 app.py & echo $$! > server.PID;
	./$(VENV)/bin/python3 -m pytest
	kill `cat server.PID`
	docker stop redis_test

.PHONY: all venv run clean
