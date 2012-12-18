inline void
PlotLimits::prepareHIG_12_043(std::vector<double>& values, const char* type, double mass, bool initial)
{
  if(mssm_){
    std::cout << "HIG-12-043 contained only SM limits" << std::endl;
    exit(1);
  }
  else{
    if(std::string(type)==std::string("observed")){
      if(mass==110) {values.push_back(1.89); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back(1.85); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back(1.64); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back(1.63); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back(1.57); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back(1.56); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back(1.72); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back( 2.1); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("+2sigma")){
      if(mass==110) {values.push_back(1.98); }
      if(mass==115) {values.push_back(1.92); }
      if(mass==120) {values.push_back(1.84); }
      if(mass==125) {values.push_back(1.84); }
      if(mass==130) {values.push_back(1.95); }
      if(mass==135) {values.push_back(2.23); }
      if(mass==140) {values.push_back(2.54); }
      if(mass==145) {values.push_back(3.07); }
    }
    else if(std::string(type)==std::string("+1sigma")){
      if(mass==110) {values.push_back(1.49); }
      if(mass==115) {values.push_back(1.45); }
      if(mass==120) {values.push_back(1.38); }
      if(mass==125) {values.push_back(1.38); }
      if(mass==130) {values.push_back(1.47); }
      if(mass==135) {values.push_back(1.68); }
      if(mass==140) {values.push_back(1.92); }
      if(mass==145) {values.push_back(2.31); }
    }
    else if(std::string(type)==std::string("expected")){
      if(mass==110) {values.push_back( 1.07); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back( 1.04); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back(0.996); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back(0.996); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back( 1.06); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back( 1.21); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 1.38); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back( 1.66); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("-1sigma")){
      if(mass==110) {values.push_back(0.775); }
      if(mass==115) {values.push_back(0.753); }
      if(mass==120) {values.push_back(0.719); }
      if(mass==125) {values.push_back(0.719); }
      if(mass==130) {values.push_back(0.764); }
      if(mass==135) {values.push_back(0.871); }
      if(mass==140) {values.push_back(0.995); }
      if(mass==145) {values.push_back(  1.2); }
    }
    else if(std::string(type)==std::string("-2sigma")){
      if(mass==110) {values.push_back(0.583); }
      if(mass==115) {values.push_back(0.566); }
      if(mass==120) {values.push_back( 0.54); }
      if(mass==125) {values.push_back( 0.54); }
      if(mass==130) {values.push_back(0.574); }
      if(mass==135) {values.push_back(0.655); }
      if(mass==140) {values.push_back(0.748); }
      if(mass==145) {values.push_back(0.903); }
    }
    else{
      std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		<< "       for the moment I'll stop here" << std::endl;
      exit(1);
    }
  }
  return;
}

