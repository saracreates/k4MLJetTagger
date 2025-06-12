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
from k4MarlinWrapper.io_helpers import IOHandlerHelper
from typing import Union, Optional, Dict, Any, List

def parse_collection_patch_file(patch_file: Union[str, os.PathLike]) -> List[str]:
    """Parse a collection patch file such that it can be used by the
    PatchCollections processor.
    This function reads the file that has been passed in and effectively
    flattens its contents into one list of strings. The main assumption is that
    the file has been produced via `check_missing_colls --minimal <...>` in
    which case it can be directly consumed. Note that no real error checking is
    done to detect malformed inputs in which case something else at a later
    stage will most likely break.
    Args:
        patch_file (Union[str, os.PathLike]): The path to the file that should
                                              be parsed
    Returns:
        List[str]: A list of strings (pairs of "names" and "types") that can be
                   consumed by the PatchCollections processor
    """
    with open(patch_file, "r") as pfile:
        patch_colls = [l.split() for l in pfile.readlines()]

    # Flatten the list of lists into one large list
    return [s for strings in patch_colls for s in strings]

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

evtsvc = EventDataSvc("EventDataSvc")
iosvc = IOSvc()

svcList = [evtsvc, iosvc]
algList = []

io_handler = IOHandlerHelper(algList, iosvc)
io_handler.add_reader(args.inputFiles)

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
from Configurables import EDM4hep2LcioTool
lcioConvTool = EDM4hep2LcioTool("EDM4hep2lcio")
lcioConvTool.convertAll = False
lcioConvTool.collNameMapping = {
    "PandoraPFOs": "PandoraPFOs",
}
MyFastJetProcessor.EDM4hep2LcioTool = lcioConvTool

algList.append(MyFastJetProcessor)

### Conversions 

CONFIG = {
             "OutputMode": "EDM4Hep",
}

REC_COLLECTION_CONTENTS_FILE = "/afs/cern.ch/work/s/saaumill/public/k4MLJetTagger/k4MLJetTagger/options/collections_rec_level.txt" # file with the collections to be patched in when writing from LCIO to EDM4hep

DST_KEEPLIST = ["MCParticlesSkimmed", "MCPhysicsParticles", "RecoMCTruthLink", "SiTracks", "SiTracks_Refitted", "PandoraClusters", "PandoraPFOs", "SelectedPandoraPFOs", "LooseSelectedPandoraPFOs", "TightSelectedPandoraPFOs", "RefinedVertexJets", "RefinedVertexJets_rel", "RefinedVertexJets_vtx", "RefinedVertexJets_vtx_RP", "BuildUpVertices", "BuildUpVertices_res", "BuildUpVertices_RP", "BuildUpVertices_res_RP", "BuildUpVertices_V0", "BuildUpVertices_V0_res", "BuildUpVertices_V0_RP", "BuildUpVertices_V0_res_RP", "PrimaryVertices", "PrimaryVertices_res", "PrimaryVertices_RP", "PrimaryVertices_res_RP", "RefinedVertices", "RefinedVertices_RP"]

DST_SUBSETLIST = ["EfficientMCParticles", "InefficientMCParticles", "MCPhysicsParticles"]

# TODO: replace all the ugly strings by something sensible like Enum
if CONFIG["OutputMode"] == "LCIO":
    Output_REC = io_handler.add_lcio_writer("Output_REC")
    Output_REC.Parameters = {
        "LCIOOutputFile": [f"{args.outputBasename}_REC.slcio"],
        "LCIOWriteMode": ["WRITE_NEW"],
    }

    Output_DST = io_handler.add_lcio_writer("Output_DST")
    dropped_types = ["MCParticle", "LCRelation", "SimCalorimeterHit", "CalorimeterHit", "SimTrackerHit", "TrackerHit", "TrackerHitPlane", "Track", "ReconstructedParticle", "LCFloatVec"]
    Output_DST.Parameters = {
        "LCIOOutputFile": [f"{args.outputBasename}_DST.slcio"],
        "LCIOWriteMode": ["WRITE_NEW"],
        "DropCollectionNames": [],
        "DropCollectionTypes": dropped_types,
        "FullSubsetCollections": DST_SUBSETLIST,
        "KeepCollectionNames": DST_KEEPLIST,
    }
    algList.append(Output_DST)

if CONFIG["OutputMode"] == "EDM4Hep":
    # Make sure that all collections are always available by patching in missing ones on-the-fly
    collPatcherRec = MarlinProcessorWrapper(
        "CollPatcherREC", OutputLevel=INFO, ProcessorType="PatchCollections"
    )
    collPatcherRec.Parameters = {
        "PatchCollections": parse_collection_patch_file(REC_COLLECTION_CONTENTS_FILE)
    }
    algList.append(collPatcherRec)

    io_handler.add_edm4hep_writer(f"{args.outputBasename}_REC.edm4hep.root", ["keep *"])
    # FIXME: needs https://github.com/key4hep/k4FWCore/issues/226
    # <DST output for edm4hep>


# We need to attach all the necessary converters
io_handler.finalize_converters()

ApplicationMgr(TopAlg=algList,
               EvtSel="NONE",
               EvtMax=args.num_ev,
               ExtSvc=[k4DataSvc("EventDataSvc")],
               OutputLevel=DEBUG,
               )