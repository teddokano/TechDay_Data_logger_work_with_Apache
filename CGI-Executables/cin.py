#!/opt/homebrew/bin/python3
import os
from http import cookies

cookie = cookies.SimpleCookie()
cookie.load(os.environ["HTTP_COOKIE"])

print("Content-Type: text/html")
print("")

print("<!DOCTYPE html>")
print("<html lang=\"ja\">")
print("<head>")
print("<meta http-equiv=\"CONTENT-TYPE\" content=\"text/html; charset=utf-8\" />")
print("</head>")
print("<body>")
print("<p>*** cookie_get.py *** start ***</p>")
print("message: " + cookie["message"].value + "<br />")
print("aa: " + cookie["aa"].value + "<br />")
print("bb: " + cookie["bb"].value + "<br />")
print("cc: " + cookie["cc"].value + "<br />")
#
# print(session.cookies.get_dict())
print("<p>*** cookie_get.py *** end ***</p>")
print("<p>Apr/27/2021</p>")
print("</body>")
print("</html>")
# ------------------------------------------------------------------
