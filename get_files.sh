#! bin/sh
mkdir -p data
curl 'https://www.maine.gov/sos/cec/elec/results/2018/{Nov18CVRExportFINAL1,Nov18CVRExportFINAL2,Nov18CVRExportFINAL3,RepCD2-8final,UOCAVA-FINALRepCD2,UOCAVA-AUX-CVRRepCD2,UOCAVA2CVRRepCD2,AUXCVRProofedCVR95RepCD2}.xlsx' -o "data/#1.xlsx"
