import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import pymysql

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        conn = pymysql.connect(
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"],
            host=os.environ["MYSQL_HOST"],
            database=os.environ["MYSQL_DB"],
        )
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM user")
                rows = cur.fetchall()

            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()

            for row in rows:
                # row[1] matches your original intent; ensure bytes for wfile
                self.wfile.write((str(row[1]) + "\n").encode("utf-8"))
        finally:
            conn.close()


if __name__ == "__main__":
    HTTPServer(("", 8000), Handler).serve_forever()
