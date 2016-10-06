import requests

r =requests.get("http://itouch.cycu.edu.tw/active_system/CourseQuerySystem/GetAuthority.jsp?yearTerm=1031")

lst =r.text.split("|")

print(len(lst))
print(sorted(lst))