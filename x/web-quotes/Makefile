SHELL = /bin/bash

quotes.txt: raw.txt
	cat raw.txt | grep -v '"' | shuf | awk '{print "\"" $$0 "\","}' > quotes.txt
