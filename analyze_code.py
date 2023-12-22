import ast
import html
import os


def traverse_directories(root_dir):
    issues = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.lua'):
                file_path = os.path.join(root, file)
                issues.extend(analyze_code(file_path))
    return issues

def analyze_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    parsed_code = ast.parse(code)
    issues = []
    for node in ast.walk(parsed_code):
        if isinstance(node, ast.Call):
            if node.func.id == 'print':
                issues.append({
                    'file_name': file_path,
                    'issue_description': 'Print statement found',
                    'issue': 'print',
                    'fix': 'Remove print statement or replace with logging'
                })
    return issues

def generate_html(issues):
    table = html.table([
        html.tr([
            html.th('File Name'),
            html.th('Issue Description'),
            html.th('Issue'),
            html.th('Fix')
        ])
    ] + [
        html.tr([
            html.td(issue['file_name']),
            html.td(issue['issue_description']),
            html.td(issue['issue']),
            html.td(issue['fix'])
        ]) for issue in issues
    ])
    with open('found.html', 'w') as file:
        file.write(str(table))

if __name__ == '__main__':
    root_dir = '.'
    issues = traverse_directories(root_dir)
    generate_html(issues)
