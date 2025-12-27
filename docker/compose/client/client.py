import os
import mysql.connector
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        mydb= mysql.connector.connect(user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"],
            host=os.environ["MYSQL_HOST"],
            database=os.environ["MYSQL_DB"])
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM user")
        myresult = mycursor.fetchall()
        for user in myresult:
            self.wfile.write(user[1] + "\n")
        mydb.close()

httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
