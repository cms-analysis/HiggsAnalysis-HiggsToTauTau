from ROOT import TROOT, TFile, TString, TPad, TPaveText, TCanvas, TH1F, TLegend, TF1, gROOT, TLine, gStyle
from ROOT import kBlack, TGraphAsymmErrors, Math, Double
import math

from HttStyles import *

SIGNAL_SCALE = 1.

sep = '-'*70
wfmt = '%.4f %.2f %-60s'
nfmt = '%.2f'

''' Creates signal-over-background weighted plots
    from post-fit Inputs. Helper class for 
    sobWeightedCombineAll.py.

    Translated to Python from original C++ implementation
    by Jose Benitez and Lorenzo Bianchini.
    Functionally working version, redesign ongoing.
'''
class SOBPlotter():

    def __init__(self):
        # self.fileList = []
        HttStyle.cd()
        self.tfile = TFile('tmp.root', 'recreate')

    def openTFile(self, fileName):
        # tfile = 0
        # for f in self.fileList:
        #     if f.GetName() == fileName: 
        #         return f
        f = TFile(fileName)
        # self.fileList.append(f)
        return f


        # if fileName not in self.fileDict:
            # self.fileDict[fileName] = TFile(fileName)
        # return self.fileDict[fileName]

    def tfileGet(self, tfile, histName):
        hist = tfile.Get(histName)
        if not hist:
            msg = 'Object {histName} not found in {tfile}'.format(histName=histName, tfile=tfile)
            raise RuntimeError(msg)
        return hist

    def tfileCopy(self, tfile, histName, newName=''):
        if newName == '':
            newName = histName
        hist = self.tfileGet(tfile, histName)
        self.tfile.cd()
        histNew = TH1F(hist)
        histNew.SetName(newName)
        return histNew


    def HideBin(self, g):
        
        blist = []

        for i in range(0, g.GetN()):
            x = Double(0.)
            y = Double(0.)
            g.GetPoint(i, x, y)
 
#            print x, y
               
            if x > 100 and x < 150:
                blist.append(i)

#        print 'Remove list = ', blist
        for ip in reversed(blist):
            g.RemovePoint(ip)


    '''Returns first bin with bin content of at least frac times the maximum'''
    def findFirstBin(self, h, frac=0.1):
        maxVal = h.GetMaximum()
        bin = 0
        for iBin in range(1, h.GetNBinsX()+1):
            if h.GetBinContent(iBin) > frac * maxVal:
                bin = iBin
        return bin

    '''Create TGraphAsymmErrors from input histogram with Poisson errors'''
    def createTGraphPoisson(self, h, w=1.):
        self.tfile.cd()
        g = TGraphAsymmErrors(h)
        for i in range(0, g.GetN()):
            y = h.GetBinContent(i+1)
            binWidth = h.GetBinWidth(i+1)

            # From https://twiki.cern.ch/twiki/bin/view/CMS/PoissonErrorBars
            alpha = 1. - 0.6827
            n = int(round(y*binWidth/w)) # Round is necessary due to, well, rounding errors
            l = Math.gamma_quantile(alpha/2., n, 1.) if n != 0. else 0.
            u = Math.gamma_quantile_c(alpha, n+1, 1)
            # print y*binWidth/w, n, y, u, l
            g.SetPointEYlow(i, (n-l)/binWidth*w)
            g.SetPointEYhigh(i, (u-n)/binWidth*w)

        return g


    '''Add input histogram to graph with Poisson errors. Errors added quadratically'''
    def addHistToTGraphPoisson(self, h, g, w=1.):
        for i in range(0, g.GetN()):
            # shifted by +1, i.e. over/underflow
            err = h.GetBinError(i+1)
            y = h.GetBinContent(i+1)

            binWidth = h.GetBinWidth(i+1)
            
            # From https://twiki.cern.ch/twiki/bin/view/CMS/PoissonErrorBars
            alpha = 1. - 0.6827
            n = int(round(y*binWidth/w)) # Round is necessary due to, well, rounding errors
            l = Math.gamma_quantile(alpha/2., n, 1.) if n != 0. else 0.
            u = Math.gamma_quantile_c(alpha, n+1, 1) if n != 0. else 0.
            g.SetPointEYlow(i, math.sqrt(((n-l)/binWidth*w)**2 + g.GetErrorYlow(i)**2))
            g.SetPointEYhigh(i, math.sqrt(((u-n)/binWidth*w)**2 + g.GetErrorYhigh(i)**2))

            gx = Double(0.)
            gy = Double(0.)
            g.GetPoint(i, gx, gy)
            g.SetPoint(i, gx, y + gy)


    '''Scale the histogram in bbb way, given the weighting list'''
    def HistScaling(self, h, wlist):

        if h.GetXaxis().GetNbins() != len(wlist):
            print '!!! Not the same # of bins !!!', h.GetXaxis().GetNbins(), len(wlist)
            
        for ibin in range(1, h.GetXaxis().GetNbins()+1):
            val = h.GetBinContent(ibin)*wlist[ibin-1]
            err = h.GetBinError(ibin)*wlist[ibin-1]
            h.SetBinContent(ibin, val)
            h.SetBinError(ibin, err)


    '''Returns first bin with bin content of at least frac times the maximum'''
    def findLastBin(self, h, frac=0.1):
        maxVal = h.GetMaximum()
        bin = 0
        for iBin in reversed(range(1, h.GetNBinsX()+1)):
            if h.GetBinContent(iBin) > frac * maxVal:
                bin = iBin
        return bin

    ''' Returns clone of the passed histogram with bin contents zeroed out'''
    def getErrorBand(self, hist):
        
        h = TH1F(hist)
        hist.SetName(hist.GetName() + 'herrorBand')
        # Zero out bin content, including under+overflow
        for iBin in range(0, h.GetNbinsX()+2):
            h.SetBinContent(iBin, 0.)
        # Zero out under/overflow bin errors
        h.SetBinError(0, 0.)
        h.SetBinError(h.GetNbinsX()+1, 0.)
        return h

    ''' Finds central 68% region in signal histogram and calculates purity for that'''
    def getSoB(self, hsplusb, hbkg):
        
        hs = TH1F(hsplusb)
        hs.SetName('HS')
        hb = TH1F(hbkg)
        hb.SetName('HB')
        hs.Add(hb, -1.)
        hs.Scale(SIGNAL_SCALE)

        print 'Integrals signal, background', hs.Integral(), hb.Integral()

        sigString = ''
        bkgString = ''
        errString = ''

        xmin = hs.GetXaxis().GetXmin()
        xmax = hs.GetXaxis().GetXmax()

        # This seems overly complicated
        for iBin in range(1, hs.GetNbinsX()+1):

            template = '{binContent:.6f}*({binXmin}<x&&x<{binXmax})'
            sigString += template.format(binContent=hs.GetBinContent(iBin), binXmin=hs.GetBinLowEdge(iBin), binXmax=hs.GetBinLowEdge(iBin)+hs.GetBinWidth(iBin))
            bkgString += template.format(binContent=hb.GetBinContent(iBin), binXmin=hb.GetBinLowEdge(iBin), binXmax=hb.GetBinLowEdge(iBin)+hb.GetBinWidth(iBin))
            errString += template.format(binContent=hb.GetBinError(iBin), binXmin=hb.GetBinLowEdge(iBin), binXmax=hb.GetBinLowEdge(iBin)+hb.GetBinWidth(iBin))


            if iBin < hs.GetNbinsX():
                sigString += '+'
                bkgString += '+'
                errString += '+'

        fSig = TF1('fsig', sigString, xmin, xmax)
        fBkg = TF1('fbkg', bkgString, xmin, xmax)
        fErr = TF1('fErr', errString, xmin, xmax)

        npoints = 10000.
        total = fSig.Integral(xmin, xmax)
        dx = (xmax - xmin)/npoints
        xlow = xmin
        xhigh = xmax
        lowInt = 0.
        highInt = 0.
        # This finds the x value borders in which 68% of the
        # are contained. These may lie anywhere within a bin
        for i in range(1, int(npoints)+1):
            xl = xmin + float(i) * dx
            lowInt += fSig.Eval(xl) * dx
            if lowInt < total * 0.158:
                xlow = xl
            xh = xmax - float(i)*dx
            highInt += fSig.Eval(xh) * dx
            if highInt < total * 0.158:
                xhigh = xh

        sig = fSig.Integral(xlow, xhigh)
        bkg = fBkg.Integral(xlow, xhigh)

        bkgErr = 0
        xlow_bin = hb.FindBin(xlow)
        xhigh_bin = hb.FindBin(xhigh)

        for ibin in range(xlow_bin, xhigh_bin):
            bkgErr += hb.GetBinError(ibin)*hb.GetBinError(ibin)

