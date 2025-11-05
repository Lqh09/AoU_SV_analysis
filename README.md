# AoU_SV_analysis
## Project Overview
This project investigates the functional and clinical relevance of structural variants (SVs) identified from long-read sequencing data in the All of Us (AoU) Research Program. To evaluate their broader impact, these variants were imputed into both the 1000 Genomes Project and short-read AoU cohorts. Integration with RNA-seq and electronic health record (EHR) data enabled downstream analyses, such as eQTL mapping, linkage disequilibrium (LD) with GWAS variants, and phenome-wide association studies (PheWAS), to comprehensively characterize the regulatory and disease-related effects of variants.

### Score the effect of SVs ###
#### CADD-SV annotation
```bash
conda activate run.caddsv
snakemake  --use-conda --configfile config.yml -j 4 -n
grep -v CADD-SV_PHRED-score CADD_output.bed |awk '{OFS="\t"}{print "chr"$1, $2, $3, $5"|"$4"|"$6}' > SV_CADD.score.bed
```
#### Distribution of CADD-SV score for shared SVs in the AoU strict cohort
Usage
```bash
python plot_cadd_sv.py   --cadd SV_CADD.score.bed   --summary SV_summary.txt   --known_ids LR_match_IDs   --output Cadd_SV_sample_summary.png
```
Input<br>
`--summary`: Tab-separated file with columns (`Variant_ID`, `Sample_Count`, `Score`, `Sensitivity`, `Sample_IDs`, `SVTYPE`) <br>
`--known_ids`: IDs of SVs detected in previous callsets (Comparison strategy can refer to *Section: Variant annotation and comparison to external datasets* in the Supplementary file.) `


### SV-eQTL ###
**Cohort:**  
  Matched DNA-seq and RNA-seq data from 731 individuals, representing 26 globally distributed populations across five continents.

**Genotyping:**  
  SVs were genotyped and imputed into 1KG samples to ensure consistent representation across populations.

- **Expression data:**  
  The expression file `inverse_normal_TMM.filtered.TSS.MAGE.v1.0.bed.gz` contains TMM-normalized expression values transformed to a normal distribution.

- **Covariates:**  
  The corresponding covariate file is `eQTL_covariates.tab.gz`.

- **Data source:**  
  Both expression and covariate files are available from the MAGE project([https://github.com/mccoy-lab/MAGE](https://github.com/mccoy-lab/MAGE))  

Sample 

