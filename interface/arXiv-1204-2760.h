#include "TGraph.h"

inline void
PlotLimits::arXiv_1204_2760(TGraph* graph)
{
  /* HIGG-2012-09 H+->tau search (4.6/fb)
     https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/HIGG-2012-09/
  */
  graph->SetPoint(0, 89.73892423637687   , 18.69109947643979 );
  graph->SetPoint(1, 100.04636912168667  , 16.387434554973822);
  graph->SetPoint(2, 110.1275444321837   , 13.350785340314134);
  graph->SetPoint(3, 119.87562510271641  , 11.465968586387437);
  graph->SetPoint(4, 129.8567252834973   , 12.722513089005234);
  graph->SetPoint(5, 139.84457539971356  , 16.387434554973822);
  graph->SetPoint(6, 150.07366233888197  , 26.12565445026178 );
  graph->SetPoint(7, 160.2267391355387   , 48.743455497382215);
}
  