#        bkg2 = hb.IntegralAndError(xlow, xhigh, bkgErr)
#        bkgString += template.format(binContent=hb.GetBinContent(iBin), binXmin=, binXmax=hb.GetBinLowEdge(iBin)+hb.GetBinWidth(iBin))
#        print 'yuta :', xlow, xhigh, xlow_bin, xhigh_bin, bkg, '+/-', math.sqrt(bkgErr)





        print 'Integrals signal, background, around peak', sig, bkg
        
#        return sig/math.sqrt(sig + bkg + bkgErr), sig*sig/bkg

        return sig/bkg, sig*(sig/bkg)

#        return sig/(sig+bkg)

        # Can introdduce other measures here:
        # sig/sqrt(sig+bkg)
        # sig/sqrt(bkgerr*bkgerr + sig + bkg)





    # This scans through all files, gets the width of 
    # the first bin for each 'ggH' histogram, and
    # sets the rebin flag to true for the hists
    # that have a smaller width
    def findRebin(self, fileNames, rebinDict, sampleName='ggH'):
        binW = 0.
        for fileName in fileNames:
            f = self.openTFile(fileName+'.root')
            ggH = self.tfileGet(f, sampleName)
            if ggH.GetBinWidth(1) > binW:
                binW = ggH.GetBinWidth(1)

        print 'Maximum bin 1 bin width', binW

        for fileName in fileNames:
            f = self.openTFile(fileName+'.root')
            ggH = self.tfileGet(f, sampleName)
            if ggH.GetBinWidth(1) != binW:
                rebinDict[fileName] = 1
            else:
                rebinDict[fileName] = 0


    def getSOBWeights(self, fileNames, isSM):
        weights = {}
        Nsig = {}
        weightSum = 0.
        NsigSum = 0.
        for fileName in fileNames:
            inFile = self.openTFile(fileName+'.root')

            ggH = self.tfileCopy(inFile, 'ggH')

            if fileName.find('emu') != -1 and isSM:
                Ztt = self.tfileCopy(inFile, 'ggH_hww')
            else:
                Ztt = self.tfileCopy(inFile, 'Ztt')

            weights[fileName], Nsig[fileName] = self.getSoB(ggH, Ztt)
            weightSum += weights[fileName]
            NsigSum += Nsig[fileName]

        if weightSum <= 0.:
            print 'ERROR: sum of S/B weights is bad, returning'
            return
        for fileName in fileNames:

            weights[fileName] = weights[fileName]/weightSum
            Nsig[fileName] = Nsig[fileName]/NsigSum
            
#            weights[fileName] = weights[fileName]

        maxW = 0.

        print
        print sep
        print 'Weight', 'Signal cont.', 'category'
        print sep
        TotalWeight = 0
        TotalNsig = 0
        for k, v in sorted(weights.items(), key=lambda x:x[1], reverse=True):
            print wfmt % (v, Nsig[k], k.replace('postfit_','').replace('_LIN','').replace('_LOG',''))
            TotalWeight += v
            TotalNsig += Nsig[k]
        print sep
        print TotalWeight, TotalNsig
        print sep
        print

        
        for fileName in fileNames:
            if weights[fileName] > maxW:
                maxW = weights[fileName]
