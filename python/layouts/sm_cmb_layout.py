import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string("Preliminary, #sqrt{s}=7 TeV, L = 4.9 fb^{-1}"),
    #dataset = cms.string("Preliminary, #sqrt{s}=7 TeV, L = 10 fb^{-1} (proj."),
    ## x-axis title
    xaxis = cms.string("m_{H} [GeV]"),
    ## x-axis title
    yaxis = cms.string("95% CL limit on #sigma/#sigma_{SM}"),
    ## mssm plot for LP11?
    mssm = cms.bool(False),
    ## print to png
    png  = cms.bool(True),
    ## print to pdf
    pdf  = cms.bool(True),
    ## print to txt
    txt  = cms.bool(True),
    ## print to root
    root = cms.bool(True),
    ## min for plotting
    min = cms.double(0.01),  ## 0.01
    ## max for plotting
    max = cms.double(1000.), ## 50
    ## min for plotting
    log = cms.int32(1),
    ## define verbosity level
    verbosity   = cms.uint32(0),
    ## define output label
    outputLabel = cms.string("cmb"), 
    ## define masspoints for limit plot
    masspoints = cms.vdouble(
    110. ,111. ,112. ,113. ,114. ,115. ,116. ,117. ,118. ,119. ,120. ,121. ,122. ,123. ,124. ,125. ,126. ,127. ,128. ,129.
   ,130. ,131. ,132. ,133. ,134. ,135. ,136. ,137. ,138. ,139. ,140. ,141. ,142. ,143. ,144. ,145. ,146. ,147. ,148. ,149.
   ,150. ,151. ,152. ,153. ,154. ,155. ,156. ,157. ,158. ,159. ,160. ,162. ,164. ,166. ,168. ,170. ,172. ,174. ,176. ,178.
   ,180. ,182. ,184. ,186. ,188. ,190. ,192. ,194. ,196. ,198. ,200. ,202. ,204. ,206. ,208. ,210. ,212. ,214. ,216. ,218.
   ,220. ,222. ,224. ,226. ,228. ,230. ,232. ,234. ,236. ,238. ,240. ,242. ,246. ,248. ,250. ,252. ,254. ,256. ,258. ,260.
   ,262. ,264. ,266. ,268. ,270. ,272. ,274. ,276. ,278. ,280. ,282. ,284. ,286. ,288. ,290. ,295. ,300. ,305. ,310. ,315.
   ,320. ,325. ,330. ,335. ,340. ,345. ,350. ,360. ,370. ,380. ,390. ,400. ,420. ,440. ,460. ,480. ,500. ,520. ,540. ,560.
   ,580. ,600.    
  ),
)
