suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
})

# Plot helpers (extend as needed)
volcano_plot <- function(res_df, out_png) {
  png(out_png, width=1200, height=900, res=150)
  on.exit(dev.off(), add = TRUE)
  # Basic volcano without EnhancedVolcano to keep deps lighter in first run
  res_df <- res_df %>% mutate(sig = ifelse(padj < 0.05 & abs(log2FoldChange) >= 1, "sig", "ns"))
  gg <- ggplot(res_df, aes(x=log2FoldChange, y=-log10(pvalue))) +
    geom_point(aes(shape=sig), alpha=0.6) +
    geom_vline(xintercept=c(-1,1), linetype="dashed") +
    geom_hline(yintercept=-log10(0.05), linetype="dashed") +
    theme_minimal()
  print(gg)
}
