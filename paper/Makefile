# Build the paper. `make tables` regenerates the included tables from the analysis; `make pdf` builds build/main.pdf.
.PHONY: pdf tex tables arxiv clean
pdf: tables
	python3 build.py
tex: tables
	python3 build.py --tex-only
tables:
	cd ../analysis && python3 paper_tables.py > /dev/null
arxiv: pdf
	rm -rf arxiv && mkdir arxiv && cp build/main.tex build/main.bbl build/header.tex arxiv/ && mkdir arxiv/figures && cp ../figures/*.pdf arxiv/figures/ \
	&& sed -i 's|\.\./\.\./figures/|figures/|g' arxiv/main.tex && cd arxiv && tar czf ../arxiv.tar.gz . && echo "arxiv.tar.gz ready"
clean:
	rm -rf build arxiv arxiv.tar.gz
