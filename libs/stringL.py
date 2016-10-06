import re

def fetchUrl(fakeUrl):
	
	urlList =[]
	regex = re.compile("<<([^>]+)~([^>]+)/([^>]+)>>")
	parametersList =regex.findall(fakeUrl)
	
	if len(parametersList) is not 0:
		for para in parametersList:
			para =[int(i) for i in para]
			
			for num in range(para[0], para[1], para[2]):
				url =re.sub('<<\S+>>', str(num), fakeUrl)
				urlList.append([num ,url])
	
	else:
		urlList.append(fakeUrl)
	
	return urlList
	
	
def removeNewlineL(string):
	return string.strip()


def removeSpaceL(string):
	return re.sub(' +','', string)

	
def removeRedundentSpaceL(string):
	return re.sub(' +',' ', string)
	

def removePunctuationL(string):
	from string import punctuation

	exclude = set(punctuation)
	
	return ''.join(ch for ch in string if ch not in exclude)
	
	
def removeWithoutEnglishL(string):
	from re import sub
		
	return " ".join(sub(r"[^A-Za-z\s]+"," ", string.lower()).split()).strip()
	
	
class nltkL(object):		
	def __init__(self, nltkPath =""):
		import nltk
		
		nltk.data.path.append(nltkPath)
		
		
	def englishTokenizer(self, string):
		from nltk import word_tokenize as tokenize
		
		return tokenize(string)
		

	def englishWordnet(self, string):
		from nltk.corpus import wordnet
		
		return wordnet.synsets(string)
	
	
	def posTagger(self, stringList):
		from nltk.tag import pos_tag as pos
		
		return pos(stringList)
		
		
	def posTaggerFilter(self, corpus, acceptTagList):
		if type(corpus) ==str:
			corpus =self.englishTokenizer(corpus)
			
		rs =" ".join([word[0] for word in self.posTagger(corpus) if word[1] in acceptTagList or word[1].lower in acceptTagList])
		
		return rs
		
	
	def englishWordList(self):
		from nltk.corpus import words
		
		return words.words()
		
	
	def englishWordChecker(self, string):
		rs =True
		wordlist =self.englishWordList()
		
		if string not in wordlist:
			if not self.englishWordnet(string):
				rs =False
		
		return rs
		
	
	def englishCorpusChecker(self, corpus, accuracy, corpusMinimumWords =3, preCheck =5, preAccuracy =0.99):
		rs =[False]
		nonEng =0
		corpus =removeRedundentSpaceL(removePunctuationL(corpus))
		words =self.englishTokenizer(corpus)
		
		if len(words) !=0 and len(words)>=corpusMinimumWords:
			for word in words[:preCheck]:
				if not self.englishWordChecker(word):	# False
					nonEng +=1						# False +1
					
			if (len(words)-nonEng)/len(words)>preAccuracy:
				rs[0] =True
				rs.append(words)
				
			elif (len(words)-nonEng)/len(words)>=0.5:
				for word in words:
					if not self.englishWordChecker(word):	# False
						nonEng +=1						# False +1	
				
				if (len(words)-nonEng)/len(words)>accuracy:
					rs[0] =True
					rs.append(words)
		
		return rs
		
	
	
	def lemma(self, string):
		from nltk.stem.wordnet import WordNetLemmatizer as lemma
		
		l =lemma()
		
		return l.lemmatize(string)
		
	
	def englishCorpusLemma(self, corpus, accuracy, corpusMinimumWords =3, preCheck =3, preAccuracy =0.99):
		rs =[False, ]		
		checker =self.englishCorpusChecker(corpus, accuracy, corpusMinimumWords, preCheck, preAccuracy)
		
		if checker[0]:
			corpus =' '.join([self.lemma(i) for i in checker[1]])
			corpus =removeWithoutEnglishL(corpus)
			rs.append(corpus)			
			rs[0] =True
			
		return rs
		
		
	def token2ngram(self, tokens, n):
		return [tokens[i:i+n] for i in range(0,len(tokens)-n-1)]	
		
		
	def string2ngram(self, string, n):
		tokens =self.englishTokenizer(string)
		return self.token2ngram(tokens, n)
		
		