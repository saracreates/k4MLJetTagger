#
# Copyright (c) 2020-2024 Key4hep-Project.
#
# This file is part of Key4hep.
# See https://key4hep.github.io/key4hep-doc/ for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from Gaudi.Configuration import INFO, DEBUG
from Configurables import MarlinProcessorWrapper
from Configurables import JetTagger
from Configurables import k4DataSvc
from Configurables import EventDataSvc
from Configurables import CollectionMerger
from k4FWCore import ApplicationMgr, IOSvc
from k4FWCore.parseArgs import parser

# Use source /cvmfs/sw.hsf.org/key4hep/setup.sh -r 2025-01-28 for /eos/experiment/fcc/prod/fcc/ee/test_spring2024/240gev/Hbb/CLD_o2_v05/rec/00016783/000/Hbb_rec_16783_1.root 



# parse the custom arguments
parser_group = parser.add_argument_group("createJetTags.py custom options")
parser_group.add_argument("--inputFiles", nargs="+", metavar=("file1", "file2"), help="One or multiple input files",
                        default=["/eos/experiment/fcc/prod/fcc/ee/test_spring2024/240gev/Hbb/CLD_o2_v05/rec/00016783/000/Hbb_rec_16783_99.root"])
parser_group.add_argument("--outputFile", help="Output file name", default="output_jettags.root")
parser_group.add_argument("--outputBasename", help="Output file basename (without extension)", default="output_jettags")
parser_group.add_argument("--onnx_model", help="Path to ONNX model used for tagging", default="/eos/experiment/fcc/ee/jet_flavour_tagging/fullsim_test_spring2024/fullsimCLD240_2mio.onnx")
parser_group.add_argument("--json_onnx_config", help="Path to JSON config file for ONNX model used for tagging", default="/eos/experiment/fcc/ee/jet_flavour_tagging/fullsim_test_spring2024/preprocess_fullsimCLD240_2mio.json")
parser_group.add_argument("--num_ev", type=int, help="Number of events to process (-1 means all)", default=-1)

args = parser.parse_known_args()[0]

svc = IOSvc("IOSvc")
svc.Input = args.inputFiles
svc.Output = args.outputFile

algList = []

### Jet Clustering

MyFastJetProcessor = MarlinProcessorWrapper("MyFastJetProcessor")
MyFastJetProcessor.ProcessorType = "FastJetProcessor"
MyFastJetProcessor.Parameters = {
    "algorithm": ["ee_kt_algorithm"],
    "clusteringMode": ["ExclusiveNJets", "2"],
    "findNrJets": ["2"],
    "findNrJetsCollectionPrefix": ["Jets_"],
    "jetOut": ["Durham_2Jets"],
    "recParticleIn": ["PandoraPFOs"], # ["PandoraPFOsWithoutIsoLep"],
    "recParticleOut": ["Durham_2JetsPFOs"],
    "recombinationScheme": ["E_scheme"],
    "storeParticlesInJets": ["true"],
}
# conversion from LCIO to EDM4hep
from Configurables import Lcio2EDM4hepTool
lcioConvTool = Lcio2EDM4hepTool("lcio2EDM4hep")
lcioConvTool.convertAll = False
lcioConvTool.collNameMapping = {
    "PandoraPFOs": "PandoraPFOs",
}
MyFastJetProcessor.Lcio2EDM4hepTool = lcioConvTool
# conversion from EDM4hep to LCIO
from Configurables import EDM4hep2LcioTool
lcioConvTool2 = EDM4hep2LcioTool("EDM4hep2lcio")
lcioConvTool2.convertAll = False
lcioConvTool2.collNameMapping = {
    "PandoraPFOs": "PandoraPFOs",
}
MyFastJetProcessor.EDM4hep2LcioTool = lcioConvTool2

algList.append(MyFastJetProcessor)


ApplicationMgr(TopAlg=algList,
               EvtSel="NONE",
               EvtMax=args.num_ev,
               ExtSvc=[k4DataSvc("EventDataSvc")],
               OutputLevel=DEBUG,
               )