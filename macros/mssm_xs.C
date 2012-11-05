#include <iostream>

#include "HiggsAnalysis/HiggsToTauTau/macros/mssm_xs_tools.h"
#include "HiggsAnalysis/HiggsToTauTau/macros/mssm_xs_tools.C"

void 
mssm_xs(char* path, double mA, double tanb)
{
  mssm_xs_tools xs;
  xs.SetInput(path);

  double xs_eff_ggH[4];
  std::cout << "MSSM Cross Section [ggH]:" << std::endl;
  xs_eff_ggH[0] = xs.Give_Xsec_ggFA(mA, tanb)*xs.Give_BR_A_tautau(mA, tanb);
  std::cout << " -> xsec(ggA):\t" << xs.Give_Xsec_ggFA(mA, tanb) << "\t --- \t" << xs.Give_BR_A_tautau(mA, tanb) << std::endl;
  xs_eff_ggH[1] = xs.Give_Xsec_ggFH(mA, tanb)*xs.Give_BR_H_tautau(mA, tanb);
  std::cout << " -> xsec(ggH):\t" << xs.Give_Xsec_ggFH(mA, tanb) << "\t --- \t" << xs.Give_BR_H_tautau(mA, tanb) << std::endl;
  xs_eff_ggH[2] = xs.Give_Xsec_ggFh(mA, tanb)*xs.Give_BR_h_tautau(mA, tanb);
  std::cout << " -> xsec(ggh):\t" << xs.Give_Xsec_ggFh(mA, tanb) << "\t --- \t" << xs.Give_BR_h_tautau(mA, tanb) << std::endl;
  xs_eff_ggH[3] = xs_eff_ggH[0]+xs_eff_ggH[1]+xs_eff_ggH[2];
  std::cout << " -> xsec(cmb):\t" << xs_eff_ggH[3] << std::endl;
  std::cout << std::endl;
  double xs_eff_bbH[4];
  std::cout << "MSSM Cross Section [bbH]:" << std::endl;
  xs_eff_bbH[0] = xs.GiveXsec_Santander_A(mA, tanb)*xs.Give_BR_A_tautau(mA, tanb);
  std::cout << " -> xsec(ggA):\t" << xs.GiveXsec_Santander_A(mA, tanb) << "\t --- \t" << xs.Give_BR_A_tautau(mA, tanb) << std::endl;
  xs_eff_bbH[1] = xs.GiveXsec_Santander_H(mA, tanb)*xs.Give_BR_H_tautau(mA, tanb);
  std::cout << " -> xsec(bbH):\t" << xs.GiveXsec_Santander_H(mA, tanb) << "\t --- \t" << xs.Give_BR_H_tautau(mA, tanb) << std::endl;
  xs_eff_bbH[2] = xs.GiveXsec_Santander_h(mA, tanb)*xs.Give_BR_h_tautau(mA, tanb);
  std::cout << " -> xsec(ggh):\t" << xs.GiveXsec_Santander_h(mA, tanb) << "\t --- \t" << xs.Give_BR_h_tautau(mA, tanb) << std::endl;
  xs_eff_bbH[3] = xs_eff_bbH[0]+xs_eff_bbH[1]+xs_eff_bbH[2];
  std::cout << " -> xsec(cmb):\t" << xs_eff_bbH[3] << std::endl;
  return;
}
