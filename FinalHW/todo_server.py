import json
import http.server
import socketserver
import os

tasks = []
next_id = 1
FILE_NAME = "tasks.txt"


def save_tasks():
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def load_tasks():
    global tasks, next_id
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
                if tasks:
                    next_id = max(task['id'] for task in tasks) + 1
        except:
            tasks = []


class TodoHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/tasks":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(tasks).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        global next_id

        if self.path == "/tasks":
            try:
                length = int(self.headers['Content-Length'])
                data = json.loads(self.rfile.read(length).decode('utf-8'))

                if 'title' not in data or 'priority' not in data:
                    self.send_error(400, "Missing title or priority")
                    return

                if data['priority'] not in ['low', 'normal', 'high']:
                    self.send_error(400, "Priority must be low, normal or high")
                    return

                new_task = {
                    'id': next_id,
                    'title': data['title'],
                    'priority': data['priority'],
                    'isDone': False
                }
                tasks.append(new_task)
                next_id += 1
                save_tasks()

                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(new_task, ensure_ascii=False).encode('utf-8'))

            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
            except:
                self.send_error(500, "Internal error")

        elif "/tasks/" in self.path and "/complete" in self.path:
            try:
                parts = self.path.split('/')
                task_id = int(parts[2])

                found = False
                for task in tasks:
                    if task['id'] == task_id:
                        task['isDone'] = True
                        found = True
                        break

                if found:
                    save_tasks()
                    self.send_response(200)
                    self.end_headers()
                else:
                    self.send_error(404, "Task not found")

            except:
                self.send_error(400, "Invalid task ID")

        else:
            self.send_error(404, "Not Found")


def run_server():
    load_tasks()
    print("Сервер запущен: http://localhost:8080")
    with socketserver.TCPServer(("", 8080), TodoHandler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()