#            print 'Weight', weights[fileName], fileName
        print 'Maximum weight', maxW

        return weights, weightSum




    def getbbbSOBWeights(self, fileNames, isSM):
        weights = {}
        weightSum = 0.

        for fileName in fileNames:
            inFile = self.openTFile(fileName+'.root')


            ggH = self.tfileCopy(inFile, 'ggH')

            if fileName.find('emu') != -1 and isSM:
                Ztt = self.tfileCopy(inFile, 'ggH_hww')
            else:
                Ztt = self.tfileCopy(inFile, 'Ztt')

#            print 'check', fileName, ggH, Ztt

            list_sig = []
            for ibin in range(1,ggH.GetXaxis().GetNbins()+1):
                sig = ggH.GetBinContent(ibin)
                bkg = Ztt.GetBinContent(ibin)
                bkgerr = Ztt.GetBinError(ibin)

                significance=0
                sn = 0
                if not (sig==0 and bkg==0):
#                    print 'yt_check:', sig, bkg, bkgerr*bkgerr, math.sqrt(sig + bkg + bkgerr*bkgerr)
                    significance = math.fabs(sig)/math.sqrt(math.fabs(sig) + math.fabs(bkg) + bkgerr*bkgerr)
                    sn = math.fabs(sig)/math.fabs(bkg)
                    # bbb_yuta
#                    significance = math.fabs(sig)/math.fabs(bkg)


                print fileName.replace('postfit_','').replace('_LIN','').replace('_LOG',''), ': bin=', ibin, 'sig=', nfmt % (sig), 'bkg=', nfmt % (bkg), 's/n=', nfmt % (sn), 'sig=', nfmt % (significance)

                list_sig.append(significance)
                weightSum += significance
#                print fileName, ibin, significance

            weights[fileName] = list_sig

        print 'Sum of Significanec = ', weightSum

        if weightSum <= 0.:
            print 'ERROR: sum of S/B weights is bad, returning'
            return


        for fileName in fileNames:
#            print weights[fileName]
            significance_list = weights[fileName]
            new_significance_list = [0 for ii in range(len(significance_list))]

            for index in range(len(significance_list)):
                val = significance_list[index]/weightSum
                new_significance_list[index] = val

            weights[fileName] = new_significance_list
 #           print weights[fileName]

#        return weights, weightSum
        return weights




    def calculateSignalIntegrals(self, fileNames, weights, muValue, doWeight, isSM):
        signalIntegral = 0.
        weightedSignalIntegral = 0.

        for fileName in fileNames:
            tfile = self.openTFile(fileName+'.root')
            
            ggH = tfile.Get('ggH')
            if fileName.find('emu') != -1 and isSM:
                Ztt = self.tfileCopy(tfile, 'ggH_hww')
            else:
                Ztt = self.tfileCopy(tfile, 'Ztt')

            signal = TH1F(ggH)
            signal.SetName('signal')
            signal.Add(Ztt, -1.)
            signal.Scale(SIGNAL_SCALE * muValue)

            for b in range(1, signal.GetNbinsX()+1):
                signal.SetBinContent(b, signal.GetBinContent(b) * signal.GetBinWidth(b))

            signalIntegral += signal.Integral()

            if doWeight == 1:
                signal.Scale(weights[fileName])

            weightedSignalIntegral += signal.Integral()

        print 'Signal yield:', signalIntegral
        print 'Weighted signal yield:', weightedSignalIntegral
        print 'Signal yield scale factor', signalIntegral/weightedSignalIntegral

        return signalIntegral, weightedSignalIntegral




    def calculateSignalIntegralsbbb(self, fileNames, weights, muValue, doWeight, isSM):
        signalIntegral = 0.
        weightedSignalIntegral = 0.

        for fileName in fileNames:
            tfile = self.openTFile(fileName+'.root')
            
            ggH = tfile.Get('ggH')
            if fileName.find('emu') != -1 and isSM:
                Ztt = self.tfileCopy(tfile, 'ggH_hww')
            else:
                Ztt = self.tfileCopy(tfile, 'Ztt')

            signal = TH1F(ggH)
            signal.SetName('signal')
            signal.Add(Ztt, -1.)
            signal.Scale(SIGNAL_SCALE * muValue)

            for b in range(1, signal.GetNbinsX()+1):
                signal.SetBinContent(b, signal.GetBinContent(b) * signal.GetBinWidth(b))

            signalIntegral += signal.Integral()

            if doWeight == 1:

                if signal.GetXaxis().GetNbins() != len(weights[fileName]):
                    print 'Not the same contents !'

                weight_list = weights[fileName]                

                self.HistScaling(signal, weight_list)
#                for ibin in range(1, signal.GetXaxis().GetNbins()+1):
#                    val = signal.GetBinContent(ibin)*weight_list[ibin-1]
#                    err = signal.GetBinError(ibin)*weight_list[ibin-1]
#                    signal.SetBinContent(ibin, val)#Scale(weights[fileName])
#                    signal.SetBinError(ibin, err)#Scale(weights[fileName])
#                    print ibin, weight_list[ibin-1], val, err

            weightedSignalIntegral += signal.Integral()

        print 'Signal yield:', signalIntegral
        print 'Weighted signal yield:', weightedSignalIntegral
        print 'Signal yield scale factor', signalIntegral/weightedSignalIntegral

        return signalIntegral, weightedSignalIntegral





    def sobWeightedCombine(self, fileNames, outName, doWeight=1, muValue=1.):
        print 'WARNING: using fitted mu value', muValue, 'make sure it\'s up to date'
        isSM = outName.find('SM') != -1

        rebinDict = {}
        self.findRebin(fileNames, rebinDict)

        weights, weightSum = self.getSOBWeights(fileNames, isSM)

        signalIntegral, weightedSignalIntegral = self.calculateSignalIntegrals(fileNames, weights, muValue, doWeight, isSM)

        for fileName in fileNames:
            weights[fileName] *= signalIntegral/weightedSignalIntegral

        
        samples = ['ggH', 'Ztt', 'signal', 'data_obs', 'ttbar', 'EWK', 'Fakes']

        fN0 = fileNames[0]
