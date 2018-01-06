# After running TmaxCalculate.py, we have calculated the maximum data for all four bands and store them in Tmax.csv
# We use DataSelection.R to use our selection criterior 

## Read all the data 

setwd("~/Dropbox/project/snoopy/pipeline/Code/")
BVRIpath <- "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/FormatedBVRI/"
BVRIfile <- list.files(BVRIpath)
outputPath <- "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/DataSelection/"
options(digits=10)
Tmaxinfor <- read.csv("/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/DataSelection/Tmax.csv")
FileName <- Tmaxinfor[,1]
Tmaxlist <- list()
Tmaxlist[[1]] <- Tmaxinfor[,2] # B
Tmaxlist[[2]] <- Tmaxinfor[,3] # V
Tmaxlist[[3]] <- Tmaxinfor[,4] # r
Tmaxlist[[4]] <- Tmaxinfor[,5] # i

## Loop for files
for(i in 1:length(BVRIfile)){
  print(i)
  # The path for the specific object
  # Read the raw data (without removing "#")
  inputfile_BVRI <- readLines(paste0(BVRIpath,BVRIfile[i]))
  # Locate the "filter" position
  LocFilter <- grep("filter",inputfile_BVRI)
  bol <- rep(0,4)
  # Loop for four filters
  for(f in 1:4){
    if(f < 4){
      Nrow <- LocFilter[f+1]-LocFilter[f]-1
    }else{
      Nrow <- length(inputfile_BVRI) - LocFilter[f]
    }
    Fildf <- data.frame(matrix(0,ncol = 3, nrow = Nrow))
    for(j in 1:Nrow){
      Fildf[j,] <- as.numeric(unlist(strsplit(inputfile_BVRI[LocFilter[f]+j],split=" ")))
    }
    MJD_f <- Fildf[,1]
    bol[f] <- DeterSelected(MJD_f, Tmaxlist[[f]][i])
  }
  boolS <- sum(bol)
  if(boolS == 4){
    write.table(inputfile_BVRI,file = paste0(outputPath,BVRIfile[i]),row.names = FALSE,col.names = FALSE,quote = FALSE)
  }else{
    next
  }
}


DeterSelected <- function(MJDSeq_, Tmax_){
  LocP <- which(MJDSeq_<= Tmax_)
  locO <- which(MJDSeq_>=Tmax_)
  if(length(LocP) == 0||length(locO) ==0 ){
    return(0)
  }else{
  PreMJD <- Tmax_-MJDSeq_[max(LocP)]
  OverMJD <- MJDSeq_[min(locO)]-Tmax_
  if(PreMJD<=5&OverMJD<=5){
    return(1)
  }else{
    return(0)
  }
  }
}


