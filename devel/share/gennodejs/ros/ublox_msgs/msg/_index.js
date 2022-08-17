
"use strict";

let NavSTATUS = require('./NavSTATUS.js');
let NavCLOCK = require('./NavCLOCK.js');
let NavDGPS = require('./NavDGPS.js');
let NavPOSLLH = require('./NavPOSLLH.js');
let CfgDGNSS = require('./CfgDGNSS.js');
let CfgSBAS = require('./CfgSBAS.js');
let MonHW6 = require('./MonHW6.js');
let CfgMSG = require('./CfgMSG.js');
let CfgINF_Block = require('./CfgINF_Block.js');
let CfgNAV5 = require('./CfgNAV5.js');
let AidALM = require('./AidALM.js');
let RxmRAWX = require('./RxmRAWX.js');
let MonVER_Extension = require('./MonVER_Extension.js');
let CfgNMEA = require('./CfgNMEA.js');
let CfgANT = require('./CfgANT.js');
let NavDOP = require('./NavDOP.js');
let CfgGNSS_Block = require('./CfgGNSS_Block.js');
let NavSAT = require('./NavSAT.js');
let NavVELECEF = require('./NavVELECEF.js');
let NavSVINFO = require('./NavSVINFO.js');
let EsfRAW = require('./EsfRAW.js');
let RxmRAW_SV = require('./RxmRAW_SV.js');
let AidEPH = require('./AidEPH.js');
let CfgTMODE3 = require('./CfgTMODE3.js');
let NavTIMEUTC = require('./NavTIMEUTC.js');
let Ack = require('./Ack.js');
let EsfSTATUS = require('./EsfSTATUS.js');
let MonGNSS = require('./MonGNSS.js');
let CfgRST = require('./CfgRST.js');
let UpdSOS = require('./UpdSOS.js');
let HnrPVT = require('./HnrPVT.js');
let NavVELNED = require('./NavVELNED.js');
let CfgUSB = require('./CfgUSB.js');
let RxmRAW = require('./RxmRAW.js');
let Inf = require('./Inf.js');
let NavSOL = require('./NavSOL.js');
let RxmEPH = require('./RxmEPH.js');
let NavSVIN = require('./NavSVIN.js');
let RxmRAWX_Meas = require('./RxmRAWX_Meas.js');
let UpdSOS_Ack = require('./UpdSOS_Ack.js');
let NavRELPOSNED = require('./NavRELPOSNED.js');
let TimTM2 = require('./TimTM2.js');
let NavSBAS_SV = require('./NavSBAS_SV.js');
let RxmALM = require('./RxmALM.js');
let MonVER = require('./MonVER.js');
let NavSBAS = require('./NavSBAS.js');
let AidHUI = require('./AidHUI.js');
let RxmSVSI_SV = require('./RxmSVSI_SV.js');
let CfgPRT = require('./CfgPRT.js');
let CfgNMEA6 = require('./CfgNMEA6.js');
let NavSVINFO_SV = require('./NavSVINFO_SV.js');
let RxmSFRB = require('./RxmSFRB.js');
let RxmSVSI = require('./RxmSVSI.js');
let NavPOSECEF = require('./NavPOSECEF.js');
let CfgNMEA7 = require('./CfgNMEA7.js');
let NavPVT = require('./NavPVT.js');
let EsfSTATUS_Sens = require('./EsfSTATUS_Sens.js');
let CfgNAVX5 = require('./CfgNAVX5.js');
let CfgINF = require('./CfgINF.js');
let EsfINS = require('./EsfINS.js');
let CfgGNSS = require('./CfgGNSS.js');
let NavATT = require('./NavATT.js');
let NavDGPS_SV = require('./NavDGPS_SV.js');
let CfgHNR = require('./CfgHNR.js');
let NavTIMEGPS = require('./NavTIMEGPS.js');
let RxmSFRBX = require('./RxmSFRBX.js');
let NavPVT7 = require('./NavPVT7.js');
let EsfMEAS = require('./EsfMEAS.js');
let CfgRATE = require('./CfgRATE.js');
let NavSAT_SV = require('./NavSAT_SV.js');
let EsfRAW_Block = require('./EsfRAW_Block.js');
let RxmRTCM = require('./RxmRTCM.js');
let MonHW = require('./MonHW.js');
let CfgDAT = require('./CfgDAT.js');
let MgaGAL = require('./MgaGAL.js');
let CfgCFG = require('./CfgCFG.js');

