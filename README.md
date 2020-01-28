# RTDoseMining
Data mining of RT Dose in DICOM-RT files
![](https://i.imgur.com/KX6WGxm.jpg)

# RT Dose
The RT Dose was introduced in 1996 with Supplement 11 together with RT Image, RT Structure Set and RT Plan as the first RT-specific DICOM objects. The focus for this Radiotherapy Dose Information Object Definition (IOD) is to address the requirements for transfer of dose distributions calculated by radiotherapy treatment planning systems. These distributions may be represented as 2D or 3D grids, as isodose curves, or as named or unnamed dose points scattered throughout the volume. This IOD may also contain dose-volume histogram data, single or multi-frame overlays. This project presents the work done for the data mining of the DICOM-RT files, specifically the RT Dose object and the RT Dose and RT DVH modules.

## Methodology
The [PyDicom](https://github.com/pydicom/pydicom) library was used to manipulate the data of the DICOM files.  It was necessary to obtain the necessary values for the construction of the dose-volume histograms and proceed to the respective calculations. It was concluded that this work would depend on the content of the RT Dose and RT Struct objects.

### RT Dose values used
+ (3004, 0050) DVH Sequence:
 + (3004, 0001) DVH Type
 + (3004, 0002) Dose Units
 + (3004, 0004) Dose Type
 + (3004, 0052) DVH Dose Scaling
 + (3004, 0054) DVH Volume Units
 + (3004, 0056) DVH Number of Bins
 + (3004, 0058) DVH Data

By analysing the Pixel Data tag, it was also possible to represent the images of the doses

## Results
<a href="https://imgur.com/d1OA2p5"><img src="https://i.imgur.com/d1OA2p5b.jpg" title="source: imgur.com" /></a>
<a href="https://imgur.com/E2E3xxt"><img src="https://i.imgur.com/E2E3xxtb.jpg" title="source: imgur.com" /></a>
