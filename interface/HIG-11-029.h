inline void
PlotLimits::prepareHIG_11_029(std::vector<double>& values, const char* type, double mass, bool initial)
{
  if(mssm_){
    if(std::string(type)==std::string("observed")){
      if(mass== 90) {values.push_back(12.246); if(initial) masses_.push_back(mass);}
      if(mass==100) {values.push_back(11.799); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back( 9.842); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back( 9.026); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 8.031); if(initial) masses_.push_back(mass);}
      if(mass==160) {values.push_back( 7.113); if(initial) masses_.push_back(mass);}
      if(mass==180) {values.push_back( 7.504); if(initial) masses_.push_back(mass);}
      if(mass==200) {values.push_back( 8.464); if(initial) masses_.push_back(mass);}
      if(mass==250) {values.push_back(13.755); if(initial) masses_.push_back(mass);}
      if(mass==300) {values.push_back(20.943); if(initial) masses_.push_back(mass);}
      if(mass==350) {values.push_back(29.124); if(initial) masses_.push_back(mass);}
      if(mass==400) {values.push_back(37.298); if(initial) masses_.push_back(mass);}
      if(mass==450) {values.push_back(45.178); if(initial) masses_.push_back(mass);}
      if(mass==500) {values.push_back(51.904); if(initial) masses_.push_back(mass);}
    }
    else if (std::string(type)==std::string("-2sigma")){
      if(mass== 90) {values.push_back( 5.194); }
      if(mass==100) {values.push_back( 6.492); }
      if(mass==120) {values.push_back( 4.500); }
      if(mass==130) {values.push_back( 5.369); }
      if(mass==140) {values.push_back( 5.615); }
      if(mass==160) {values.push_back( 5.574); }
      if(mass==180) {values.push_back( 6.747); }
      if(mass==200) {values.push_back( 7.845); }
      if(mass==250) {values.push_back(10.327); }
      if(mass==300) {values.push_back(13.469); }
      if(mass==350) {values.push_back(17.660); }
      if(mass==400) {values.push_back(21.923); }
      if(mass==450) {values.push_back(25.008); }
      if(mass==500) {values.push_back(30.315); }
    }
    else if (std::string(type)==std::string("-1sigma")){
      if(mass== 90) {values.push_back( 7.009); }
      if(mass==100) {values.push_back( 7.450); }
      if(mass==120) {values.push_back( 6.475); }
      if(mass==130) {values.push_back( 6.710); }
      if(mass==140) {values.push_back( 6.628); }
      if(mass==160) {values.push_back( 6.986); }
      if(mass==180) {values.push_back( 8.140); }
      if(mass==200) {values.push_back( 9.118); }
      if(mass==250) {values.push_back(12.344); }
      if(mass==300) {values.push_back(15.704); }
      if(mass==350) {values.push_back(20.093); }
      if(mass==400) {values.push_back(24.298); }
      if(mass==450) {values.push_back(29.164); }
      if(mass==500) {values.push_back(35.739); }
    }
    else if(std::string(type)==std::string("expected")){
      if(mass== 90) {values.push_back( 8.371); if(initial) masses_.push_back(mass);}
      if(mass==100) {values.push_back( 8.777); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back( 8.087); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back( 7.847); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 7.901); if(initial) masses_.push_back(mass);}
      if(mass==160) {values.push_back( 8.514); if(initial) masses_.push_back(mass);}
      if(mass==180) {values.push_back( 9.533); if(initial) masses_.push_back(mass);}
      if(mass==200) {values.push_back(10.519); if(initial) masses_.push_back(mass);}
      if(mass==250) {values.push_back(13.923); if(initial) masses_.push_back(mass);}
      if(mass==300) {values.push_back(18.378); if(initial) masses_.push_back(mass);}
      if(mass==350) {values.push_back(23.025); if(initial) masses_.push_back(mass);}
      if(mass==400) {values.push_back(27.886); if(initial) masses_.push_back(mass);}
      if(mass==450) {values.push_back(33.264); if(initial) masses_.push_back(mass);}
      if(mass==500) {values.push_back(40.510); if(initial) masses_.push_back(mass);}
    }
    else if (std::string(type)==std::string("+1sigma")){
      if(mass== 90) {values.push_back(10.605); }
      if(mass==100) {values.push_back(10.828); }
      if(mass==120) {values.push_back( 9.889); }
      if(mass==130) {values.push_back( 9.691); }
      if(mass==140) {values.push_back( 9.692); }
      if(mass==160) {values.push_back(10.419); }
      if(mass==180) {values.push_back(11.324); }
      if(mass==200) {values.push_back(12.811); }
      if(mass==250) {values.push_back(16.765); }
      if(mass==300) {values.push_back(21.415); }
      if(mass==350) {values.push_back(26.939); }
      if(mass==400) {values.push_back(32.449); }
      if(mass==450) {values.push_back(38.800); }
      if(mass==500) {values.push_back(47.145); }
    }
    else if (std::string(type)==std::string("+2sigma")){
      if(mass== 90) {values.push_back(12.836); }
      if(mass==100) {values.push_back(13.418); }
      if(mass==120) {values.push_back(11.957); }
      if(mass==130) {values.push_back(11.453); }
      if(mass==140) {values.push_back(11.557); }
      if(mass==160) {values.push_back(12.453); }
      if(mass==180) {values.push_back(13.762); }
      if(mass==200) {values.push_back(14.989); }
      if(mass==250) {values.push_back(19.373); }
      if(mass==300) {values.push_back(24.471); }
      if(mass==350) {values.push_back(31.113); }
      if(mass==400) {values.push_back(37.293); }
      if(mass==450) {values.push_back(44.728); }
      if(mass==500) {values.push_back(55.000); }
    }
    else{
      std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		<< "       for the moment I'll stop here" << std::endl;
      exit(1);
    }
  }
  else{ // SM Winter11 results
    if(std::string(type)==std::string("observed")){
      if(mass==110) {values.push_back( 3.20); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back( 3.19); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back( 3.62); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back( 4.27); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back( 5.08); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back( 5.39); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 5.46); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back( 7.00); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("+2sigma")){
      if(mass==110) {values.push_back( 6.63); }
      if(mass==115) {values.push_back( 5.86); }
      if(mass==120) {values.push_back( 6.07); }
      if(mass==125) {values.push_back( 6.01); }
      if(mass==130) {values.push_back( 6.43); }
      if(mass==135) {values.push_back( 7.87); }
      if(mass==140) {values.push_back( 7.99); }
      if(mass==145) {values.push_back(10.70); }
    }
    else if(std::string(type)==std::string("+1sigma")){
      if(mass==110) {values.push_back( 4.76); }
      if(mass==115) {values.push_back( 4.23); }
      if(mass==120) {values.push_back( 4.33); }
      if(mass==125) {values.push_back( 4.38); }
      if(mass==130) {values.push_back( 4.72); }
      if(mass==135) {values.push_back( 5.77); }
      if(mass==140) {values.push_back( 5.85); }
      if(mass==145) {values.push_back( 7.65); }
    }
    else if(std::string(type)==std::string("expected")){
      if(mass==110) {values.push_back( 3.30); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back( 2.97); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back( 3.03); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back( 3.05); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back( 3.31); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back( 4.06); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 4.17); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back( 5.45); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("-1sigma")){
      if(mass==110) {values.push_back( 2.36); }
      if(mass==115) {values.push_back( 2.13); }
      if(mass==120) {values.push_back( 2.17); }
      if(mass==125) {values.push_back( 2.19); }
      if(mass==130) {values.push_back( 2.37); }
      if(mass==135) {values.push_back( 2.96); }
      if(mass==140) {values.push_back( 2.99); }
      if(mass==145) {values.push_back( 3.97); }
    }
    else if(std::string(type)==std::string("-2sigma")){
      if(mass==110) {values.push_back( 1.83); }
      if(mass==115) {values.push_back( 1.61); }
      if(mass==120) {values.push_back( 1.65); }
      if(mass==125) {values.push_back( 1.75); }
      if(mass==130) {values.push_back( 1.82); }
      if(mass==135) {values.push_back( 2.25); }
      if(mass==140) {values.push_back( 2.39); }
      if(mass==145) {values.push_back( 3.06); }
    }
    else{
      std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		<< "       for the moment I'll stop here" << std::endl;
      exit(1);
    }
  }
  return;
}

