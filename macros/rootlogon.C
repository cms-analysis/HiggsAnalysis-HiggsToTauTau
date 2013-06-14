{
  if(gSystem->Getenv("CMSSW_VERSION")) {    
    //TString rfitpath("/afs/cern.ch/cms/slc5_amd64_gcc462/lcg/roofit/5.34.02/include");
    TString rfitpath("/afs/cern.ch/cms/slc5_amd64_gcc472/lcg/roofit/5.34.03/include");
    TString path = gSystem->GetIncludePath();
    path += "-I. -I$ROOTSYS/src -I";
    path += rfitpath;
    gSystem->SetIncludePath(path.Data());
    //gSystem->Load("/afs/cern.ch/cms/slc5_amd64_gcc462/lcg/roofit/5.34.02-cms/lib/libRooFitCore.so");
    //gSystem->Load("/afs/cern.ch/cms/slc5_amd64_gcc462/lcg/roofit/5.34.02-cms/lib/libRooFit.so");
    gSystem->Load("/afs/cern.ch/cms/slc5_amd64_gcc472/lcg/roofit/5.34.03-cms/lib/libRooFitCore.so");
    gSystem->Load("/afs/cern.ch/cms/slc5_amd64_gcc472/lcg/roofit/5.34.03-cms/lib/libRooFit.so");
    TString str = gSystem->GetMakeSharedLib();
    if (str.Contains("-m32")==0 && str.Contains("-m64")==0) {
      str.ReplaceAll("g++", "g++ -m32");
      gSystem->SetMakeSharedLib(str);
    }
  }
}
