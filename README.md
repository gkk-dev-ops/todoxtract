# TODO Finder and Server

This Python application finds `TODO` comments in a given repository and serves them as an HTML page.

## Requirements

- Python 3.x
- Jinja2

You can install the required packages from `requirements.txt` using pip:

```bash
pip install -r requirements.txt
```

## Usage

You can run the application using the following command:

```bash
python main.py [REPO_PATH] [--port PORT] [--skip-dirs DIR1 DIR2 ...]
```

### Arguments

- `REPO_PATH`: Mandatory. The path to the repository where you want to find TODOs.
- `--port`: Optional. The port number on which the server will run. Default is 8080.
- `--skip-dirs`: Optional. Space-separated list of directories that you want to skip during the search.

By default, the directories specified in the `.gitignore` file of the repository are skipped.

## Output

The found TODOs will be rendered as an HTML page and served. The server details will be printed to the console.

For example, if the server is running on port 8080, you can view the page at:

```
http://127.0.0.1:8080/build/todos.html
```

## Project Structure

- `main.py`: The main Python script that contains the logic for finding TODOs and serving the HTML page.
- `requirements.txt`: The requirements file that lists the dependencies needed for the application.
- `template.html`: The Jinja2 template file used for generating the HTML page.
- `build/`: This directory will be created at runtime and will contain the generated `todos.html` file.
- `assets/`: Optional. If this directory exists, it will be copied to `build/assets/` during the build.

## Author

gkk