#        print 'Yuta1', fN0
        if fN0.find('emu') != -1 and isSM:
            samples.append('ggH_hww')
        if fN0.find('eleTau') != -1 and isSM:
            samples.append('Zee')

        file1 = self.openTFile(fN0+'.root')
        
        histDict = {}
        dataGraph = 0
        # Use first file clones as base histograms

        for sample in samples:
            if sample == 'signal':
                histDict[sample] = self.tfileCopy(file1, 'ggH', sample)
            else:
                histDict[sample] = self.tfileCopy(file1, sample)
            if doWeight == 1:
                histDict[sample].Scale(weights[fN0])
            if rebinDict[fN0]:
                histDict[sample].Rebin(2)
            if sample == 'signal':
                histDict[sample].Add(histDict['Ztt'], -1.)
                histDict[sample].Scale(SIGNAL_SCALE)
            if sample == 'data_obs':
                dataGraph = self.createTGraphPoisson(histDict[sample], weights[fN0])


        for fileName in fileNames:
            if fileName == fileNames[0]: continue
            file2 = self.openTFile(fileName+'.root')
            
            localHistDict = {}

            for sample in samples:
                if fileName.find('emu') == -1 and sample == 'ggH_hww':
                    continue
                # if fileName.find('emu') != -1 and isSM and sample == 'Ztt':
                #     localHistDict[sample] = self.tfileCopy(file2, 'ggH_hww', sample+fileName)
                if sample == 'signal':
                    localHistDict[sample] = self.tfileCopy(file2, 'ggH', sample+fileName)
                else:
                    localHistDict[sample] = self.tfileCopy(file2, sample, sample+fileName)
                if doWeight == 1:
                    localHistDict[sample].Scale(weights[fileName])
                if rebinDict[fileName]:
                    localHistDict[sample].Rebin(2)
                if sample == 'signal':
                    localHistDict[sample].Add(localHistDict['Ztt'], -1.)
                    localHistDict[sample].Scale(SIGNAL_SCALE)
                if sample == 'data_obs':
                    print 'ADDING', fileName, sample
                    self.addHistToTGraphPoisson(localHistDict[sample], dataGraph, weights[fileName])
                #                print 'Add here ... ', sample, histDict[sample], localHistDict[sample]
                histDict[sample].Add(localHistDict[sample])
                if fileName.find('emu') == -1 and 'ggH_hww' in histDict and sample == 'Ztt':
                    histDict['ggH_hww'].Add(localHistDict[sample])


        fullOutName = 'Plot_' + outName + '.root'
        outFile = TFile(fullOutName, 'RECREATE')
        for hist in histDict.values():
            hist.Write()

        dataGraph.Write()

        outFile.ls()
        outFile.Close()


    def sobInputs(self, fileNames, outName, muValue=1.):
        print 'WARNING: using fitted mu value', muValue, 'make sure it\'s up to date'
        isSM = outName.find('SM') != -1
        

        fN0 = fileNames[0]
        isEMSM = fN0.find('emu_') != -1 and isSM
        isETSM = fN0.find('eleTau_') != -1 and isSM
        
        samples = ['ggH', 'Ztt', 'signal', 'data_obs', 'ttbar', 'EWK', 'Fakes']
        if isEMSM:
            samples.append('ggH_hww')
        if isETSM:
            samples.append('Zee')

        file1 = self.openTFile(fN0+'.root')

        histDict = {}
        
        NBINS = 20
        XMIN = 0.
        XMAX = 0.7

        # First loop: copy original histograms to get style
        for sample in samples:
            if sample == 'signal':
                histDict[sample] = self.tfileCopy(file1, 'ggH', sample)
            else:
                histDict[sample] = self.tfileCopy(file1, sample)

            h = histDict[sample]
            h.Reset()
            h.SetBins(NBINS, XMIN, XMAX)
            
        file1.Close()

        # Second loop: Over all files, fill S/B-histos
        for fileName in fileNames:
            file2 = self.openTFile(fileName+'.root')
            
            localHistDict = {}
            for sample in samples:
                if not isEMSM and sample == 'ggH_hww':
                    continue
                if not isETSM and sample == 'Zee':
                    continue
                if sample == 'signal':
                    localHistDict[sample] = self.tfileCopy(file2, 'ggH', sample+fileName)
                else:
                    localHistDict[sample] = self.tfileCopy(file2, sample, sample+fileName)
                if sample == 'signal':
                    localHistDict[sample].Add(localHistDict['Ztt'], -1.)
                    localHistDict[sample].Scale(SIGNAL_SCALE)
                if fileName.find('emu') == -1 and 'ggH_hww' in histDict and sample == 'Ztt':
                    histDict['ggH_hww'].Add(localHistDict[sample])

            tmpSignal = localHistDict['signal']
            tmpBG = localHistDict['Ztt'] if not isEMSM and not '' else localHistDict['ggH_hww']

            for iBin in range(1, tmpSignal.GetNbinsX()+2):
                # Determine bin to fill

                sob = tmpSignal.GetBinContent(iBin)/(tmpBG.GetBinContent(iBin) + tmpSignal.GetBinContent(iBin)) if tmpSignal.GetBinContent(iBin) > 0. else -1.


                # Fill bin
                for sample in samples:
                    if not isEMSM and sample == 'ggH_hww':
                        continue
                    if sample not in histDict:
                        print sample, fileName
                    hSOB = histDict[sample]
                    hMass = localHistDict[sample]
                    bin = hSOB.FindBin(sob)
                    massContent = hMass.GetBinContent(iBin) * hMass.GetBinWidth(iBin)
                    hSOB.SetBinContent(bin, hSOB.GetBinContent(bin) + massContent)
                    err2 = hSOB.GetBinError(bin)**2
                    errm2 = (hMass.GetBinError(iBin) * hMass.GetBinWidth(iBin))**2
                    hSOB.SetBinError(bin, math.sqrt(err2 + errm2))
            for sample in samples:
                if not isEMSM and sample == 'ggH_hww':
                    continue
                print sample, localHistDict[sample].Integral(), histDict[sample].Integral()
                histDict[sample].SetBinContent(NBINS, histDict[sample].GetBinContent(NBINS) + histDict[sample].GetBinContent(NBINS+1))
                histDict[sample].SetBinError(NBINS, math.sqrt(histDict[sample].GetBinError(NBINS)**2 + histDict[sample].GetBinContent(NBINS+1)**2))

        dataGraph = self.createTGraphPoisson(histDict['data_obs'])

        fullOutName = 'Plot_' + outName + '.root'
        outFile = TFile(fullOutName, 'RECREATE')
        for hist in histDict.values():
            hist.Write()

        dataGraph.Write()

        outFile.ls()
        outFile.Close()



