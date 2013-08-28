#include "TGraph.h"

inline void
PlotLimits::arXiv_1205_5736(TGraph* graph)
{
  /* CMS-11-019 H+->tau search (2/fb)
     https://twiki.cern.ch/twiki/bin/view/CMSPublic/Hig11019TWiki
  */
  graph->SetPoint(0, 87.908369129999997 , 18.789237668161434 );
  graph->SetPoint(1, 112.22192412       , 24.798206278026907 );
  graph->SetPoint(2, 119.52907261999999 , 39.058295964125563 );
  graph->SetPoint(3, 120.42727809       , 52.331838565022423 );
}
