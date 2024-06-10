import os
from pathlib import Path

build_folder = "myapp/frontend/dist"
extensions = [".js", ".css", ".html", ".json", ".ico"]


with open("resource.qrc", "w") as f:
    f.write('<RCC>\n<qresource prefix="/">')
    for root, _, files in os.walk(build_folder):
        for file in files:
            extension = Path(file).suffix
            if extension in extensions:
                file_path = os.path.join(root, file)
                file_path = file_path.replace("\\", "/")
                f.write(f"\n<file>{file_path}</file>")
    f.write("</qresource>\n</RCC>")
