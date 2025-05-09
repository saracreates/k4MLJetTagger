/*
 * Copyright (c) 2020-2024 Key4hep-Project.
 *
 * This file is part of Key4hep.
 * See https://key4hep.github.io/key4hep-doc/ for further info.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef STRUCTS_H
#define STRUCTS_H

#include <iostream>
#include <stdexcept>
#include <vector>

struct Pfcand {
  /**
   * Structure to store the observables of a particle / jet constituent. These observables will be used as input
   * features to the neural network for jet flavor tagging with the Particle Transformer. For CLD, these are 33
   * observables including kinematics, PID and track parameters. NOTE: regarding the cov matrix, we use following
   * convenstion compared to FCCAnalysis: HERE | FCCAnalysis | explanation d0  | xy or dxy | transverse impact parameter
   * phi | dphi| azimuthal angle
   * tanLambda | ctngtheta or deta or dlambda | lambda is the dip angle of the track in r-z
   * omega | dpt | curvature in [1/mm]
   * z0 | dz | longitudinal impact parameter
   * All these transformations/convenstions can be found in the VarMapper class that is in Helpers.cpp
   */

  // kinematics
  float pfcand_erel_log, pfcand_thetarel, pfcand_phirel;
  float pfcand_e, pfcand_p; // needed for pf_vectors
  // PID
  int pfcand_type;
  int pfcand_charge;
  int pfcand_isEl, pfcand_isMu, pfcand_isGamma, pfcand_isChargedHad, pfcand_isNeutralHad;
  int pfcand_dndx, pfcand_tof; // dummy, filled with 0

  // track params
  // cov matrix - 15 values related to 5 Helix (see struct) parameters
  float pfcand_cov_omegaomega, pfcand_cov_tanLambdatanLambda, pfcand_cov_phiphi, pfcand_cov_d0d0, pfcand_cov_z0z0;
  float pfcand_cov_d0z0, pfcand_cov_phid0, pfcand_cov_tanLambdaz0, pfcand_cov_d0omega, pfcand_cov_d0tanLambda,
      pfcand_cov_phiomega, pfcand_cov_phiz0, pfcand_cov_phitanLambda, pfcand_cov_omegaz0, pfcand_cov_omegatanLambda;
  // IP
  float pfcand_d0, pfcand_z0;
  float pfcand_Sip2dVal, pfcand_Sip2dSig;
  float pfcand_Sip3dVal, pfcand_Sip3dSig;
  float pfcand_JetDistVal, pfcand_JetDistSig;

  void print_values() {
    std::cout << "pfcand_e" << pfcand_e << std::endl;
    std::cout << "pfcand_p" << pfcand_p << std::endl;
    std::cout << "pfcand_erel_log: " << pfcand_erel_log << std::endl;
    std::cout << "pfcand_thetarel: " << pfcand_thetarel << std::endl;
    std::cout << "pfcand_phirel: " << pfcand_phirel << std::endl;
    std::cout << "pfcand_type: " << pfcand_type << std::endl;
    std::cout << "pfcand_charge: " << pfcand_charge << std::endl;
    std::cout << "pfcand_isEl: " << pfcand_isEl << std::endl;
    std::cout << "pfcand_isMu: " << pfcand_isMu << std::endl;
    std::cout << "pfcand_isGamma: " << pfcand_isGamma << std::endl;
    std::cout << "pfcand_isChargedHad: " << pfcand_isChargedHad << std::endl;
    std::cout << "pfcand_isNeutralHad: " << pfcand_isNeutralHad << std::endl;
    std::cout << "pfcand_dndx: " << pfcand_dndx << std::endl;
    std::cout << "pfcand_tof: " << pfcand_tof << std::endl;
    std::cout << "pfcand_cov_omegaomega: " << pfcand_cov_omegaomega << std::endl;
    std::cout << "pfcand_cov_tanLambdatanLambda: " << pfcand_cov_tanLambdatanLambda << std::endl;
    std::cout << "pfcand_cov_phiphi: " << pfcand_cov_phiphi << std::endl;
    std::cout << "pfcand_cov_d0d0: " << pfcand_cov_d0d0 << std::endl;
    std::cout << "pfcand_cov_z0z0: " << pfcand_cov_z0z0 << std::endl;
    std::cout << "pfcand_cov_d0z0: " << pfcand_cov_d0z0 << std::endl;
    std::cout << "pfcand_cov_phid0: " << pfcand_cov_phid0 << std::endl;
    std::cout << "pfcand_cov_tanLambdaz0: " << pfcand_cov_tanLambdaz0 << std::endl;
    std::cout << "pfcand_cov_d0omega: " << pfcand_cov_d0omega << std::endl;
    std::cout << "pfcand_cov_d0tanLambda: " << pfcand_cov_d0tanLambda << std::endl;
    std::cout << "pfcand_cov_phiomega: " << pfcand_cov_phiomega << std::endl;
    std::cout << "pfcand_cov_phiz0: " << pfcand_cov_phiz0 << std::endl;
    std::cout << "pfcand_cov_phitanLambda: " << pfcand_cov_phitanLambda << std::endl;
    std::cout << "pfcand_cov_omegaz0: " << pfcand_cov_omegaz0 << std::endl;
    std::cout << "pfcand_cov_omegatanLambda: " << pfcand_cov_omegatanLambda << std::endl;
    std::cout << "pfcand_d0: " << pfcand_d0 << std::endl;
    std::cout << "pfcand_z0: " << pfcand_z0 << std::endl;
    std::cout << "pfcand_Sip2dVal: " << pfcand_Sip2dVal << std::endl;
    std::cout << "pfcand_Sip2dSig: " << pfcand_Sip2dSig << std::endl;
    std::cout << "pfcand_Sip3dVal: " << pfcand_Sip3dVal << std::endl;
    std::cout << "pfcand_Sip3dSig: " << pfcand_Sip3dSig << std::endl;
    std::cout << "pfcand_JetDistVal: " << pfcand_JetDistVal << std::endl;
    std::cout << "pfcand_JetDistSig: " << pfcand_JetDistSig << std::endl;
  }

  float get_attribute(std::string& attribute) {
    /**
     * Return the attributes of the Struct Pfcand given an string.
     * @param attribute: the attribute to return
     * @return: the value of the attribute
     */
    if (attribute == "pfcand_erel_log")
      return pfcand_erel_log;
    else if (attribute == "pfcand_thetarel")
      return pfcand_thetarel;
    else if (attribute == "pfcand_phirel")
      return pfcand_phirel;
    else if (attribute == "pfcand_type")
      return pfcand_type;
    else if (attribute == "pfcand_charge")
      return pfcand_charge;
    else if (attribute == "pfcand_isEl")
      return pfcand_isEl;
    else if (attribute == "pfcand_isMu")
      return pfcand_isMu;
    else if (attribute == "pfcand_isGamma")
      return pfcand_isGamma;
    else if (attribute == "pfcand_isChargedHad")
      return pfcand_isChargedHad;
    else if (attribute == "pfcand_isNeutralHad")
      return pfcand_isNeutralHad;
    else if (attribute == "pfcand_dndx")
      return pfcand_dndx;
    else if (attribute == "pfcand_tof")
      return pfcand_tof;
    else if (attribute == "pfcand_cov_omegaomega")
      return pfcand_cov_omegaomega;
    else if (attribute == "pfcand_cov_tanLambdatanLambda")
      return pfcand_cov_tanLambdatanLambda;
    else if (attribute == "pfcand_cov_phiphi")
      return pfcand_cov_phiphi;
    else if (attribute == "pfcand_cov_d0d0")
      return pfcand_cov_d0d0;
    else if (attribute == "pfcand_cov_z0z0")
      return pfcand_cov_z0z0;
    else if (attribute == "pfcand_cov_d0z0")
      return pfcand_cov_d0z0;
    else if (attribute == "pfcand_cov_phid0")
      return pfcand_cov_phid0;
    else if (attribute == "pfcand_cov_tanLambdaz0")
      return pfcand_cov_tanLambdaz0;
    else if (attribute == "pfcand_cov_d0omega")
      return pfcand_cov_d0omega;
    else if (attribute == "pfcand_cov_d0tanLambda")
      return pfcand_cov_d0tanLambda;
    else if (attribute == "pfcand_cov_phiomega")
      return pfcand_cov_phiomega;
    else if (attribute == "pfcand_cov_phiz0")
      return pfcand_cov_phiz0;
    else if (attribute == "pfcand_cov_phitanLambda")
      return pfcand_cov_phitanLambda;
    else if (attribute == "pfcand_cov_omegaz0")
      return pfcand_cov_omegaz0;
    else if (attribute == "pfcand_cov_omegatanLambda")
      return pfcand_cov_omegatanLambda;
    else if (attribute == "pfcand_d0")
      return pfcand_d0;
    else if (attribute == "pfcand_z0")
      return pfcand_z0;
    else if (attribute == "pfcand_Sip2dVal")
      return pfcand_Sip2dVal;
    else if (attribute == "pfcand_Sip2dSig")
      return pfcand_Sip2dSig;
    else if (attribute == "pfcand_Sip3dVal")
      return pfcand_Sip3dVal;
    else if (attribute == "pfcand_Sip3dSig")
      return pfcand_Sip3dSig;
    else if (attribute == "pfcand_JetDistVal")
      return pfcand_JetDistVal;
    else if (attribute == "pfcand_JetDistSig")
      return pfcand_JetDistSig;
    else if (attribute == "pfcand_e")
      return pfcand_e;
    else if (attribute == "pfcand_p")
      return pfcand_p;
    else
      throw std::invalid_argument("Attribute not found: " + attribute);
  };

  std::vector<std::string> get_attribute_names() {
    /**
     * Return a list of strings with all the attributes names of the Struct Pfcand.
     * @return: a list of strings with all the attributes names
     */
    return {"pfcand_erel_log",
            "pfcand_thetarel",
            "pfcand_phirel",
            "pfcand_e",
            "pfcand_p",
            "pfcand_type",
            "pfcand_charge",
            "pfcand_isEl",
            "pfcand_isMu",
            "pfcand_isGamma",
            "pfcand_isChargedHad",
            "pfcand_isNeutralHad",
            "pfcand_dndx",
            "pfcand_tof",
            "pfcand_cov_omegaomega",
            "pfcand_cov_tanLambdatanLambda",
            "pfcand_cov_phiphi",
            "pfcand_cov_d0d0",
            "pfcand_cov_z0z0",
            "pfcand_cov_d0z0",
            "pfcand_cov_phid0",
            "pfcand_cov_tanLambdaz0",
            "pfcand_cov_d0omega",
            "pfcand_cov_d0tanLambda",
            "pfcand_cov_phiomega",
            "pfcand_cov_phiz0",
            "pfcand_cov_phitanLambda",
            "pfcand_cov_omegaz0",
            "pfcand_cov_omegatanLambda",
            "pfcand_d0",
            "pfcand_z0",
            "pfcand_Sip2dVal",
            "pfcand_Sip2dSig",
            "pfcand_Sip3dVal",
            "pfcand_Sip3dSig",
            "pfcand_JetDistVal",
            "pfcand_JetDistSig"};
  };
};

struct Jet {
  std::vector<Pfcand> constituents;
  int flavor_fromMC_HjjZvv; // jet flavor from MC which is extracted from the the H(jj)Z(vv) process by looking at the
                            // daughters of the H boson
};

struct Helix {
  /**
   * Structure to store the helix parameters of a track wrt to the primary vertex. We use the key4hep convention
   * (https://github.com/key4hep/EDM4hep/blob/997ab32b886899253c9bc61adea9a21b57bc5a21/edm4hep.yaml#L195C9-L200 ):
   * - d0: transverse impact parameter
   * - phi: azimuthal angle
   * - omega: signed curvature of the track in [1/mm]
   * - z0: longitudinal impact parameter
   * - tanLambda: lambda is the dip angle of the track in r-z
   */
  float d0, phi, omega, z0, tanLambda;
};

#endif // STRUCTS_H