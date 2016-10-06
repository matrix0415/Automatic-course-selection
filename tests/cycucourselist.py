import requests

r =requests.get("http://itouch.cycu.edu.tw/active_system/CourseQuerySystem/GetCourses.jsp?yearTerm=1031")

courseList =r.text

lst =[i.split("|") for i in courseList.split("@")]

del lst[0]

lst2 =set(sorted([i[8] for i in lst]))
lst3 =set(sorted([i[23] for i in lst]))
difflist =[i for i in lst3 if i not in lst2]
difflist2 =[i for i in lst2 if i not in lst3]

print(str(len(lst2)), lst2)
print()
print(difflist2)
print()
print(str(len(lst3)), lst3)
print()
print(difflist)
print()



r =requests.get("http://itouch.cycu.edu.tw/active_system/CourseQuerySystem/GetAuthority.jsp?yearTerm=1031")

lstA =r.text.split("|")

difflist3 =[i for i in lst3 if i not in lstA]
difflist4 =[i for i in lstA if i not in lst3]

print(difflist3, "\n", difflist4)

lstkey =[]

for i in range(22, 36):
	print(str(i), "-----------------------------")
	print(set(sorted([k[i] for k in lst])))
	 
	
