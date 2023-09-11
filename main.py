import os
import re
import argparse
import fnmatch
import shutil
from jinja2 import Environment, FileSystemLoader
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

def should_skip(dir_name):
    return any(fnmatch.fnmatch(dir_name, pattern) for pattern in skip_dirs)

def find_todos(repo_path, skip_dirs=[]):
    todos = []
    # Read .gitignore and populate skip_dirs
    gitignore_path = os.path.join(repo_path, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore_patterns = f.readlines()
        skip_dirs += [pattern.strip() for pattern in gitignore_patterns if pattern.strip()]
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if not should_skip(d)]
        for filename in files:
            if filename.endswith(".git"):
                continue  # skip .git directories
            
            with open(os.path.join(root, filename), 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
                
                for line_number, line in enumerate(lines, start=1):
                    if re.search(r"# TODO|// TODO|/\* TODO", line):
                        todos.append({
                            'filename': filename,
                            'line_number': line_number,
                            'content': line.strip(),
                        })
    return todos

def generate_html(todos):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')
    output = template.render(todos=todos, repo_path=repo_path[repo_path.rfind('/')+1:])
    if not os.path.exists('build'):
        os.makedirs('build')
        shutil.copytree('assets', 'build/assets')
    with open(os.path.join('build', 'todos.html'), 'w') as f:
        f.write(output)

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/todos.html'
        return SimpleHTTPRequestHandler.do_GET(self)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find TODOs in a repo and serve them in an HTML page.")
    parser.add_argument("repo_path", help="Path to the repository")
    parser.add_argument("--port", default=8080, help="Port to serve on")
    parser.add_argument("--skip-dirs", nargs="*", default=[], help="Directories to skip")
    args = parser.parse_args()
    repo_path = args.repo_path
    skip_dirs = args.skip_dirs
    PORT = args.port

    todos = find_todos(repo_path, skip_dirs if skip_dirs else [])
    generate_html(todos)
    
    with TCPServer(("", int(PORT)), MyHandler) as httpd:
        print(f"Serving at port {PORT}")
        print(f"http://127.0.0.1:{PORT}/build/todos.html")
        httpd.serve_forever()
