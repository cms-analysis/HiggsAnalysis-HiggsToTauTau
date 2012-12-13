#include <iostream>

#include "HiggsAnalysis/HiggsToTauTau/macros/mssm_xs_tools.h"
#include "HiggsAnalysis/HiggsToTauTau/macros/mssm_xs_tools.C"

void 
mssm_xs(char* path, double mA, double tanb)
{
  mssm_xs_tools xs;
  xs.SetInput(path);

  double xs_eff_ggH_tautau[4];
  std::cout << "MSSM Cross Section [ggH](tautau):" << std::endl;
  xs_eff_ggH_tautau[0] = xs.Give_Xsec_ggFA(mA, tanb)*xs.Give_BR_A_tautau(mA, tanb);
  std::cout << " -> xsec(ggA)(tautau):\t" << xs.Give_Xsec_ggFA(mA, tanb) << "\t --- \t" << xs.Give_BR_A_tautau(mA, tanb) << std::endl;
  xs_eff_ggH_tautau[1] = xs.Give_Xsec_ggFH(mA, tanb)*xs.Give_BR_H_tautau(mA, tanb);
  std::cout << " -> xsec(ggH)(tautau):\t" << xs.Give_Xsec_ggFH(mA, tanb) << "\t --- \t" << xs.Give_BR_H_tautau(mA, tanb) << std::endl;
  xs_eff_ggH_tautau[2] = xs.Give_Xsec_ggFh(mA, tanb)*xs.Give_BR_h_tautau(mA, tanb);
  std::cout << " -> xsec(ggh)(tautau):\t" << xs.Give_Xsec_ggFh(mA, tanb) << "\t --- \t" << xs.Give_BR_h_tautau(mA, tanb) << std::endl;
  xs_eff_ggH_tautau[3] = xs_eff_ggH_tautau[0]+xs_eff_ggH_tautau[1]+xs_eff_ggH_tautau[2];
  std::cout << " -> xsec(cmb)(tautau):\t" << xs_eff_ggH_tautau[3] << std::endl;
  double xs_eff_bbH_tautau[4];
  std::cout << "MSSM Cross Section [bbH](tautau):" << std::endl;
  xs_eff_bbH_tautau[0] = xs.GiveXsec_Santander_A(mA, tanb)*xs.Give_BR_A_tautau(mA, tanb);
  std::cout << " -> xsec(bbA):\t" << xs.GiveXsec_Santander_A(mA, tanb) << "\t --- \t" << xs.Give_BR_A_tautau(mA, tanb) << std::endl;
  xs_eff_bbH_tautau[1] = xs.GiveXsec_Santander_H(mA, tanb)*xs.Give_BR_H_tautau(mA, tanb);
  std::cout << " -> xsec(bbH):\t" << xs.GiveXsec_Santander_H(mA, tanb) << "\t --- \t" << xs.Give_BR_H_tautau(mA, tanb) << std::endl;
  xs_eff_bbH_tautau[2] = xs.GiveXsec_Santander_h(mA, tanb)*xs.Give_BR_h_tautau(mA, tanb);
  std::cout << " -> xsec(bbh):\t" << xs.GiveXsec_Santander_h(mA, tanb) << "\t --- \t" << xs.Give_BR_h_tautau(mA, tanb) << std::endl;
  xs_eff_bbH_tautau[3] = xs_eff_bbH_tautau[0]+xs_eff_bbH_tautau[1]+xs_eff_bbH_tautau[2];
  std::cout << " -> xsec(cmb):\t" << xs_eff_bbH_tautau[3] << std::endl;
  std::cout << std::endl;

  double xs_eff_ggH_mumu[4];
  std::cout << "MSSM Cross Section [ggH](mumu):" << std::endl;
  xs_eff_ggH_mumu[0] = xs.Give_Xsec_ggFA(mA, tanb)*xs.Give_BR_A_mumu(mA, tanb);
  std::cout << " -> xsec(ggA)(mumu):\t" << xs.Give_Xsec_ggFA(mA, tanb) << "\t --- \t" << xs.Give_BR_A_mumu(mA, tanb) << std::endl;
  xs_eff_ggH_mumu[1] = xs.Give_Xsec_ggFH(mA, tanb)*xs.Give_BR_H_mumu(mA, tanb);
  std::cout << " -> xsec(ggH)(mumu):\t" << xs.Give_Xsec_ggFH(mA, tanb) << "\t --- \t" << xs.Give_BR_H_mumu(mA, tanb) << std::endl;
  xs_eff_ggH_mumu[2] = xs.Give_Xsec_ggFh(mA, tanb)*xs.Give_BR_h_mumu(mA, tanb);
  std::cout << " -> xsec(ggh)(mumu):\t" << xs.Give_Xsec_ggFh(mA, tanb) << "\t --- \t" << xs.Give_BR_h_mumu(mA, tanb) << std::endl;
  xs_eff_ggH_mumu[3] = xs_eff_ggH_mumu[0]+xs_eff_ggH_mumu[1]+xs_eff_ggH_mumu[2];
  std::cout << " -> xsec(cmb)(mumu):\t" << xs_eff_ggH_mumu[3] << std::endl;
  double xs_eff_bbH_mumu[4];
  std::cout << "MSSM Cross Section [bbH](mumu):" << std::endl;
  xs_eff_bbH_mumu[0] = xs.GiveXsec_Santander_A(mA, tanb)*xs.Give_BR_A_mumu(mA, tanb);
  std::cout << " -> xsec(bbA)(mumu):\t" << xs.GiveXsec_Santander_A(mA, tanb) << "\t --- \t" << xs.Give_BR_A_mumu(mA, tanb) << std::endl;
  xs_eff_bbH_mumu[1] = xs.GiveXsec_Santander_H(mA, tanb)*xs.Give_BR_H_mumu(mA, tanb);
  std::cout << " -> xsec(bbH)(mumu):\t" << xs.GiveXsec_Santander_H(mA, tanb) << "\t --- \t" << xs.Give_BR_H_mumu(mA, tanb) << std::endl;
  xs_eff_bbH_mumu[2] = xs.GiveXsec_Santander_h(mA, tanb)*xs.Give_BR_h_mumu(mA, tanb);
  std::cout << " -> xsec(bbh)(mumu):\t" << xs.GiveXsec_Santander_h(mA, tanb) << "\t --- \t" << xs.Give_BR_h_mumu(mA, tanb) << std::endl;
  xs_eff_bbH_mumu[3] = xs_eff_bbH_mumu[0]+xs_eff_bbH_mumu[1]+xs_eff_bbH_mumu[2];
  std::cout << " -> xsec(cmb)(mumu):\t" << xs_eff_bbH_mumu[3] << std::endl;
  std::cout << std::endl;

  double xs_eff_ggH_bb[4];
  std::cout << "MSSM Cross Section [ggH](bb):" << std::endl;
  xs_eff_ggH_bb[0] = xs.Give_Xsec_ggFA(mA, tanb)*xs.Give_BR_A_bb(mA, tanb);
  std::cout << " -> xsec(ggA)(bb):\t" << xs.Give_Xsec_ggFA(mA, tanb) << "\t --- \t" << xs.Give_BR_A_bb(mA, tanb) << std::endl;
  xs_eff_ggH_bb[1] = xs.Give_Xsec_ggFH(mA, tanb)*xs.Give_BR_H_bb(mA, tanb);
  std::cout << " -> xsec(ggH)(bb):\t" << xs.Give_Xsec_ggFH(mA, tanb) << "\t --- \t" << xs.Give_BR_H_bb(mA, tanb) << std::endl;
  xs_eff_ggH_bb[2] = xs.Give_Xsec_ggFh(mA, tanb)*xs.Give_BR_h_bb(mA, tanb);
  std::cout << " -> xsec(ggh)(bb):\t" << xs.Give_Xsec_ggFh(mA, tanb) << "\t --- \t" << xs.Give_BR_h_bb(mA, tanb) << std::endl;
  xs_eff_ggH_bb[3] = xs_eff_ggH_bb[0]+xs_eff_ggH_bb[1]+xs_eff_ggH_bb[2];
  std::cout << " -> xsec(cmb)(bb):\t" << xs_eff_ggH_bb[3] << std::endl;
  double xs_eff_bbH_bb[4];
  std::cout << "MSSM Cross Section [bbH](bb):" << std::endl;
  xs_eff_bbH_bb[0] = xs.GiveXsec_Santander_A(mA, tanb)*xs.Give_BR_A_bb(mA, tanb);
  std::cout << " -> xsec(bbA)(bb):\t" << xs.GiveXsec_Santander_A(mA, tanb) << "\t --- \t" << xs.Give_BR_A_bb(mA, tanb) << std::endl;
  xs_eff_bbH_bb[1] = xs.GiveXsec_Santander_H(mA, tanb)*xs.Give_BR_H_bb(mA, tanb);
  std::cout << " -> xsec(bbH)(bb):\t" << xs.GiveXsec_Santander_H(mA, tanb) << "\t --- \t" << xs.Give_BR_H_bb(mA, tanb) << std::endl;
  xs_eff_bbH_bb[2] = xs.GiveXsec_Santander_h(mA, tanb)*xs.Give_BR_h_bb(mA, tanb);
  std::cout << " -> xsec(bbh)(bb):\t" << xs.GiveXsec_Santander_h(mA, tanb) << "\t --- \t" << xs.Give_BR_h_bb(mA, tanb) << std::endl;
  xs_eff_bbH_bb[3] = xs_eff_bbH_bb[0]+xs_eff_bbH_bb[1]+xs_eff_bbH_bb[2];
  std::cout << " -> xsec(cmb)(bb):\t" << xs_eff_bbH_bb[3] << std::endl;
  std::cout << std::endl;
  return;
}
