import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 5.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = 20.', #this is the actual merging scale
            'JetMatching:nQmatch = 4', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
            'JetMatching:nJetMax = 2', #number of partons in born matrix element for highest multiplicity
            'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
            'pythia8CUEP8M1Settings',
            'processParameters',
            )
     )
)




from PhysicsTools.HepMCCandAlgos.genParticles_cfi import *
from RecoJets.Configuration.RecoGenJets_cff import *
from RecoJets.Configuration.GenJetParticles_cff import *

from RecoJets.JetProducers.GenJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *





selectedGenParticles = cms.EDFilter("CandPtrSelector",
 src = cms.InputTag("genParticles"),
 cut = cms.string("!(isHardProcess() && pdgId()>10 && pdgId()<17 )")
)
 

 
myJets=ak4GenJets.clone(src='selectedGenParticles')
 
 
 

leadingJets = cms.EDFilter("LargestPtCandViewSelector",
src = cms.InputTag("myJets"),
maxNumber = cms.uint32(2)
)
   
jjCandidates = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("leadingJets leadingJets"),
    cut = cms.string("mass > 200.0")
)


filterGenMjjJets = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("jjCandidates"),
    minNumber = cms.uint32(1)
)





ProductionFilterSequence = cms.Sequence(generator*genParticles*genParticlesForJets*selectedGenParticles*myJets*leadingJets*jjCandidates*filterGenMjjJets)