####################### YUTA added
    def bbbsobWeightedCombine(self, fileNames, outName, doWeight=1, muValue=1.):
        
        print 'WARNING: using fitted mu value', muValue, 'make sure it\'s up to date'
        isSM = outName.find('SM') != -1

        rebinDict = {}
        self.findRebin(fileNames, rebinDict)

#        weights, weightSum = self.getbbbSOBWeights(fileNames, isSM)
        weights = self.getbbbSOBWeights(fileNames, isSM)

        signalIntegral, weightedSignalIntegral = self.calculateSignalIntegralsbbb(fileNames, weights, muValue, doWeight, isSM)


        for fileName in fileNames:
#            print 'before weight', weights[fileName]
            wlist = weights[fileName]
            for index in range(len(wlist)):
#                print '\t beore',index, wlist[index]
                wlist[index] *= signalIntegral/weightedSignalIntegral
#                print '\t after',index, wlist[index]

            weights[fileName] = wlist
#            print 'after weight', weights[fileName]
            
        samples = ['ggH', 'Ztt', 'signal', 'data_obs', 'ttbar', 'EWK', 'Fakes']

        fN0 = fileNames[0]

        if fN0.find('emu') != -1 and isSM:
            samples.append('ggH_hww')
        if fN0.find('eleTau') != -1 and isSM:
            samples.append('Zee')

        file1 = self.openTFile(fN0+'.root')
#        print file1
        
        histDict = {}
        # Use first file clones as base histograms

        for sample in samples:
            if sample == 'signal':
                histDict[sample] = self.tfileCopy(file1, 'ggH', sample)
            else:
                histDict[sample] = self.tfileCopy(file1, sample)
            if doWeight == 1:
                self.HistScaling(histDict[sample], weights[fN0])


            if rebinDict[fN0]:
                histDict[sample].Rebin(2)
            if sample == 'signal':
                histDict[sample].Add(histDict['Ztt'], -1.)
                histDict[sample].Scale(SIGNAL_SCALE)

        for fileName in fileNames:
            if fileName == fileNames[0]: continue
            file2 = self.openTFile(fileName+'.root')
            
            localHistDict = {}

            for sample in samples:
                if fileName.find('emu') == -1 and sample == 'ggH_hww':
                    continue
                if sample == 'signal':
                    localHistDict[sample] = self.tfileCopy(file2, 'ggH', sample+fileName)
                else:
                    localHistDict[sample] = self.tfileCopy(file2, sample, sample+fileName)

                self.HistScaling(localHistDict[sample], weights[fileName])
