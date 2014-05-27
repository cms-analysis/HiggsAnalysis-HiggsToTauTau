import ROOT

file_in = ROOT.TFile.Open('Fisher.root','read')
file_in.cd()

names = {
'FisherWZ'		:  'WZ',
'FisherZZ'		:  'ZZ',
'Fishertt1l'		:  'tt1l',
'Fishertt2l'		:  'tt2l',
'FisherttW'		:  'ttW',
'FisherttZ'		:  'ttZ',
'FishertH_YtMinus'	:  'tH_YtMinus125',
'FisherttH'		:  'ttH',
'Fisherreducible'	:  'reducible',
'Fisherdata'		:  'data_obs',
'FishersumMC'		:  'sumMC',
        }

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

file_out = ROOT.TFile.Open('htt_th.inputs-sm-8TeV.root','recreate')
file_out.cd()
file_out.mkdir('emt')
file_out.cd('emt')
for hist in hists :
  hist.Write()

file_out.cd()
file_out.mkdir('mmt')
file_out.cd('mmt')
## dummy for the moment
for hist in hists :
  hist.Scale(0.00000001)
  hist.Write()

file_out.Close()

