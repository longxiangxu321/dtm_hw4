# DTM Homework 4
[TOC]
## Introduction
This homework is about **Point Cloud Processing**. It includes
- Cropping a large point cloud data
- A simple implementation of Cloth Simulation Filter <https://www.mdpi.com/2072-4292/8/6/501/htm?ref=https://githubhelp.com>
- Generating Digital Terrain Model(DTM) based on ground points
- Comparison of two DTM
- Extracting isolines

## Team Member
- *Bingshiuan Tsai*
- *Mengying Chen*
- *Longxiang Xu*

## Requirements
The code has been tested with Python 3.8.
Required packages:
- laspy 2.3.0
- matplotlib 3.5.3
- numpy 1.21.2
- rasterio 1.2.10
- scipy 1.9.0
- startinpy 0.9.2

## Folder Structure
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
