smollm2-360-slice.png:
	dd if=smollm2-360.gguf of=smollm2-360-slice.file bs=16K skip=200 count=16
	binpic -color -o smollm2-360-slice.png smollm2-360-slice.file

.PHONY: clean
clean:
	rm -f smollm2-360-slice.file
	rm -f smollm2-360-slice.png
