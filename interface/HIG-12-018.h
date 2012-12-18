inline void
PlotLimits::prepareHIG_12_018(std::vector<double>& values, const char* type, double mass, bool initial)
{
  if(mssm_){
    std::cout << "HIG-12-018 contained only SM limits" << std::endl;
    exit(1);
  }
  else{
    if(std::string(type)==std::string("observed")){
      if(mass==110) {values.push_back(1.21); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back( 1.2); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back(1.19); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back(1.06); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back( 1.2); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back(1.81); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 2.2); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back(3.36); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("+2sigma")){
      if(mass==110) {values.push_back(2.52); }
      if(mass==115) {values.push_back(2.47); }
      if(mass==120) {values.push_back(2.41); }
      if(mass==125) {values.push_back(2.36); }
      if(mass==130) {values.push_back(2.48); }
      if(mass==135) {values.push_back(2.84); }
      if(mass==140) {values.push_back(3.33); }
      if(mass==145) {values.push_back(4.35); }
    }
    else if(std::string(type)==std::string("+1sigma")){
      if(mass==110) {values.push_back( 1.9); }
      if(mass==115) {values.push_back(1.86); }
      if(mass==120) {values.push_back(1.81); }
      if(mass==125) {values.push_back(1.78); }
      if(mass==130) {values.push_back(1.87); }
      if(mass==135) {values.push_back(2.14); }
      if(mass==140) {values.push_back(2.51); }
      if(mass==145) {values.push_back(3.28); }
    }
    else if(std::string(type)==std::string("expected")){
      if(mass==110) {values.push_back(1.37); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back(1.34); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back( 1.3); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back(1.28); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back(1.34); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back(1.54); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 1.8); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back(2.36); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("-1sigma")){
      if(mass==110) {values.push_back(0.987); }
      if(mass==115) {values.push_back(0.964); }
      if(mass==120) {values.push_back(0.942); }
      if(mass==125) {values.push_back(0.925); }
      if(mass==130) {values.push_back( 0.97); }
      if(mass==135) {values.push_back( 1.11); }
      if(mass==140) {values.push_back(  1.3); }
      if(mass==145) {values.push_back(  1.7); }
    }
    else if(std::string(type)==std::string("-2sigma")){
      if(mass==110) {values.push_back(0.742); }
      if(mass==115) {values.push_back(0.725); }
      if(mass==120) {values.push_back(0.708); }
      if(mass==125) {values.push_back(0.695); }
      if(mass==130) {values.push_back(0.729); }
      if(mass==135) {values.push_back(0.835); }
      if(mass==140) {values.push_back(0.979); }
      if(mass==145) {values.push_back( 1.28); }
    }
    else{
      std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		<< "       for the moment I'll stop here" << std::endl;
      exit(1);
    }
  }
  return;
}