#                localHistDict[sample].Scale(weights[fileName])

                if rebinDict[fileName]:
                    localHistDict[sample].Rebin(2)
                if sample == 'signal':
                    localHistDict[sample].Add(localHistDict['Ztt'], -1.)
                    localHistDict[sample].Scale(SIGNAL_SCALE)
                histDict[sample].Add(localHistDict[sample])
                if fileName.find('emu') == -1 and 'ggH_hww' in histDict and sample == 'Ztt':
                    histDict['ggH_hww'].Add(localHistDict[sample])

        fullOutName = 'Plot_' + outName + '.root'
        outFile = TFile(fullOutName, 'RECREATE')
        for hist in histDict.values():
            hist.Write()

        outFile.ls()
        outFile.Close()




    @staticmethod
    def CMSPrelim(c, dataset, channel, cat):
        
        lowX = 0.16
        lowY = 0.835
        color = 1
        font = 62

        c.cmsprel = TPaveText(lowX-0.03, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
        c.cmsprel.SetBorderSize(   0 )
        c.cmsprel.SetFillStyle(    0 )
        c.cmsprel.SetTextAlign(   12 )
        c.cmsprel.SetTextColor( color )
        c.cmsprel.SetTextFont ( font )
        #cmsprel.SetTextSize ( 0.035 )
        #cmsprel.SetTextSize ( 0.027 )
        c.cmsprel.SetTextSize ( 0.030 )
        c.cmsprel.AddText(dataset)
        c.cmsprel.Draw()

#        print 'dataset, channel, cat -> ', dataset, channel, cat
        c.chan = TPaveText(lowX+0.05, lowY-0.002, lowX+0.45, lowY+0.028, "NDC")
        c.chan.SetBorderSize(   0 )
        c.chan.SetFillStyle(    0 )
        c.chan.SetTextAlign(   12 )
        c.chan.SetTextSize ( 0.035 )
        c.chan.SetTextColor( color )
        c.chan.SetTextFont ( font )
        c.chan.AddText(channel)
        c.chan.Draw()

        c.category = TPaveText(lowX+0.05, lowY-0.002-0.06, lowX+0.45, lowY+0.028-0.06, "NDC")
        c.category.SetBorderSize(   0 )
        c.category.SetFillStyle(    0 )
        c.category.SetTextAlign(   12 )
        c.category.SetTextSize ( 0.035 )
        c.category.SetTextColor( color )
        c.category.SetTextFont ( font )
        c.category.AddText(cat)
        c.category.Draw()

    def diffGraph(self, g, h, opt):
        gdiff = TGraphAsymmErrors(g)
        gdiff.SetName(g.GetName() + h.GetName() + '_diff')

        for i in range(0, gdiff.GetN()):
            x = Double(0.)
            y = Double(0.)
            g.GetPoint(i, x, y)
            gdiff.SetPoint(i, x, y - h.GetBinContent(i+1))

            
            if opt == 1: # keep bin errors
                pass
            elif opt == 2:
                gdiff.SetPointEYhigh(i, math.sqrt(g.GetErrorYhigh(i)**2 + h.GetBinError(i+1)**2))

        return gdiff

    def diffPlot(self, h1, h2, opt):
        h = TH1F(h1)
        h.SetName(h1.GetName() + h2.GetName() + '_diff')
        for b in range(1, h.GetNbinsX()+1):
            h.SetBinContent(b, h1.GetBinContent(b) - h2.GetBinContent(b))
            h.SetBinError(b, 0.)
            if opt == 1:
                h.SetBinError(b, h1.GetBinError(b))
            elif opt == 2:
                h.SetBinError(b, math.sqrt(h1.GetBinError(b)*h1.GetBinError(b) + h2.GetBinError(b)*h2.GetBinError(b)))

        h.SetBinContent(0, 0.)
        h.SetBinError(0, 0.)
        h.SetBinContent(h.GetNbinsX()+1, 0.)
        h.SetBinError(h.GetNbinsX()+1, 0.)

        return h
    
    @staticmethod
    def findMaxY(h, blind, opt=0, lowx=-1., highx=-1.):
        if lowx == -1.:
            lowx = h.GetXaxis().GetXmin()
        if highx == -1.:
            highx = h.GetXaxis().GetXmax()

        maxVal = 0.
        for b in range(1, h.GetNbinsX()+1):

            if blind==False:
                xval = h.GetXaxis().GetBinCenter(b)
                if xval > 100 and xval < 150:
#                    print 'Remove',b
                    continue

            if h.GetBinContent(b) > 0. and lowx < h.GetBinCenter(b) and h.GetBinCenter(b) < highx:
                if opt == 0:
                    if h.GetBinContent(b) + h.GetBinError(b) > maxVal:
                        maxVal = h.GetBinContent(b) + h.GetBinError(b)
                elif opt == 1:
                    if h.GetBinContent(b) > maxVal:
                        maxVal = h.GetBinContent(b)

#            print 'max, chek point = ', b, maxVal

#        print 'Final value = ', maxVal

        if maxVal==0:
            maxVal = 0.1

        return maxVal


    def findMinY(self, h, blind, opt=0, lowx=-1., highx=-1.):
        if lowx == -1.:
            lowx = h.GetXaxis().GetXmin()
        if highx == -1.:
            highx = h.GetXaxis().GetXmax()

        maxVal = 0.

        for b in range(1, h.GetNbinsX()+1):

            if blind==False:
                xval = h.GetXaxis().GetBinCenter(b)
                if xval > 100 and xval < 150:
#                    print 'Remove',b
                    continue
                

            if h.GetBinContent(b) < 0. and lowx < h.GetBinCenter(b) and h.GetBinCenter(b) < highx:
                if opt == 0:
                    if -h.GetBinContent(b) + h.GetBinError(b) > maxVal:
                        maxVal = -h.GetBinContent(b) + h.GetBinError(b)
                elif opt == 1:
                    if -h.GetBinContent(b) > maxVal:
                        maxVal = -h.GetBinContent(b)

#            print 'max, chek point = ', b, maxVal

#        print 'Final value = ', maxVal
        return maxVal



    def sobWeightedPlot(self, fileName, datasetName, channel, cat, log, mass, tanb, blind, sob=False):

#        print 'yuta', channel, cat
        
        c = TCanvas(fileName, '', 600, 600)
        c.cd()
        if log: c.SetLogy(1)

        f = self.openTFile('Plot_'+fileName+'.root')

        isEMSM = fileName.find('SM') != -1 and fileName.find('em') != -1
        isETSM = fileName.find('SM') != -1 and fileName.find('et') != -1

        samples = ['ggH', 'Ztt', 'signal', 'data_obs', 'ttbar', 'EWK', 'Fakes']

        if isEMSM:
            samples.append('ggH_hww')
        if isETSM:
            samples.append('Zee')

        dataGraph = self.tfileGet(f, 'Graph_from_data_obs')

        histDict = {}
        for sample in samples:
            histDict[sample] = self.tfileGet(f, sample)
#            print 'check :', sample, histDict[sample].GetSumOfWeights()
            if not histDict[sample]:
                print 'Missing histogram', sample, 'in file', 'Plot_'+fileName+'.root'

# original for plots
        xminInset = 60 # 0
        xmaxInset = 179 # 340 (for full range)

# all range
#        xminInset = 0 # 0
#        xmaxInset = 350 # 340 (for full range)

#        xminInset = 40 # 0
#        xmaxInset = 200 # 340 (for full range)
#        xminInset = 120 # 0
#        xmaxInset = 251 # 340 (for full range)

        if tanb > 0:
            xminInset = mass - 100
            xmaxInset = mass + 100

        if sob:
            xminInset = 0.4
            xmaxInset = 0.7

        ztt = histDict['Ztt']
        ggH = histDict['ggH']
        data = histDict['data_obs']

        # This is to fix a weird plotting bug
        if sob:
            new_data = TH1F('new_data', '', ggH.GetNbinsX(), 0., 0.7)
            for i in range(1, new_data.GetNbinsX()+1):
                new_data.SetBinContent(i, data.GetBinContent(i))
                # print data.GetBinContent(i)
            data = new_data

        ggH_hww = 0
        zee = 0

        signal = histDict['signal']
        if isEMSM:
            ggH_hww = histDict['ggH_hww']
        if isETSM:
            print 'retrieve Zee'
            zee = histDict['Zee']
        tt = histDict['ttbar']
        ewk = histDict['EWK']
        fakes = histDict['Fakes']

        ztt.GetYaxis().SetRangeUser(0., 1.3*self.findMaxY(data, 0))
        if log: 
            ztt.GetYaxis().SetRangeUser(0.001, 50.*self.findMaxY(data, 0))

        ztt.GetXaxis().SetTitle('#bf{m_{#tau#tau}  [GeV]}')
        ztt.GetYaxis().SetTitle('#bf{S/B Weighted dN/dm_{#tau#tau} [1/GeV]}')
        if tanb > 0. and not log:
            ztt.GetXaxis().SetRangeUser(0., mass+200.)

        if sob:
            ztt.GetXaxis().SetTitle('S/(S+B)')
            ztt.GetYaxis().SetTitle('Events')

        ztt.SetTitleOffset(1.3, 'Y')
        ztt.SetTitleOffset(1., 'X')
        ztt.GetYaxis().SetNdivisions(505)
        ztt.SetNdivisions(505)

        for b in range(0, signal.GetNbinsX()+2):
            if signal.GetBinCenter(b) < xminInset or xmaxInset < signal.GetBinCenter(b):
                signal.SetBinContent(b, 0.)
                signal.SetBinError(b, 0.)

        signal.SetName('sig')
        signal.SetFillStyle(3353) # 1001=solid , 3004,3005=diagonal
        signal.SetFillColor(2)
        signal.SetLineColor(2)
        signal.SetLineStyle(1)
        signal.SetLineWidth(0)

        ggH.SetBinContent(0,0) # remove red line on top of y axis in plot
        ggH.SetBinContent(ggH.GetNbinsX()+1,0)
        ggH.SetBinError(0,0)
        ggH.SetBinError(ggH.GetNbinsX()+1,0)
        ggH.SetName('ggH')
        ggH.SetFillStyle(3353) # 1001=solid , 3004,3005=diagonal
        ggH.SetFillColor(2)
        ggH.SetLineColor(2)
        ggH.SetLineStyle(1)
        ggH.SetLineWidth(0)

        
        if isEMSM:
            errorBand = TH1F(ggH_hww)
        else:
            errorBand = TH1F(ztt)
        errorBand.SetName("errorBand")

        errorBand.SetMarkerSize(0)
        errorBand.SetFillColor(1)
        errorBand.SetFillStyle(3013)
        errorBand.SetLineWidth(1)

        legend = TLegend()
        mssmLabel = ''
        if tanb > 0:
            mssmLabel = "tan#beta={tanb}".format(tanb=tanb)
        higgsLabel = "H(125 GeV)#rightarrow#tau#tau"
        if tanb > 0:
            higgsLabel="H(125 GeV)#rightarrow#tau#tau"

        legend.SetFillStyle(0)
        legend.SetFillColor(0)
        legend.SetBorderSize(0)
        legend.AddEntry(ggH,higgsLabel,"F")
        if tanb>0: 
            legend.AddEntry(TObject(0), mssmLabel, "")
        legend.AddEntry(data,"observed", "LP")
        if isEMSM:
            legend.AddEntry(ggH_hww, "H(125 GeV)#rightarrowWW", "F")
        legend.AddEntry(ztt, "Z#rightarrow#tau#tau","F")
        legend.AddEntry(tt, "t#bar{t}","F")
        if isETSM:
            legend.AddEntry(zee, "Z#rightarrowee", "F")
        legend.AddEntry(ewk, "electroweak","F")
        legend.AddEntry(fakes, "QCD","F")

        legend.SetX1NDC(0.63)
        legend.SetX2NDC(1.05)
        legend.SetY1NDC(0.25)
        legend.SetY2NDC(0.46)
        if log:
            legend.SetX1NDC(0.18)
            legend.SetX2NDC(0.60)
            legend.SetY1NDC(0.17)
            legend.SetY2NDC(0.38)
        
        legend.SetTextSize(.028)
        legend.SetTextAlign(12)

        if isEMSM:
            dataDiff = self.diffPlot(data, ggH_hww, 1)
            dataDiffGraph = self.diffGraph(dataGraph, ggH_hww, 1)
            errBand=self.getErrorBand(ggH_hww)
        else:
            dataDiff = self.diffPlot(data, ztt, 1)
            dataDiffGraph = self.diffGraph(dataGraph, ztt, 1)
            errBand=self.getErrorBand(ztt)


        errBand.SetFillStyle(3013) # 1001=solid , 3004,3005=diagonal, 3013=hatched official for H.tau tau
        errBand.SetFillColor(1)
        errBand.SetLineStyle(1)
        errBand.SetLineColor(1)
        errBand.SetLineWidth(1)

        errBandFrame = TH1F('errBandFrame', '', int((xmaxInset-xminInset)/dataDiff.GetBinWidth(1)),xminInset,xmaxInset)
        

        errBandFrame.GetYaxis().SetTitle("")
        errBandFrame.GetYaxis().SetRangeUser(-1.1*self.findMinY(dataDiff,blind,0,xminInset,xmaxInset),2.0*self.findMaxY(dataDiff,blind,0,xminInset,xmaxInset))
#        errBandFrame.GetYaxis().SetRangeUser(-1.*self.findMinY(dataDiff,blind,0,xminInset,xmaxInset),1.1*self.findMaxY(dataDiff,blind,0,xminInset,xmaxInset)) # good !
#        errBandFrame.GetYaxis().SetRangeUser(-0.2*self.findMinY(dataDiff,blind,0,xminInset,xmaxInset),0.5*self.findMaxY(dataDiff,blind,0,xminInset,xmaxInset))

        print 'Yuta', channel, cat
        if (channel=='e#tau_{h}' and cat=='vbf') or (channel=='e#tau_{h}' and cat==''):
            print 'enter'
            errBandFrame.GetYaxis().SetRangeUser(-2.*self.findMinY(dataDiff,blind,0,xminInset,xmaxInset),2.0*self.findMaxY(dataDiff,blind,0,xminInset,xmaxInset))
        errBandFrame.GetYaxis().SetNdivisions(5)
        errBandFrame.GetYaxis().SetLabelSize(0.06)
        errBandFrame.GetXaxis().SetTitle("#bf{m_{#tau#tau} [GeV]}    ")
        errBandFrame.GetXaxis().SetTitleColor(kBlack)
        errBandFrame.GetXaxis().SetTitleSize(0.07)
        errBandFrame.GetXaxis().SetTitleOffset(0.85)
        errBandFrame.GetXaxis().SetLabelSize(0.06)
        errBandFrame.GetXaxis().SetNdivisions(506)
#        errBandFrame.SetNdivisions(505)

        legendDiff = TLegend()
        legendDiff.SetFillStyle(0)
        legendDiff.SetFillColor(0)
        legendDiff.SetBorderSize(0)
        legendDiff.AddEntry(signal,higgsLabel,"F")

        if tanb>0:
            legendDiff.AddEntry(TObject(0), mssmLabel, '') # That might not work in python
#        legendDiff.AddEntry(dataDiff,"Data - Background","LP")
        legendDiff.AddEntry(dataDiffGraph,"Data - Background","LEP")
        legendDiff.AddEntry(errBand,"Bkg. Uncertainty","F")
        legendDiff.SetX1NDC(0.45)
        legendDiff.SetX2NDC(0.88)
        legendDiff.SetY1NDC(0.67)
        legendDiff.SetY2NDC(0.88)
        if dataDiff.GetBinContent(dataDiff.FindBin(mass)) < 0.:
            legendDiff.SetX1NDC(0.45)
            legendDiff.SetX2NDC(0.88)
            legendDiff.SetY1NDC(0.24)
            legendDiff.SetY2NDC(0.45)

        legendDiff.SetTextSize(.045)
        legendDiff.SetTextAlign(12)

        padBack = TPad("padBack","padBack",0.57,0.58,0.975,0.956) # TPad must be created after TCanvas otherwise ROOT crashes
        padBack.SetFillColor(0)
        pad = TPad("diff","diff",0.45,0.5,0.9765,0.957) # TPad must be created after TCanvas otherwise ROOT crashes
        pad.cd()
        pad.SetFillColor(0)
        pad.SetFillStyle(0)
        errBandFrame.Draw()
        errBand.Draw("e2lsame")
        signal.Draw("histsame")
        line = TLine()
        line.DrawLine(xminInset, 0, xmaxInset, 0)
        # dataDiff.Draw("pe same")

        if blind==False:
            self.HideBin(dataDiffGraph)

        dataDiffGraph.SetMarkerSize(0.5)
        dataDiffGraph.Draw('pe same')

        for ibin in range(0, dataDiffGraph.GetN()):
            x = Double(0.)
            y = Double(0.)
            dataDiffGraph.GetPoint(ibin, x, y)
            
            print 'Yuta_bin=',ibin, 'x=',x, 'y=',y, dataDiffGraph.GetErrorYhigh(ibin), dataDiffGraph.GetErrorYlow(ibin)
            print 'Yuta_error=', ibin, errBand.GetXaxis().GetBinCenter(ibin+1), errBand.GetBinError(ibin+1)

        legendDiff.Draw()
        pad.RedrawAxis()

        c.cd()
        ztt.Draw("hist")
        ggH.Draw("hist same")
        if isEMSM:
            ggH_hww.Draw("hist same")
        ztt.Draw("hist same")
        errorBand.Draw("e2 same")
        tt.Draw("hist same")
        if isETSM:
            zee.Draw("hist same")
        ewk.Draw("hist same")
        fakes.Draw("hist same")


        # data.Draw("pe same")
        dataGraph.SetMarkerSize(1)
        dataGraph.Draw('PE same')


        if blind==False:
            self.HideBin(dataGraph)


        print '#####', data.Integral(), data.GetBinContent(1)
        legend.Draw()
        c.RedrawAxis()
        padBack.Draw() # clear the background axe
        pad.Draw()
        if log: c.SetLogy(1)
        self.CMSPrelim(c, datasetName, channel, cat)

        savepath = 'figure/Plot_'+fileName
        if cat=='':
            savepath = savepath + '.pdf'
        else:
            savepath = savepath + '_' + cat + '.pdf'

#        c.Print('figure/Plot_'+fileName+".eps")
#        c.Print('figure/Plot_'+fileName+".png")
#        c.Print('figure/Plot_'+fileName+".pdf")
        c.Print(savepath)

        c.Close()
 


def sobWeightedCombine(fileNames, outName, doWeight=1, muValue=1.):
    s = SOBPlotter()
    s.sobWeightedCombine(fileNames, outName, doWeight, muValue)

def sobWeightedPlot(fileName, datasetName, channel, cat, log, mass, tanb, sob=False):
    s = SOBPlotter()
    s.sobWeightedPlot(fileName, datasetName, channel, cat, log, mass, tanb, sob)

def sobInputs(fileNames, outName, muValue=1.):
    s = SOBPlotter()
    s.sobInputs(fileNames, outName, muValue)

def bbbsobWeightedCombine(fileNames, outName, doWeight=1, muValue=1.):
    s = SOBPlotter()
    s.bbbsobWeightedCombine(fileNames, outName, doWeight, muValue)

