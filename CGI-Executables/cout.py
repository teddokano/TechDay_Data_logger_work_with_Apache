#!/opt/homebrew/bin/python3

from http import cookies

C = cookies.SimpleCookie()
C["message"] = "This is a Test by Python."
C["aa"] = "Mt. Fuji by Python"
C["bb"] = "Mt. Tanigawa by Python"
C["cc"] = "Mt. Aso by Python"

print(C.output())


print("Content-Type: text/html")
print("")
print("<!DOCTYPE html>")
print("<html lang=\"ja\">")
print("<body>")
print("<p>*** cookie_put.py ***</p>")
print("<p>Apr/27/2021</p>")
print("</body>")
print("</html>")
# ------------------------------------------------------------------
