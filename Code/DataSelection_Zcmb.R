# Extract the redshift information from the selected supernova Ia

dataselectionPath <- "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/FormatedBVRI/"
dataselectionFile <- list.files(dataselectionPath)
setwd(dataselectionPath)
SNe <- rep(0,length(dataselectionFile))
Zcmb <- rep(0,length(dataselectionFile))
for(FileI in 1:length(dataselectionFile)){
  infor <- readLines(dataselectionFile[FileI])[1]
  SNe[FileI] <- strsplit(infor,split = " ")[[1]][1]
  Zcmb[FileI] <- as.numeric(strsplit(infor,split = " ")[[1]][2])
}
redshiftdf = data.frame(SNe = SNe,Zcmb = Zcmb)
write.csv(redshiftdf,file = "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/Redshift.csv",row.names = FALSE)
