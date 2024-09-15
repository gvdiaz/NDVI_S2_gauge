from snappy import Product
from snappy import ProductIO
from snappy import ProductUtils

geom_name = 'shape'
product = ProductIO.readProduct('my_s1_dim_here')
polygons_wkt = "POLYGON ((-0.379473496337121 51.806829421554639...)"


#add the wkt geometry to the product using a seperate method which returns a product with added vector
masked_product = self.add_wkt_vector_geom(product , geom_name, polygons_wkt)


#make new product
w = masked_product.getSceneRasterWidth()
h = masked_product.getSceneRasterheight()
out_product = Product('masked', 'masked', w, h)
ProductUtils.copyGeoCoding(masked_product, out_product)
writer = ProductIO.getProductWriter('BEAM-DIMAP')
out_product.setProductWriter(writer)

band_names = masked_product.getBandNames()
#apply to all bands
for band_name in band_names:
    print('defining output bands:', band_name)
    ProductUtils.copyBand(band_name, masked_product, out_product, False) # assuming the bands are already Float32

# first the bands must be defined, then we can write the header
out_product.writeHeader('masked_product.dim')

geom_mask = masked_product.getMaskGroup().get(geom_name)
#apply to all bands
for band_name in band_names:
    print('reading band:', band_name)
    #add a band to be masked
    src_band = masked_product.getBand(band_name)
    out_band = out_product.getBand(band_name)
    #set the band noData values
    out_band.setNoDataValue(np.nan)
    out_band.setNoDataValueUsed(True)

    data_array = np.zeros(shape=(w, h), dtype=np.float32)
    src_band.readPixels(0, 0, w, h, data_array)

    #array for mask values
    mask_array = np.zeros(shape=(w, h), dtype=np.int32) # maybe uint8 also works
    #read the pixels into an array
    geom_name.readPixels(0, 0, w, h, mask_array)
    # create a numpy mask condition
    invalid_mask = np.where(mask_array == 0, 1, 0)
    #apply the mask to our masked array
    masked_data = np.ma.array(data_array, mask=invalid_mask, fill_value=np.nan)
    #write the masked band
    out_band.writePixels(0, 0, w, h, masked_data)

# write changed header again
out_product.writeHeader('masked_product.dim')

print('Masking finished')
