import rasterio

def main():
    raster = rasterio.open("cloth_dtm.tif")
    breakpoint()
    print("az")

if __name__ == '__main__':
    main()