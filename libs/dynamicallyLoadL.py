
def dLoadModule(moduleName, modulePath, parameter):
	mod =__import__(modulePath)
	s ="mod.%s(%s)"%(moduleName, parameter)
	rs =eval(s)
	return rs