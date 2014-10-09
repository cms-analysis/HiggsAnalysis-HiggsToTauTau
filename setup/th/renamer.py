import ROOT

def fill_root_file(file_in_name, category, file_out_name, option = 'recreate') :

  names = {
    'FisherWZ'            :  'WZ'           ,
    'FisherZZ'            :  'ZZ'           ,
    'Fishertt1l'          :  'tt1l'         ,
    'Fishertt2l'          :  'tt2l'         ,
    'FisherttW'           :  'ttW'          ,
    'FisherttZ'           :  'ttZ'          ,
    'FishertH_YtMinus'    :  'tH_YtMinus125',
    'FisherttH'           :  'ttH'          ,
    'Fisherreducible'     :  'reducible'    ,
    'Fisherdata'          :  'data_obs'     ,
    'FishersumMC'         :  'sumMC'        ,
#     'FishersumMC'         :  'data_obs'     , # this is just a test, as of 9/10/14 FIXME!
          }

  file_in = ROOT.TFile.Open(file_in_name,'read')
  file_in.cd()
  
  hists = []
  
  for key in file_in.GetListOfKeys() :
    hist = key.ReadObj()
    if hist.GetName() in names.keys() :
      if names[hist.GetName()] in [hh.GetName() for hh in hists] : continue
      hist.SetName(names[hist.GetName()])
      hist.SetMarkerStyle(9)
      hist.SetMarkerSize(1)
      hist.SetMarkerColor(ROOT.kBlack)
      hist.SetLineColor(ROOT.kBlack)
      hists.append(hist)
  
  file_out = ROOT.TFile.Open(file_out_name,option)
  file_out.cd()
  file_out.mkdir(category)
  file_out.cd(category)
  for hist in hists :
    hist.Write()
  file_out.cd()
  file_out.Close()
 
  
fill_root_file('Fisher_emt.root','emt','htt_th.inputs-sm-8TeV.root','recreate')
fill_root_file('Fisher_mmt.root','mmt','htt_th.inputs-sm-8TeV.root','update'  )
