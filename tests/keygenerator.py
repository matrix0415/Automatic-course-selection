from multiprocessing import Process as proc

def loop(char, string, hi, wf):
	lst =[]
	for i in char:
		if hi>0:
			loop(char, string+i, hi-1, wf)
		else:
			wf.write(string+"'''")

def main()
	char =[]
	jobs =[]
	wf =open("pwd.text", "a")
	char.append(list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqristuvwxyz0123456789"))
	char.append(char[0]+list("!@^*()-+<>.,/[]}{:;| "))

	for c in char:
			for i in range (6, 16):
				p =proc(target =loop, args=(c, "", i, wf))
				p.start()
				jobs.append(p)

	for job in jobs:
		job.join()

	wf.close()

if __name__ == "__main__":
	main()