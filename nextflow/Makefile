SHELL:=/bin/bash
export NXF_VER:=18.10.1

./nextflow:
	printf ">>> Installing Nextflow in the local directory\n" && \
	curl -fsSL get.nextflow.io | bash

install: ./nextflow

run: ./nextflow
	./nextflow run demo.nf
	$(MAKE) clean

clean:
	rm -rf work .nextflow
	rm -f .nextflow.log*
