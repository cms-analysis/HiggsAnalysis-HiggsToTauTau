inline void
PlotLimits::prepareHIG_13_004(std::vector<double>& values, const char* type, double mass, bool initial)
{
  if(mssm_){
    std::cout << "HIG-13-004 contained only SM limits" << std::endl;
    exit(1);
  }
  else{
    if(std::string(type)==std::string("observed")){
      if(mass==110) {values.push_back(1.79); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back(1.88); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back(1.81); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back( 1.8); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back(1.84); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back( 1.9); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 1.9); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back( 2.3); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("+2sigma")){
      if(mass==110) {values.push_back(1.54); }
      if(mass==115) {values.push_back(1.48); }
      if(mass==120) {values.push_back(1.39); }
      if(mass==125) {values.push_back(1.42); }
      if(mass==130) {values.push_back(1.51); }
      if(mass==135) {values.push_back(1.74); }
      if(mass==140) {values.push_back(2.03); }
      if(mass==145) {values.push_back( 2.5); }
    }
    else if(std::string(type)==std::string("+1sigma")){
      if(mass==110) {values.push_back(1.16); }
      if(mass==115) {values.push_back(1.11); }
      if(mass==120) {values.push_back(1.05); }
      if(mass==125) {values.push_back(1.07); }
      if(mass==130) {values.push_back(1.13); }
      if(mass==135) {values.push_back(1.31); }
      if(mass==140) {values.push_back(1.52); }
      if(mass==145) {values.push_back(1.88); }
    }
    else if(std::string(type)==std::string("expected")){
      if(mass==110) {values.push_back(0.836); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back(0.801); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back(0.756); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back(0.768); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back(0.816); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back(0.941); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back(  1.1); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back( 1.36); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("-1sigma")){
      if(mass==110) {values.push_back(0.603); }
      if(mass==115) {values.push_back(0.578); }
      if(mass==120) {values.push_back(0.545); }
      if(mass==125) {values.push_back(0.554); }
      if(mass==130) {values.push_back(0.589); }
      if(mass==135) {values.push_back(0.679); }
      if(mass==140) {values.push_back(0.792); }
      if(mass==145) {values.push_back(0.978); }
    }
    else if(std::string(type)==std::string("-2sigma")){
      if(mass==110) {values.push_back(0.454); }
      if(mass==115) {values.push_back(0.434); }
      if(mass==120) {values.push_back( 0.41); }
      if(mass==125) {values.push_back(0.416); }
      if(mass==130) {values.push_back(0.443); }
      if(mass==135) {values.push_back(0.511); }
      if(mass==140) {values.push_back(0.596); }
      if(mass==145) {values.push_back(0.735); }
    }
    else{
      std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		<< "       for the moment I'll stop here" << std::endl;
      exit(1);
    }
  }
  return;
}

