# Introduction
This homework is about **Point Cloud Processing**. It includes
- **Cropping a large point cloud data**
- **A simple implementation of Cloth Simulation Filter**    
        <https://www.mdpi.com/2072-4292/8/6/501/htm?ref=https://githubhelp.com>
- **Generating Digital Terrain Model(DTM) based on ground points**
- **Comparison of two DTM**
- **Extracting isolines**


# Table of Content
- [Team Member](#team-member)
- [Requirements](#requirements)
- [Folder Structure](#folder-structure)
- [Run and Configuration](#run-and-configuration)
  * [Data](#data)
  * [crop.py](#croppy)
  * [csf.py](#csfpy)
  * [dtm.py](#dtmpy)
  * [thining.py](#thiningpy)
  * [compare.py](#comparepy)
  * [isoline.py](#isolinepy)


# Team Member
- *Bingshiuan Tsai*
- *Mengying Chen*
- *Longxiang Xu*

# Requirements
The code has been tested with Python 3.8.   
Required packages:
- laspy 2.3.0
- matplotlib 3.5.3
- numpy 1.21.2
- rasterio 1.2.10
- scipy 1.9.0
- startinpy 0.9.2

# Folder Structure
```
hw4
├─ compare.py  
├─ crop.py  
├─ csf.py  
├─ data  
│    ├─ dtm  
│    │    ├─ cloth_dtm.tif  
│    │    ├─ ground_dtm.tif  
│    │    ├─ roi_dtm.tif  
│    │    └─ roi_dtm.tif.aux.xml  
│    ├─ isoline  
│    │    ├─ cloth_isoline.wkt  
│    │    └─ ground_isoline.wkt  
│    └─ pointcloud  
│           ├─ cloth_points.laz  
│           ├─ ground_points.laz   
│           ├─ non_ground_points.laz  
│           ├─ nth_thinned_10%.laz  
│           ├─ nth_thinned_50%.laz  
│           ├─ random_thinned_10%.laz  
│           ├─ random_thinned_50%.laz  
│           └─ roi.laz
├─ dtm.py  
├─ isoline.py  
└─ thinning.py  
```

# Run and Configuration
## Data
Original data can be down loadded from PDOK  <https://download.pdok.nl/rws/ahn3/v1_0/laz/C_68GZ1.LAZ>

## crop.py
This program crop a subset of the original point cloud using chunked reading.   


Change the 'xmin', 'ymin', and 'width', 'height' according to your desired bounding box.    
In our case, the settings are:
```
    xmin = 191952.00
    ymin = 325070.00
    width = 500
    height = 500
```

## csf.py
This program applys a cloth simulation filtering on the point cloud to obtain ground points. 


Modify the parameters below according to your test on your data.   
In our case, the following values were used.
```
    resolution = 4 # grid size of the cloth
    tension = 0.5 
    gravity = 0.3
    max_iter = 500
    threshold = 0.1 # non-movable threshold force
    z_tolerance = 0.3 # off ground tolerance
```

## dtm.py
This program generate raster DTM according to the input point cloud.  

The `resolution of desired output can be specified`.

## thining.py
This program generate thinned point cloud using random thining and nth_point thinning.
  
The sampling percentage can be specified from 0 to 100.

## compare.py
This program compare the difference of two raster DTM, output heat map and RMSE.
  
If the second input of `compare_dtm` is downloaded from AHN, the parameter 'dtm2flip=' needs to be set to `True`.

## isoline.py
This program extract isolines from input raster DTM.
  
The `isoline_interval` can be determined by the user.

