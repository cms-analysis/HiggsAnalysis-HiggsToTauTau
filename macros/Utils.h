#include "string"
#include "iostream"

#include "TFile.h"


template <class Type>
Type* get(TFile* file, const char* hist) 
{
  Type* plot = (Type*) file->Get(hist);
  if(!plot){ std::cout << "ERROR:: hist: " << hist << " does not exist in file " << file->GetName() << "." << std::endl; exit(1); }
  return plot;
}

std::string cleanupWhitespaces(std::string str)
{
  if(str.find(" ")!=std::string::npos){
    return cleanupWhitespaces(str.substr(0, str.find(" ")).append(str.substr(str.find(" ")+1, std::string::npos)));
  }
  return str;
}

std::string string2Vector(std::string str, std::vector<std::string>& vec)
{
  if(str.find(",")!=std::string::npos){
    vec.push_back(str.substr(0, str.find(",")));
    return string2Vector(str.substr(str.find(",")+1, std::string::npos), vec);
  }
  vec.push_back(str);
  return str;
}
