TARGETS = ibm-llm-list.txt wikipedia.llmlist.html

.PBONY: all
all: $(TARGETS)

ibm-llm-list.txt:
	links -dump https://www.ibm.com/think/topics/large-language-models-list > ibm-llm-list.txt

wikipedia.llmlist.html:
	links -dump https://en.wikipedia.org/wiki/List_of_large_language_models > wikipedia.llmlist.html
