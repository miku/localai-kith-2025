SHELL = /bin/bash

.PHONY: fmt
fmt:
	prettier -w index.html

quotes.txt: raw.txt
	cat raw.txt | grep -v '"' | shuf | awk '{print "\"" $$0 "\","}' > quotes.txt

