# AoU_SV_analysis
## Project Overview
This project investigates the functional and clinical relevance of structural variants (SVs) identified from long-read sequencing data in the All of Us Research Program. To evaluate their broader impact, these variants were imputed into both the 1000 Genomes Project and short-read AoU cohorts. Integration with RNA-seq and electronic health record (EHR) data enabled downstream analyses, such as eQTL mapping, linkage disequilibrium (LD) with GWAS variants, and phenome-wide association studies (PheWAS), to comprehensively characterize the regulatory and disease-related effects of variants.

### Score the effect of SVs ###
CADD-SV annotation
```bash
conda activate run.caddsv
snakemake  --use-conda --configfile config.yml -j 4 -n
grep -v CADD-SV_PHRED-score CADD_output.bed |awk '{OFS="\t"}{print "chr"$1, $2, $3, $5"|"$4"|"$6}' > SV_CADD.score.bed
```bash

### SV-eQTL ###



