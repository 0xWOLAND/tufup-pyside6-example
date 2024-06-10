# Build

To build on MacOS, run:

```shell
python3 repo_init.py
make build
python3 repo_add_bundle.py
```

## Start server

```shell
python -m http.server -d temp_myapp/repository
```

Then, update the version in `myapp/settings.py`. Then, run

```shell
make build
python3 repo_add_bundle.py
```
