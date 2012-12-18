inline void
PlotLimits::prepareHIG_12_050(std::vector<double>& values, const char* type, double mass, bool initial)
{
  if(!mssm_){
    std::cout << "HIG-12-050 contained only MSSM limits" << std::endl;
    exit(1);
  }
  else{
    if(std::string(type)==std::string("observed")){
      if(mass== 90) {values.push_back(5.45); if(initial) masses_.push_back(mass);}
      if(mass==100) {values.push_back( 5.2); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back(4.69); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back(5.05); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 5.4); if(initial) masses_.push_back(mass);}
      if(mass==160) {values.push_back(5.05); if(initial) masses_.push_back(mass);}
      if(mass==180) {values.push_back(4.36); if(initial) masses_.push_back(mass);}
      if(mass==200) {values.push_back(4.88); if(initial) masses_.push_back(mass);}
      if(mass==250) {values.push_back( 5.3); if(initial) masses_.push_back(mass);}
      if(mass==300) {values.push_back(7.68); if(initial) masses_.push_back(mass);}
      if(mass==350) {values.push_back(10.4); if(initial) masses_.push_back(mass);}
      if(mass==400) {values.push_back(13.7); if(initial) masses_.push_back(mass);}
      if(mass==450) {values.push_back(17.3); if(initial) masses_.push_back(mass);}
      if(mass==500) {values.push_back(20.8); if(initial) masses_.push_back(mass);}
      if(mass==600) {values.push_back(29.7); if(initial) masses_.push_back(mass);}
      if(mass==700) {values.push_back(39.3); if(initial) masses_.push_back(mass);}
      if(mass==800) {values.push_back(48.6); if(initial) masses_.push_back(mass);}
    }
    else if (std::string(type)==std::string("-2sigma")){
      if(mass== 90) {values.push_back(10.6); }
      if(mass==100) {values.push_back( 9.3); }
      if(mass==120) {values.push_back(7.54); }
      if(mass==130) {values.push_back(6.89); }
      if(mass==140) {values.push_back(6.77); }
      if(mass==160) {values.push_back( 7.6); }
      if(mass==180) {values.push_back(8.54); }
      if(mass==200) {values.push_back(9.44); }
      if(mass==250) {values.push_back(12.7); }
      if(mass==300) {values.push_back(16.6); }
      if(mass==350) {values.push_back(  21); }
      if(mass==400) {values.push_back(24.6); }
      if(mass==450) {values.push_back(29.4); }
      if(mass==500) {values.push_back(35.8); }
      if(mass==600) {values.push_back(47.4); }
      if(mass==700) {values.push_back(63.4); }
      if(mass==800) {values.push_back(98.3); }
    }
    else if (std::string(type)==std::string("-1sigma")){
      if(mass== 90) {values.push_back(8.91); }
      if(mass==100) {values.push_back(7.85); }
      if(mass==120) {values.push_back(5.95); }
      if(mass==130) {values.push_back(5.74); }
      if(mass==140) {values.push_back(5.79); }
      if(mass==160) {values.push_back(6.18); }
      if(mass==180) {values.push_back(7.49); }
      if(mass==200) {values.push_back( 8.3); }
      if(mass==250) {values.push_back(11.1); }
      if(mass==300) {values.push_back(14.4); }
      if(mass==350) {values.push_back(18.7); }
      if(mass==400) {values.push_back(22.2); }
      if(mass==450) {values.push_back(26.2); }
      if(mass==500) {values.push_back(31.1); }
      if(mass==600) {values.push_back(41.7); }
      if(mass==700) {values.push_back(55.9); }
      if(mass==800) {values.push_back(  74); }
    }
    else if(std::string(type)==std::string("expected")){
      if(mass== 90) {values.push_back(7.19); if(initial) masses_.push_back(mass);}
      if(mass==100) {values.push_back(5.89); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back(4.92); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back(4.94); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back(5.23); if(initial) masses_.push_back(mass);}
      if(mass==160) {values.push_back(5.54); if(initial) masses_.push_back(mass);}
      if(mass==180) {values.push_back(5.96); if(initial) masses_.push_back(mass);}
      if(mass==200) {values.push_back(6.91); if(initial) masses_.push_back(mass);}
      if(mass==250) {values.push_back(9.26); if(initial) masses_.push_back(mass);}
      if(mass==300) {values.push_back(12.4); if(initial) masses_.push_back(mass);}
      if(mass==350) {values.push_back(16.1); if(initial) masses_.push_back(mass);}
      if(mass==400) {values.push_back(19.1); if(initial) masses_.push_back(mass);}
      if(mass==450) {values.push_back(  23); if(initial) masses_.push_back(mass);}
      if(mass==500) {values.push_back(26.9); if(initial) masses_.push_back(mass);}
      if(mass==600) {values.push_back(36.4); if(initial) masses_.push_back(mass);}
      if(mass==700) {values.push_back(47.8); if(initial) masses_.push_back(mass);}
      if(mass==800) {values.push_back(61.4); if(initial) masses_.push_back(mass);}
    }
    else if (std::string(type)==std::string("+1sigma")){
      if(mass== 90) {values.push_back(5.18); }
      if(mass==100) {values.push_back(4.41); }
      if(mass==120) {values.push_back(3.51); }
      if(mass==130) {values.push_back(3.84); }
      if(mass==140) {values.push_back(4.46); }
      if(mass==160) {values.push_back(4.84); }
      if(mass==180) {values.push_back(5.42); }
      if(mass==200) {values.push_back(5.69); }
      if(mass==250) {values.push_back( 7.7); }
      if(mass==300) {values.push_back(10.5); }
      if(mass==350) {values.push_back(13.5); }
      if(mass==400) {values.push_back(16.3); }
      if(mass==450) {values.push_back(19.4); }
      if(mass==500) {values.push_back(  23); }
      if(mass==600) {values.push_back(30.3); }
      if(mass==700) {values.push_back(39.8); }
      if(mass==800) {values.push_back(  51); }
    }
    else if (std::string(type)==std::string("+2sigma")){
      if(mass== 90) {values.push_back(3.25); }
      if(mass==100) {values.push_back(2.93); }
      if(mass==120) {values.push_back(2.53); }
      if(mass==130) {values.push_back(   3); }
      if(mass==140) {values.push_back(3.54); }
      if(mass==160) {values.push_back(4.02); }
      if(mass==180) {values.push_back(4.78); }
      if(mass==200) {values.push_back(5.01); }
      if(mass==250) {values.push_back(5.99); }
      if(mass==300) {values.push_back( 8.3); }
      if(mass==350) {values.push_back(10.8); }
      if(mass==400) {values.push_back(12.9); }
      if(mass==450) {values.push_back(  16); }
      if(mass==500) {values.push_back(18.7); }
      if(mass==600) {values.push_back(24.8); }
      if(mass==700) {values.push_back(32.2); }
      if(mass==800) {values.push_back(40.8); }
    }
    else{
      std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		<< "       for the moment I'll stop here" << std::endl;
      exit(1);
    }
  }
}

