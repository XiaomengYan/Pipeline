setwd("~/Dropbox/project/snoopy/pipeline")
rawpath <- "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/CSP_Photometry_DR2/"

rawfile <- list.files(rawpath)
options(digits=10)

for(i in 1:length(rawfile)){
  # The path for the specific object
  inputname <- paste0(rawpath,rawfile[i])
  # Read the raw data (without removing "#")
  inputfile_raw <- readLines(inputname)
  # Remove "#"
  inputfile_all <- gsub("#","",inputfile_raw)
  # Calculate the length of observations 
  Nlines = length(inputfile_all)-5
  dataframName  <- unlist(strsplit(gsub(" ","",inputfile_all[5]),split="\t"))
  lightcurveMat <- data.frame(matrix(0,nrow = Nlines,ncol = length(dataframName)))
  for(j in 1:Nlines){
  lightcurveMat[j,] <- as.numeric(unlist(strsplit(inputfile_all[j+5],split="\t")))
  }
  names(lightcurveMat) <- dataframName
  # Then extract the light curve information 
  Objname <- unlist(strsplit(inputfile_all[1], split = " "))[8]
  RRADEC <- unlist(strsplit(gsub("\t","",inputfile_all[3]), split = " "))
  Redshift <- as.numeric(RRADEC[4])
  RA <- TranFunRA(RRADEC[8])
  DEC <- TranFunDEC(RRADEC[11])
  ObsTime <- as.numeric(paste(unlist(strsplit(Objname,split = ""))[3:6],collapse = ""))
  FilterType <- DeterFilter(ObsTime)
  FilterName <- c('B','V','r','i')
  lightcurveMat <- ExtractBVRIFun(lightcurveMat,FilterName)
  WriteFun(Objname,FilterType,Redshift,RA,DEC,lightcurveMat)
}


















####################### Main function ########################################
# WriteTxt function: combine the data frame and the information about the Object 
# which generate the format that can be recognized by SNOOPY
WriteFun <- function(Objname_,FilterType_,Redshift_,RA_,DEC_,lightcurveMat_){
  InfVec <- c(Objname_,Redshift_,RA_,DEC_)
  outpath <- "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/FormatedBVRI/"
  Objnametxt <- paste0(outpath,Objname_,"_CSP_main.txt")
  write.table(t(InfVec),Objnametxt,sep = " ",col.names = FALSE,row.names = FALSE,quote = FALSE)
  Nfilter <- (ncol(lightcurveMat_)-1)/2
  for(j in 1:Nfilter){
  newdf <- data.frame(MJD = lightcurveMat_[,1],filter = lightcurveMat_[,2*j],Sig = lightcurveMat_[,2*j+1])
  bol <- unique(c(which(newdf[,2]==99.9),which(newdf[,3]==99.9)))
  if(length(bol)==0){
    reNadf <- newdf
  }else{
  reNadf <- newdf[-unique(c(which(newdf[,2]==99.9),which(newdf[,3]==99.9))),]}
  fileName <- names(lightcurveMat_)[j*2]
  write.table(t(c("filter",paste0(fileName,FilterType_))),Objnametxt,sep = " ",append = TRUE,col.names = FALSE,row.names = FALSE,quote = FALSE)
  write.table(reNadf,Objnametxt,sep = " ",append = TRUE,col.names = FALSE,row.names = FALSE,quote = FALSE)
  }
}

### Extract specific filter information from the lightcurveMat dataframe.
ExtractBVRIFun <- function(lightcurveMat_,FilterName_){
  lightcurveMat_name <- names(lightcurveMat_)
  resdf <- data.frame(MJD = lightcurveMat_[,1])
  for(i in FilterName){
    locFilter <- which(lightcurveMat_name == i)
    if(length(locFilter)>0){
      resdf[,i] <- lightcurveMat_[,locFilter]
      resdf[,ncol(resdf)+1] <- lightcurveMat_[,locFilter+1]
      names(resdf)[ncol(resdf)] <- paste0("sigma",i)
    }else{
      next
    }
  }
  return(resdf)
}

# Determine the V-band filter according to Timestamp
DeterFilter <- function(ObsTime_){
  Change <- 2006
  if(ObsTime_ < Change){
    return("CSP3014")
  }else{
    return("CSP9844")
  }
}

# Transfer function which transfer ::: to .
TranFunRA <- function(InputChara){
  tmp <- as.numeric(unlist(strsplit(InputChara,split = "\\:")))
   res <- (tmp[1]+tmp[2]/60+tmp[3]/3600)*15
  return(res)
}

TranFunDEC <-function(InputChara){
  tmp <- as.numeric(unlist(strsplit(InputChara,split = "\\:")))
  res <- abs(tmp[1])+tmp[2]/60+tmp[3]/3600
  if(tmp[1]>=0){
  return(res)
  }else{return((-1)*res)}
}


