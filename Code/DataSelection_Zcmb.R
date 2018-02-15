# Extract the redshift information from the selected supernova Ia
setwd("~/Dropbox/project/snoopy/pipeline")
dataselectionPath <- "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/ThirdReleaseData/FormateBVRI/"
dataselectionFile <- list.files(dataselectionPath)
setwd(dataselectionPath)
SNe <- rep(0,length(dataselectionFile))
Zcmb <- rep(0,length(dataselectionFile))
for(FileI in 1:length(dataselectionFile)){
  infor <- readLines(dataselectionFile[FileI])[1]
  SNe[FileI] <- strsplit(infor,split = " ")[[1]][1]
  Zcmb[FileI] <- as.numeric(strsplit(infor,split = " ")[[1]][2])
}
redshiftdf = data.frame(SN = SNe,Zcmb = Zcmb)


data <- "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/ThirdReleaseData/kCorrected/"
dataFile <- list.files(data)
setwd(data)
SNesub <- rep(0,length(dataselectionFile))
for(FileI in 1:length(dataFile)){
  infor <- dataFile[FileI]
  SNesub[FileI] <- strsplit(infor,split = "_")[[1]][1]
}
Namedf <- data.frame(SN = SNesub)
library(plyr)
subredshiftdf <- join_all(list(Namedf,redshiftdf),by = "SN",type = "inner")


write.csv(subredshiftdf,file = "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/ThirdReleaseData/Redshift.csv",row.names = FALSE)
