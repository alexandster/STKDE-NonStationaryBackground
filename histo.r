#histo.r
#this script creates a histogram of the differences between upper and lower envelope.

inTable <- read.table("outputs/envelope_diff_v2.txt", header = FALSE, sep = ",", dec = ".")
histo <- hist(inTable$V4)
