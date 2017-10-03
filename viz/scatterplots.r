library(ggplot2)

data <- read.csv(file="../data/hanziDB.csv",sep=",",head=TRUE, nrows=1000)

data$stroke_count <- as.numeric(as.character(data$stroke_count))
plot <- ggplot(data) + geom_point(aes(x=frequency_rank, y=stroke_count), color='blue', alpha=0.3) + geom_point(aes(x = frequency_rank, y = hsk_level), color = 'red', alpha=0.2)

print(plot)
