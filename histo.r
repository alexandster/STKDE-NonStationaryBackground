inTable <- read.table("E:/Dissertation3/test/envelope_diff_v2.txt", header = FALSE, sep = ",", dec = ".")
histo <- hist(inTable$V4)


#buckets <- c(0,1,2,3,4,5,25)
#bp <- barplot(histo$count, log="y", col="white")