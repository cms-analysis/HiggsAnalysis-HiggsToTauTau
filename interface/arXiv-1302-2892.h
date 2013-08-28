#include "TGraph.h"

inline void
PlotLimits::arXiv_1302_2892(TGraph* graph)
{
  /* CMS-12-033 bbH->bbbb search (4.8/fb)
     https://twiki.cern.ch/twiki/bin/view/CMSPublic/Hig12033TWiki
  */
  graph->SetPoint( 0,  90 , 21.8 );
  graph->SetPoint( 1, 100 , 17.7 );
  graph->SetPoint( 2, 120 , 20.5 );
  graph->SetPoint( 3, 130 , 21.9 );
  graph->SetPoint( 4, 140 , 21.2 );
  graph->SetPoint( 5, 160 , 19.5 );
  graph->SetPoint( 6, 180 , 27.8 );
  graph->SetPoint( 7, 200 , 21.6 );
  graph->SetPoint( 8, 250 , 32.6 );
  graph->SetPoint( 9, 300 , 42.2 );
  graph->SetPoint(10, 350 , 35.5 );
}
