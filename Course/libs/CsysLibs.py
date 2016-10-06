import hmac, hashlib, requests

class CsysLibs:
	def __init__(self, acc, pwd):
		self.s =requests.Session()
		self.hash =""
		self.pageID =""
		self.acc =acc
		self.pwd =pwd
		self.url ="http://csys.cycu.edu.tw/sso/sso.srv"
		self.courseUrl ="http://csys.cycu.edu.tw/student/op/StudentCourseView.srv"
		self.traceCourseUrl ="http://csys.cycu.edu.tw/student/op/StudentCourseTrace.srv"
		self.headers ={"Host": "csys.cycu.edu.tw",
				"Referer": "http://csys.cycu.edu.tw/index.jsp",
				"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0",
				"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
				"Accept-Language": "zh-tw,zh;q=0.8,en-us;q=0.5,en;q=0.3",
				"Accept-Encoding": "gzip, deflate",
				"DNT": "1",
				"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
				"Content-Length": "94",
				"Connection": "keep-alive",
				"Pragma": "no-cache",
				"Cache-Control": "no-cache",
		}


	# Initial Login
	def Initialize(self):
		init ={"cmd":"login_init"}
		rs =self.s.post(self.url, data =init)
		self.hash =rs.json()['secureRandom']

		return rs.json()['result']


	# Login
	def Login(self):
		h =hmac.new(str.encode(self.pwd), digestmod =hashlib.sha256)
		h.update(str.encode(self.acc))
		h.update(str.encode(self.hash))
		login ={"cmd":"login", "userid":self.acc, "hash": h.hexdigest()}
		data ="cmd=login&userid=%s&hash=%s"%(self.acc, login['hash'])
		self.headers['Content-Length'] =len(data)
		self.s.headers.update(self.headers)

		rs =self.s.post(self.url, data =data)
		self.pageID =rs.json()['pageId']

		return rs.json()['result']


	# Check Page ID
	def CheckPageID(self):
		self.headers['Page-Id'] =self.pageID
		self.s.headers.update(self.headers)
		checkData ={"cmd": "checkPageId"}
		r =self.s.post(self.url, checkData)

		return r.json()


	# Student Course Trace
	def TraceCourseSelect(self):
		traceData ={"cmd": "selectJson", "where": "sn_status>0 AND idcode="+self.acc, "orderby": "sn_course_type,op_code"}
		r =self.s.post(self.traceCourseUrl, data =traceData)
		print(r.text)
		return r.json()


	# Insert Trace Course
	def TraceCourseInsert(self, courseID):
		traceCourse ="""cmd=insert&json={"idcode":"%s", "op_code":"%s"}"""%(self.acc, courseID)
		r =self.s.post(self.traceCourseUrl, data =traceCourse)
		#print(r.text)
		return ""
		#return r.json()


	# Trace Course Delete
	def TraceCourseDelete(self, courseID):
		traceDelete ="""cmd=delete&pk=%s,%s"""%(self.acc, courseID)
		r =self.s.post(self.traceCourseUrl, data =traceDelete)
		print(r.text)
		return r.json()


	# Student Course View
	def CourseSelect(self):
		courseData ={
			"cmd": "selectJson",
			"where": "sn_status>0 AND idcode='%s'"%self.acc,
			"orderby": "sn_course_type,op_code"
		}
		r =self.s.post(self.courseUrl, data =courseData)

		return r.json()


	# Insert Student Course
	def CourseInsert(self, courseID):
		addCourse ="""cmd=addSelection&op_code=%s"""%courseID
		r =self.s.post(self.courseUrl, data =addCourse)

		return r.json()


	# Delete Student Course
	def CourseDelete(self, courseID):
		delCourse ="""cmd=deleteSelection&op_code=%s"""%courseID
		r =self.s.post(self.courseUrl, data =delCourse)

		return r.json()

	# Logout
	def Logout(self):
		logout ={"cmd":"logout"}
		r =self.s.post(self.url, logout)

		return r.json()

cID ="MI539R"
clib =CsysLibs("10394019", "Avc129117156")
rs =clib.Initialize()
print("Initialize", rs)

if rs:
	rs =clib.Login()
	print("Login", rs)

	if rs:
		try:
			rs =clib.CheckPageID()
			print("CheckPageID", rs)

			#rs =clib.TraceCourseSelect()
			#print("TraceCourseSelect", rs)

			rs =clib.TraceCourseInsert(cID)
			print("TraceCourseInsert", rs)

			rs =clib.TraceCourseDelete(cID)
			print("TraceCourseDelete", rs)

			rs =clib.CourseSelect()
			print("CourseSelect", rs)

			rs =clib.CourseInsert(cID)
			print("CourseInsert", rs)

			rs =clib.CourseDelete(cID)
			print("CourseDelete", rs)

		finally:
			rs =clib.Logout()
			print("Logout", rs)


