all:
	python parseq.py

export:
	scp index.en.ht end.en.ht pcx:static/data-stewardship/
	rsync -vr result/ pcx:static/data-stewardship/
	ssh pcx 'cd static/data-stewardship ; ./makeit'
	ssh pcx 'cd static/data-stewardship; for f in c* ; do cd $$f ; ../makeit ..; cd .. ; done'

clean:
	rm -r result
	mkdir result
