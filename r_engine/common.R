suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
})

# Helper function to add a diffexpress column
formatting_func <- function(df, padj_cutoff = 0.05, lfc_cutoff = 1.5) {
    df$diffexpress <- "NO"
    df$diffexpress[df$padj < padj_cutoff & df$log2FoldChange > lfc_cutoff] <- "UP"
    df$diffexpress[df$padj < padj_cutoff & df$log2FoldChange < -lfc_cutoff] <- "DOWN"
    return(df)
}

# Helper function for volcano plots
volcano_plot <- function(res_df, out_png) {
  png(out_png, width=1200, height=900, res=150)
  on.exit(dev.off(), add = TRUE)
  # Basic volcano without EnhancedVolcano to keep deps lighter in first run
  res_df <- res_df %>% mutate(sig = ifelse(padj < 0.05 & abs(log2FoldChange) >= 1, "sig", "ns"))
  gg <- ggplot(res_df, 
                aes(x = log2FoldChange, 
                          y = -log10(padj), 
                          col = diffexpress)) +
    geom_vline(xintercept = c(-1.5, 1.5), col = "gray", linetype = "dashed") +
    geom_hline(yintercept = -log10(0.05), col = "gray", linetype = "dashed") +
    geom_point(size = 2) +
    scale_color_manual(values = c("blue","grey","red"),
                    labels = c("Downregulated", "Not significant", "Upregulated")) +
    coord_cartesian(ylim = c(0, 40), xlim = c(-10, 10)) +
    labs(color = "Legend", 
      x = expression("log"[2]*"FC"), 
      y = expression("-log"[10]*"p-value"))
    theme_minimal()
  print(gg)
}
