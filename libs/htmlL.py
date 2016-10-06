import urllib.request

def soupSelectorL(html, selector):
	from bs4 import BeautifulSoup as bs
	from libs.errorlogL import writeLogL
	
	rs =[False, ]
	
	try:
		bSoup =bs(html, from_encoding ="UTF-8")
		rs.append(bSoup.select(selector))
		rs[0] =True
		
	except Exception as e:
		rs.append(writeLogL("libs.htmlL.soupSelectorL", e))
	
	return rs
	
	
class CrawlHtmlL(urllib.request.BaseHandler):
	
	def deflate(self, data):
		import urllib.error, zlib
		
		try:
			return zlib.decompress(data, -zlib.MAX_WBITS)
		except zlib.error:
			return zlib.decompress(data)
	
	""" A handler to add gzip capabilities to urllib.request """
	def http_request(self, req):
		''' add headers to requests '''
		req.add_header("Accept-Encoding", "gzip, deflate")
		return req
     
	def http_response(self, req, resp):
		import io, gzip
		import urllib.response
		
		old_resp=resp
        # gzip
		if resp.headers.get("content-encoding") == "gzip":
			gz = gzip.GzipFile(
				fileobj = io.BytesIO( resp.read() ),
				mode="r"
			)
			resp = urllib.response.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
			resp.msg = old_resp.msg
            # deflate
		if resp.headers.get("content-encoding") == "deflate":
			gz = io.BytesIO(self.deflate(resp.read()))
			resp = urllib.response.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)  # class to add info() and geturl
			resp.msg = old_resp.msg
		return resp
		