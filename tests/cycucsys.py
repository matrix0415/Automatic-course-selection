import hmac, hashlib, requests

acc ="10394019"
pwd ="Avc129117156"
url ="http://csys.cycu.edu.tw/sso/sso.srv"

headers ={"Host": "csys.cycu.edu.tw",
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

loginRs =False
while not loginRs:
	# Initial Login
	init ={"cmd":"login_init"}
	s =requests.Session()
	r =s.post(url, data =init)


	# Login
	hash =r.json()['secureRandom']
	h =hmac.new(str.encode(pwd), digestmod =hashlib.sha256)
	h.update(str.encode(acc))
	h.update(str.encode(hash))
	login ={"cmd":"login", "userid":acc, "hash": h.hexdigest()}
	data ="cmd=login&userid=%s&hash=%s"%(acc, login['hash'])
	headers['Content-Length'] =len(data)
	s.headers.update(headers)

	r =s.post(url, data =data)
	print(r.json())

	if r.json()['result']:
		try:
			loginRs =True
			# Check Page ID
			headers['Page-Id'] =r.json()['pageId']
			s.headers.update(headers)
			checkData ={"cmd": "checkPageId"}

			r =s.post(url, checkData)
			print(r.text)

			'''
			# ------- Course Trace -------
			# Student Course Trace
			traceCourseUrl ="http://csys.cycu.edu.tw/student/op/StudentCourseTrace.srv"
			traceData ={"cmd": "selectJson", "where": "sn_status>0 AND idcode=10394019", "orderby": "sn_course_type,op_code"}

			r =s.post(traceCourseUrl, data =traceData)
			print(r.text)

			# Insert Trace Course
			traceCourse ="""cmd=insert&json={"idcode":"10394019", "op_code":"MI481R"}"""

			r =s.post(traceCourseUrl, data =traceCourse)
			print(r.text)


			# Trace Course Delete
			traceDelete ="""cmd=delete&pk=10394019,MI481R"""

			r =s.post(traceCourseUrl, data =traceDelete)
			print(r.text)


			# ------- Course View -------
			# Student Course View
			courseUrl ="http://csys.cycu.edu.tw/student/op/StudentCourseView.srv"
			courseData ={"cmd": "selectJson", "where": "sn_status>0 AND idcode='10394019'", "orderby": "sn_course_type,op_code"}
			r =s.post(courseUrl, data =courseData)
			#print(r.text)

			'''
			courseUrl ="http://csys.cycu.edu.tw/student/op/StudentCourseView.srv"
			# Insert Student Course
			addCourse ="""cmd=addSelection&op_code=MI539R"""

			r =s.post(courseUrl, data =addCourse)
			print(r.text)

			'''
			# Delete Student Course
			delCourse ="""cmd=deleteSelection&op_code=MI539R"""

			r =s.post(courseUrl, data =delCourse)
			print(r.text)
			'''

		except Exception as e:
			print(e)

		finally:
			# Logout
			logout ={"cmd":"logout"}

			r =s.post(url, logout)
			print(r.text)

