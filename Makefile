install: 
	pip install -r requirements.txt
build-frontend:
	cd myapp/frontend && pnpm i && pnpm run build && cd ../..
build-resource:
	rm -f resource_rc.py
	python3 build_rc.py
	pyside6-rcc resource.qrc -o resource_rc.py
debug:
	make build-frontend
	make build-resource
	python3 main.py
build:
	make build-frontend
	make build-resource
	pyinstaller myapp.spec --clean -y --distpath temp_myapp/dist/app --workpath temp_myapp/build
	rm -r temp_myapp/dist/app/myapp
clean:
	rm -r temp_myapp .tufup-repo-config
lint:
	black .
test:
	pytest
test_ci:
	pytest myapp/utils/