module.exports = {
  NavSTATUS: NavSTATUS,
  NavCLOCK: NavCLOCK,
  NavDGPS: NavDGPS,
  NavPOSLLH: NavPOSLLH,
  CfgDGNSS: CfgDGNSS,
  CfgSBAS: CfgSBAS,
  MonHW6: MonHW6,
  CfgMSG: CfgMSG,
  CfgINF_Block: CfgINF_Block,
  CfgNAV5: CfgNAV5,
  AidALM: AidALM,
  RxmRAWX: RxmRAWX,
  MonVER_Extension: MonVER_Extension,
  CfgNMEA: CfgNMEA,
  CfgANT: CfgANT,
  NavDOP: NavDOP,
  CfgGNSS_Block: CfgGNSS_Block,
  NavSAT: NavSAT,
  NavVELECEF: NavVELECEF,
  NavSVINFO: NavSVINFO,
  EsfRAW: EsfRAW,
  RxmRAW_SV: RxmRAW_SV,
  AidEPH: AidEPH,
  CfgTMODE3: CfgTMODE3,
  NavTIMEUTC: NavTIMEUTC,
  Ack: Ack,
  EsfSTATUS: EsfSTATUS,
  MonGNSS: MonGNSS,
  CfgRST: CfgRST,
  UpdSOS: UpdSOS,
  HnrPVT: HnrPVT,
  NavVELNED: NavVELNED,
  CfgUSB: CfgUSB,
  RxmRAW: RxmRAW,
  Inf: Inf,
  NavSOL: NavSOL,
  RxmEPH: RxmEPH,
  NavSVIN: NavSVIN,
  RxmRAWX_Meas: RxmRAWX_Meas,
  UpdSOS_Ack: UpdSOS_Ack,
  NavRELPOSNED: NavRELPOSNED,
  TimTM2: TimTM2,
  NavSBAS_SV: NavSBAS_SV,
  RxmALM: RxmALM,
  MonVER: MonVER,
  NavSBAS: NavSBAS,
  AidHUI: AidHUI,
  RxmSVSI_SV: RxmSVSI_SV,
  CfgPRT: CfgPRT,
  CfgNMEA6: CfgNMEA6,
  NavSVINFO_SV: NavSVINFO_SV,
  RxmSFRB: RxmSFRB,
  RxmSVSI: RxmSVSI,
  NavPOSECEF: NavPOSECEF,
  CfgNMEA7: CfgNMEA7,
  NavPVT: NavPVT,
  EsfSTATUS_Sens: EsfSTATUS_Sens,
  CfgNAVX5: CfgNAVX5,
  CfgINF: CfgINF,
  EsfINS: EsfINS,
  CfgGNSS: CfgGNSS,
  NavATT: NavATT,
  NavDGPS_SV: NavDGPS_SV,
  CfgHNR: CfgHNR,
  NavTIMEGPS: NavTIMEGPS,
  RxmSFRBX: RxmSFRBX,
  NavPVT7: NavPVT7,
  EsfMEAS: EsfMEAS,
  CfgRATE: CfgRATE,
  NavSAT_SV: NavSAT_SV,
  EsfRAW_Block: EsfRAW_Block,
  RxmRTCM: RxmRTCM,
  MonHW: MonHW,
  CfgDAT: CfgDAT,
  MgaGAL: MgaGAL,
  CfgCFG: CfgCFG,
};
