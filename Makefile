init:
	python3 -m venv venv; \
	echo 'source venv/bin/activate' >> .env; \
	echo 'export DATABASE_URL=""' >> .env; \
	source ./venv/bin/activate; \
	pip3 install -r requirements.txt; \

run:
	python main.py

test:
	py.test ./tests


update_deps:
	source ./venv/bin/activate; \
	pip3 install --upgrade -r requirements.txt; \


