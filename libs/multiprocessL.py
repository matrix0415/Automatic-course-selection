def prepareForMultiprocess(listLen, nJobs):
	from math import ceil
	
	perJobRow =ceil(listLen/nJobs)	# num per process		
	rowUntil =perJobRow*nJobs+1
	
	return {"perJobRow": perJobRow, "rowUntil": rowUntil}