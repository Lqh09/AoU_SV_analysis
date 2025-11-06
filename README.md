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
`plot_cadd_sv.py` 
- `--cadd`: CADD results (`SV_CADD.score.bed`)
- `--summary`: Tab-separated file with columns (`Variant_ID`, `Sample_Count`, `Score`, `Sensitivity`, `Sample_IDs`, `SVTYPE`) <br>
- `--known_ids`: IDs of SVs detected in previous callsets (Comparison strategy can refer to *Section: Variant annotation and comparison to external datasets* in the Supplementary file.) `

### eQTL mapping ###
- **Cohort:**  
Matched DNA-seq and RNA-seq data from 731 1KG individuals, representing 26 globally distributed populations across five continents.

- **Genotypes:**  
SVs were genotyped and imputed into 1KG samples using KAGE and GLIMPSE to obtain high-quality, population-consistent genotype calls.
SNPs genotype data are available from: [https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000G_2504_high_coverage/working/20201028_3202_phased/](https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000G_2504_high_coverage/working/20201028_3202_phased/)

- **Expression:**  
The expression file `inverse_normal_TMM.filtered.TSS.MAGE.v1.0.bed.gz` contains TMM-normalized expression values transformed to a normal distribution.

- **Covariates:**  
The corresponding covariate file is `eQTL_covariates.tab.gz`.

- **Data source:**  
Both expression and covariate files are available from the MAGE project([https://github.com/mccoy-lab/MAGE](https://github.com/mccoy-lab/MAGE))  

#### eQTL 
##### Generate SV–gene pairs within 1 Mb
```bash
bedtools window -w 1000000 -a variant.vcf.gz -b gene_annotation.bed |awk 'BEGIN{print "SV,gene"}{print $3","$NF}' > variant_gene_1Mb
```
##### Run eQTL analysis
`run_eqtl.py` 
- `--geno`: SV genotypes for each sample (e.g., `1|1`, `0|1`), with columns: `VariantID`, `Sample1`, `Sample2`, ...
- `--expr`: Gene expression matrix, with columns: `gene`, `Sample1`, `Sample2`, ...
- `--covar`: Sample covariate file, with columns: `id`, `Sample1`, `Sample2`, ...
- `--pairs` List of SV–gene pairs (e.g., variant_gene_1Mb)
- `---out-pairs`: Raw association results for each SV–gene pair
- `--out-bh`: Benjamini–Hochberg FDR–corrected results
##### Visualize eQTL results
`eQTL_summary.py` 
- `--eqtl`: Raw eQTL results (`eQTL_result.csv`)
- `--eqtl_bh`: FDR-corrected results (`eQTL_result.bh.csv`)
- `--gene-name`: Tab-delimited file mapping gene IDs to gene names.
- `--gene-list`: Medically relevant gene names.   
- `--out-png`: Figure summarizing eQTL findings
  
#### Fine-mapping 
##### Generate CAVIAR input files
`caviar_inputs.py`
- `--sv-z`: SV-eQTL summary statistics with columns: `VariantID`, `GeneID`, `Zscore`, `pscore`, `pos`.
- `--sv-gt`: SV genotype file with columns: `VariantID`, `Sample1`, `Sample2`, ...
- `--snp-z`: SNP-eQTL summary statistics with columns: `VariantID`, `GeneID`, `Zscore`, `pscore`, `pos`.
- `--snp-gt`: SNP genotype file with columns: `VariantID`, `Sample1`, `Sample2`, ...
- `variant.zscore`: Variant IDs and corresponding zscores.  
- `variant.ld`: LD r² matrix.  
- `variant.list`: Ordered list of variant IDs used in the analysis.
            
##### Casual variant identification 
`run_caviar.sh`: Processing all variant–gene pairs using the generated input files.

##### Case study
`Genotypes_expression.py`: Relationship between genotypes and gene expression for a specific pair
- `--gene`: Gene ID in the SV–gene pair.
- `--SV`: SV ID in the SV–gene pair.

`Manhattan_plot.py`: Generates Manhattan plots for *BID*. The genotype and eQTL significance files follow the same format as `caviar_inputs.py`, but include data for the selected gene only to improve computational efficiency.


### SVs in LD with GWAS-significant SNVs  ###


### Phenome-wide SV analysis ###
