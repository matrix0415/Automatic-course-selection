import requests


url ="https://itouch.cycu.edu.tw/active_system/login/login2.jsp"
data ={"UserNm":"10394019", "UserPasswd":"Avc129117156", "Submit":"登入"}
r =requests.post(url, data =data)
print(r.url)

s =requests.Session()
r2 =s.post(url, data =data)

# Basic Info
r3 =s.get("http://itouch.cycu.edu.tw/active_system/quary/s_basic.jsp")
#print(r3.text)

# Scores Info
data2 ={"T3":"1021"}
r4 =s.post("http://itouch.cycu.edu.tw/active_project/cycu2000h_03/cycu_11/Grade/Grade_new.jsp", data =data2)
print(r4.url)

logout =s.get("http://itouch.cycu.edu.tw/active_system/login/logout.jsp")
print(logout.url)

data ={"UserNm":"10394019", "UserPasswd":"Avc129117156", "Submit":"登入"}
login =requests.post(url, data =data)



