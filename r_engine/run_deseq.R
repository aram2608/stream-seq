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

dir.create(cfg$outdir, showWarnings = FALSE, recursive = TRUE)