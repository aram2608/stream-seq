#!/usr/bin/env Rscript

# Load in the required libraries
suppressPackageStartupMessages({
    library(jsonlite)
    library(readr)
    library(dplyr)
    library(DESeq2)
    library(tibble)
})

# Load in our volcano plot function
source("r_engine/common.R")

# Load in our config file
args <- commandArgs(trailingOnly=TRUE)
if (length(args) < 1) {
    stop("Usage: Rscript run_deseq2.R <config.json>")
}
cfg <- jsonlite::fromJSON(args[1])

# Creates output again just in case
dir.create(cfg$outdir, showWarnings = FALSE, recursive = TRUE)

# Loads in the count matrix
cat("Reading count matrix: ", cfg$counts, "...\n")
raw_data <- read.delim(cfg$counts, sep = "\t", header = TRUE)

# Cleans up columns and sets rownames
counts <- raw_data[, -1]
rownames(counts) <- raw_data[, 1]
head(counts)

# Loads in the column data
cat("\nReading column data: ", cfg$samples, "...\n")
coldata <- read.delim(cfg$samples, sep = ",", header = TRUE)
rownames(coldata) <- coldata[,1]
head(coldata)

# Saving design from config file as formula
design <- as.formula(cfg$design)

# Running DESeq analysis
cat("Running DESeq2...")
dds <- DESeqDataSetFromMatrix(countData = counts,
                            colData = coldata,
                            design = design)
dds <- DESeq(dds)

# Saving result as a dataframe
res <- results(dds)
head(res)