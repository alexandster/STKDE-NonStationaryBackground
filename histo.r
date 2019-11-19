#histo.r
#this script creates a histogram of the differences between upper and lower envelope.

inTable <- read.table("outputs/envelope/envelope_diff.txt", header = FALSE, sep = ",", dec = ".")
histo <- hist(inTable$V4)
