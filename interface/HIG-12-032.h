inline void
PlotLimits::prepareHIG_12_032(std::vector<double>& values, const char* type, double mass, bool initial)
{
  if(mssm_){
    std::cout << "HIG-12-032 contained only SM limits" << std::endl;
    exit(1);
  }
  else{
    if(std::string(type)==std::string("observed")){
      if(mass==110) {values.push_back(0.939); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back( 1.01); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back(    1); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back( 1.01); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back( 1.09); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back( 1.53); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 1.78); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back( 2.32); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("+2sigma")){
      if(mass==110) {values.push_back(2.33); }
      if(mass==115) {values.push_back( 2.3); }
      if(mass==120) {values.push_back(2.23); }
      if(mass==125) {values.push_back(2.24); }
      if(mass==130) {values.push_back(2.36); }
      if(mass==135) {values.push_back(2.66); }
      if(mass==140) {values.push_back(3.24); }
      if(mass==145) {values.push_back(3.76); }
    }
    else if(std::string(type)==std::string("+1sigma")){
      if(mass==110) {values.push_back(1.75); }
      if(mass==115) {values.push_back(1.73); }
      if(mass==120) {values.push_back(1.68); }
      if(mass==125) {values.push_back(1.69); }
      if(mass==130) {values.push_back(1.77); }
      if(mass==135) {values.push_back(   2); }
      if(mass==140) {values.push_back(2.44); }
      if(mass==145) {values.push_back(2.83); }
    }
    else if(std::string(type)==std::string("expected")){
      if(mass==110) {values.push_back(1.26); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back(1.25); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back(1.21); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back(1.21); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back(1.28); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back(1.44); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back(1.76); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back(2.04); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("-1sigma")){
      if(mass==110) {values.push_back(0.911); }
      if(mass==115) {values.push_back(0.899); }
      if(mass==120) {values.push_back(0.871); }
      if(mass==125) {values.push_back(0.877); }
      if(mass==130) {values.push_back(0.922); }
      if(mass==135) {values.push_back( 1.04); }
      if(mass==140) {values.push_back( 1.27); }
      if(mass==145) {values.push_back( 1.47); }
    }
    else if(std::string(type)==std::string("-2sigma")){
      if(mass==110) {values.push_back(0.685); }
      if(mass==115) {values.push_back(0.676); }
      if(mass==120) {values.push_back(0.655); }
      if(mass==125) {values.push_back(0.659); }
      if(mass==130) {values.push_back(0.693); }
      if(mass==135) {values.push_back(0.782); }
      if(mass==140) {values.push_back(0.954); }
      if(mass==145) {values.push_back( 1.11); }
    }
    else{
      std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		<< "       for the moment I'll stop here" << std::endl;
      exit(1);
    }
  }
  return;
}

