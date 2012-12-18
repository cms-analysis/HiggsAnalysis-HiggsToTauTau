inline void
PlotLimits::prepareHIG_11_020(std::vector<double>& values, const char* type, bool xsec, double mass, bool initial)
{
  if(mssm_){
    if(std::string(type)==std::string("observed")){
      if(xsec){
	// xsec limits
	if(mass== 90) {values.push_back(14.076); if(initial) masses_.push_back(mass);}
	if(mass==100) {values.push_back( 7.995); if(initial) masses_.push_back(mass);}
	if(mass==120) {values.push_back( 4.501); if(initial) masses_.push_back(mass);}
	if(mass==130) {values.push_back( 4.095); if(initial) masses_.push_back(mass);}
	if(mass==140) {values.push_back( 3.834); if(initial) masses_.push_back(mass);}
	if(mass==160) {values.push_back( 3.103); if(initial) masses_.push_back(mass);}
	if(mass==180) {values.push_back( 2.296); if(initial) masses_.push_back(mass);}
	if(mass==200) {values.push_back( 2.353); if(initial) masses_.push_back(mass);}
	if(mass==250) {values.push_back( 1.700); if(initial) masses_.push_back(mass);}
	if(mass==300) {values.push_back( 1.227); if(initial) masses_.push_back(mass);}
	if(mass==400) {values.push_back( 0.600); if(initial) masses_.push_back(mass);}
	if(mass==450) {values.push_back( 0.416); if(initial) masses_.push_back(mass);}
	if(mass==400) {values.push_back( 0.335); if(initial) masses_.push_back(mass);}
      }
      else{
	// tanb limits
	if(mass== 90) {values.push_back(8.50 ); if(initial) masses_.push_back(mass);}
	if(mass==100) {values.push_back(7.92 ); if(initial) masses_.push_back(mass);}
	if(mass==120) {values.push_back(8.67 ); if(initial) masses_.push_back(mass);}
	if(mass==130) {values.push_back(7.78 ); if(initial) masses_.push_back(mass);}
	if(mass==140) {values.push_back(10.99); if(initial) masses_.push_back(mass);}
	if(mass==160) {values.push_back(12.69); if(initial) masses_.push_back(mass);}
	if(mass==180) {values.push_back(14.00); if(initial) masses_.push_back(mass);}
	if(mass==200) {values.push_back(17.66); if(initial) masses_.push_back(mass);}
	if(mass==250) {values.push_back(24.46); if(initial) masses_.push_back(mass);}
	if(mass==300) {values.push_back(31.68); if(initial) masses_.push_back(mass);}
	if(mass==400) {values.push_back(44.82); if(initial) masses_.push_back(mass);}
	if(mass==450) {values.push_back(50.62); if(initial) masses_.push_back(mass);}
	if(mass==500) {values.push_back(59.53); if(initial) masses_.push_back(mass);}
      }
    }
    else if (std::string(type)==std::string("+2sigma")){
      if(xsec){
	// xsec limits
	if(mass== 90) {values.push_back(34.598); }
	if(mass==100) {values.push_back(24.746); }
	if(mass==120) {values.push_back(11.224); }
	if(mass==130) {values.push_back( 9.260); }
	if(mass==140) {values.push_back( 6.884); }
	if(mass==160) {values.push_back( 5.011); }
	if(mass==180) {values.push_back( 3.504); }
	if(mass==200) {values.push_back( 2.916); }
	if(mass==250) {values.push_back( 1.848); }
	if(mass==300) {values.push_back( 1.279); }
	if(mass==400) {values.push_back( 0.736); }
	if(mass==450) {values.push_back( 0.579); }
	if(mass==500) {values.push_back( 0.457); }
      }
      else{
	// tanb limits
	if(mass== 90) {values.push_back(13.33); }
	if(mass==100) {values.push_back(13.90); }
	if(mass==120) {values.push_back(13.86); }
	if(mass==130) {values.push_back(13.16); }
	if(mass==140) {values.push_back(14.81); }
	if(mass==160) {values.push_back(16.13); }
	if(mass==180) {values.push_back(17.20); }
	if(mass==200) {values.push_back(19.64); }
	if(mass==250) {values.push_back(25.48); }
	if(mass==300) {values.push_back(32.29); }
	if(mass==400) {values.push_back(49.22); }
	if(mass==450) {values.push_back(58.79); }
	if(mass==500) {values.push_back(69.25); }
      }
    }
    else if (std::string(type)==std::string("+1sigma")){
      if(xsec){
	/// xsec limits
	if(mass== 90) {values.push_back(24.864); }
	if(mass==100) {values.push_back(18.287); }
	if(mass==120) {values.push_back( 8.397); }
	if(mass==130) {values.push_back( 6.899); }
	if(mass==140) {values.push_back( 5.134); }
	if(mass==160) {values.push_back( 3.718); }
	if(mass==180) {values.push_back( 2.616); }
	if(mass==200) {values.push_back( 2.190); }
	if(mass==250) {values.push_back( 1.351); }
	if(mass==300) {values.push_back( 0.955); }
	if(mass==400) {values.push_back( 0.538); }
	if(mass==450) {values.push_back( 0.416); }
	if(mass==500) {values.push_back( 0.335); }
      }
      else{
	// tanb limits
	if(mass== 90) {values.push_back(11.31); }
	if(mass==100) {values.push_back(11.99); }
	if(mass==120) {values.push_back(12.02); }
	if(mass==130) {values.push_back(11.05); }
	if(mass==140) {values.push_back(12.77); }
	if(mass==160) {values.push_back(13.91); }
	if(mass==180) {values.push_back(14.92); }
	if(mass==200) {values.push_back(17.06); }
	if(mass==250) {values.push_back(21.88); }
	if(mass==300) {values.push_back(28.14); }
	if(mass==400) {values.push_back(42.65); }
	if(mass==450) {values.push_back(50.62); }
	if(mass==500) {values.push_back(59.53); }
      }
    }
    else if(std::string(type)==std::string("expected")){
      if(xsec){
	// xsec limits
	if(mass== 90) {values.push_back(17.802); if(initial) masses_.push_back(mass);}
	if(mass==100) {values.push_back(12.569); if(initial) masses_.push_back(mass);}
	if(mass==120) {values.push_back( 6.001); if(initial) masses_.push_back(mass);}
	if(mass==130) {values.push_back( 4.823); if(initial) masses_.push_back(mass);}
	if(mass==140) {values.push_back( 3.655); if(initial) masses_.push_back(mass);}
	if(mass==160) {values.push_back( 2.630); if(initial) masses_.push_back(mass);}
	if(mass==180) {values.push_back( 1.883); if(initial) masses_.push_back(mass);}
	if(mass==200) {values.push_back( 1.543); if(initial) masses_.push_back(mass);}
	if(mass==250) {values.push_back( 0.957); if(initial) masses_.push_back(mass);}
	if(mass==300) {values.push_back( 0.661); if(initial) masses_.push_back(mass);}
	if(mass==400) {values.push_back( 0.376); if(initial) masses_.push_back(mass);}
	if(mass==450) {values.push_back( 0.294); if(initial) masses_.push_back(mass);}
	if(mass==500) {values.push_back( 0.254); if(initial) masses_.push_back(mass);}
      }
      else{
	// tanb limtis
	if(mass== 90) {values.push_back(9.56 ); if(initial) masses_.push_back(mass);}
	if(mass==100) {values.push_back(9.96 ); if(initial) masses_.push_back(mass);}
	if(mass==120) {values.push_back(10.12); if(initial) masses_.push_back(mass);}
	if(mass==130) {values.push_back(8.75 ); if(initial) masses_.push_back(mass);}
	if(mass==140) {values.push_back(10.71); if(initial) masses_.push_back(mass);}
	if(mass==160) {values.push_back(11.69); if(initial) masses_.push_back(mass);}
	if(mass==180) {values.push_back(12.67); if(initial) masses_.push_back(mass);}
	if(mass==200) {values.push_back(14.37); if(initial) masses_.push_back(mass);}
	if(mass==250) {values.push_back(18.56); if(initial) masses_.push_back(mass);}
	if(mass==300) {values.push_back(23.75); if(initial) masses_.push_back(mass);}
	if(mass==400) {values.push_back(36.32); if(initial) masses_.push_back(mass);}
	if(mass==450) {values.push_back(43.41); if(initial) masses_.push_back(mass);}
	if(mass==500) {values.push_back(52.65); if(initial) masses_.push_back(mass);}
      }
    }
    else if (std::string(type)==std::string("-1sigma")){
      if(xsec){
	// xsec limits
	if(mass== 90) {values.push_back(12.360); }
	if(mass==100) {values.push_back( 8.644); }
	if(mass==120) {values.push_back( 4.062); }
	if(mass==130) {values.push_back( 3.381); }
	if(mass==140) {values.push_back( 2.619); }
	if(mass==160) {values.push_back( 1.877); }
	if(mass==180) {values.push_back( 1.323); }
	if(mass==200) {values.push_back( 1.119); }
	if(mass==250) {values.push_back( 0.701); }
	if(mass==300) {values.push_back( 0.470); }
	if(mass==400) {values.push_back( 0.264); }
	if(mass==450) {values.push_back( 0.213); }
	if(mass==500) {values.push_back( 0.213); }
      }
      else{
	// tanb limits
	if(mass== 90) {values.push_back(7.98 ); }
	if(mass==100) {values.push_back(8.23 ); }
	if(mass==120) {values.push_back(8.19 ); }
	if(mass==130) {values.push_back(6.68 ); }
	if(mass==140) {values.push_back(8.95 ); }
	if(mass==160) {values.push_back(9.87 ); }
	if(mass==180) {values.push_back(10.66); }
	if(mass==200) {values.push_back(12.31); }
	if(mass==250) {values.push_back(16.03); }
	if(mass==300) {values.push_back(20.37); }
	if(mass==400) {values.push_back(31.13); }
	if(mass==450) {values.push_back(37.77); }
	if(mass==500) {values.push_back(48.74); }
      }
    }
    else if (std::string(type)==std::string("-2sigma")){
      if(xsec){
	// xsec limits
	if(mass== 90) {values.push_back( 9.211); }
	if(mass==100) {values.push_back( 6.216); }
	if(mass==120) {values.push_back( 2.891); }
	if(mass==130) {values.push_back( 2.579); }
	if(mass==140) {values.push_back( 1.912); }
	if(mass==160) {values.push_back( 1.450); }
	if(mass==180) {values.push_back( 0.945); }
	if(mass==200) {values.push_back( 0.703); }
	if(mass==250) {values.push_back( 0.518); }
	if(mass==300) {values.push_back( 0.368); }
	if(mass==400) {values.push_back( 0.213); }
	if(mass==450) {values.push_back( 0.132); }
	if(mass==500) {values.push_back( 0.172); }
      }
      else{
	// tanb limits
	if(mass== 90) {values.push_back(6.85 ); }
	if(mass==100) {values.push_back(6.95 ); }
	if(mass==120) {values.push_back(6.65 ); }
	if(mass==130) {values.push_back(5.14 ); }
	if(mass==140) {values.push_back(7.43 ); }
	if(mass==160) {values.push_back(8.64 ); }
	if(mass==180) {values.push_back(9.07 ); }
	if(mass==200) {values.push_back(9.84 ); }
	if(mass==250) {values.push_back(13.92); }
	if(mass==300) {values.push_back(18.30); }
	if(mass==400) {values.push_back(28.40); }
	if(mass==450) {values.push_back(30.95); }
	if(mass==500) {values.push_back(44.45); }
      }
    }
    else{
      std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		<< "       for the moment I'll stop here" << std::endl;
      exit(1);
    }
  }
  else{
    if(std::string(type)==std::string("observed")){
      if(mass==110) {values.push_back( 5.984); if(initial) masses_.push_back(mass);}
      if(mass==150) {values.push_back( 7.018); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back( 7.618); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back( 7.106); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back(10.029); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back(10.352); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back(12.415); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back(17.923); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("+2sigma")){
      if(mass==110) {values.push_back(10.971); }
      if(mass==115) {values.push_back(11.788); }
      if(mass==120) {values.push_back(11.099); }
      if(mass==125) {values.push_back(11.190); }
      if(mass==130) {values.push_back(12.661); }
      if(mass==135) {values.push_back(14.527); }
      if(mass==140) {values.push_back(17.831); }
      if(mass==145) {values.push_back(24.432); }
    }
    else if(std::string(type)==std::string("+1sigma")){
      if(mass==110) {values.push_back( 7.839); }
      if(mass==115) {values.push_back( 8.663); }
      if(mass==120) {values.push_back( 8.010); }
      if(mass==125) {values.push_back( 8.108); }
      if(mass==130) {values.push_back( 9.178); }
      if(mass==135) {values.push_back(10.558); }
      if(mass==140) {values.push_back(12.944); }
      if(mass==145) {values.push_back(17.708); }
    }
    else if(std::string(type)==std::string("expected")){
      if(mass==110) {values.push_back( 5.402); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back( 6.139); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back( 5.606); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back( 5.706); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back( 6.439); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back( 7.430); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 9.124); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back(12.534); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("-1sigma")){
      if(mass==110) {values.push_back( 3.911); }
      if(mass==115) {values.push_back( 4.443); }
      if(mass==120) {values.push_back( 4.013); }
      if(mass==125) {values.push_back( 3.997); }
      if(mass==130) {values.push_back( 4.563); }
      if(mass==135) {values.push_back( 5.401); }
      if(mass==140) {values.push_back( 6.522); }
      if(mass==145) {values.push_back( 8.975); }
    }
    else if(std::string(type)==std::string("-2sigma")){
      if(mass==110) {values.push_back( 3.114); }
      if(mass==115) {values.push_back( 3.342); }
      if(mass==120) {values.push_back( 3.110); }
      if(mass==125) {values.push_back( 3.117); }
      if(mass==130) {values.push_back( 3.440); }
      if(mass==135) {values.push_back( 4.209); }
      if(mass==140) {values.push_back( 5.210); }
      if(mass==145) {values.push_back( 7.148); }
    }
    else{
      std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		<< "       for the moment I'll stop here" << std::endl;
      exit(1);
    }
  }
  return;
}

