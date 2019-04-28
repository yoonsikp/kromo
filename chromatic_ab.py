from PIL import Image
import numpy as np
import sys
import math
import time

def cartesian_to_polar(data):
    width = data.shape[1]
    height = data.shape[0]
    assert (width > 2)
    assert (height > 2)
    assert (width % 2 == 1)
    assert (height % 2 == 1)
    perimeter = 2 * (width + height - 2)
    halfdiag = math.ceil(((width ** 2 + height ** 2) ** 0.5) / 2)
    halfw = width // 2
    halfh = height // 2
    ret = np.zeros((halfdiag, perimeter))
    # ret[0] = data[halfh, halfw]
    # Don't want to deal with divide by zero errors...
    ret[0:(halfw + 1), halfh] = data[halfh, halfw::-1]
    ret[0:(halfw + 1), height + width - 2 + halfh] = data[halfh, halfw:(halfw * 2 + 1)]
    ret[0:(halfh + 1), height - 1 + halfw] = data[halfh:(halfh * 2 + 1), halfw]
    ret[0:(halfh + 1), perimeter - halfw] = data[halfh::-1, halfw]
    # if we divide the rectangle into 8 triangles, we can do 4 triangles at a time
    # This section is responsible for triangles incl. corners
    for i in range(0, halfh):
        slope = (halfh - i) / (halfw)
        diagx = ((halfdiag ** 2)/(slope ** 2 + 1)) ** 0.5
        unit_xstep = diagx / (halfdiag - 1)
        unit_ystep = diagx * slope / (halfdiag - 1)
        for row in range(halfdiag):
            ystep = round(row * unit_ystep)
            xstep = round(row * unit_xstep)
            if ( (halfh >= ystep) and halfw >= xstep):
                ret[row, i] = data[halfh - ystep, halfw - xstep]
                ret[row, height - 1 - i] = data[halfh + ystep, halfw - xstep]
                ret[row, height + width - 2 + i] = data[halfh + ystep, halfw + xstep]
                ret[row, height + width + height - 3 - i] = data[halfh - ystep, halfw + xstep] 
            else:
                break

    for j in range(1, halfw):
        slope = (halfh) / (halfw - j)
        diagx = ((halfdiag ** 2)/(slope ** 2 + 1)) ** 0.5
        unit_xstep = diagx / (halfdiag - 1)
        unit_ystep = diagx * slope / (halfdiag - 1)
        for row in range(halfdiag):
            ystep = round(row * unit_ystep)
            xstep = round(row * unit_xstep)
            if ( halfw >= xstep and halfh >= ystep ):
                ret[row, height - 1 + j] = data[halfh + ystep, halfw - xstep]
                ret[row, height + width - 2 - j] = data[halfh + ystep, halfw + xstep]
                ret[row, height + width + height - 3 + j] = data[halfh - ystep, halfw + xstep]
                ret[row, perimeter - j] = data[halfh - ystep, halfw - xstep]
            else:
                break
    return ret

def polar_to_cartesian(data, width, height):
    assert (width > 2)
    assert (height > 2)
    assert (width % 2 == 1)
    assert (height % 2 == 1)
    perimeter = 2 * (width + height - 2)
    halfdiag = math.ceil(((width ** 2 + height ** 2) ** 0.5) / 2)
    halfw = width // 2
    halfh = height // 2
    ret = np.zeros((height, width))
    # Don't want to deal with divide by zero errors...
    ret[halfh, halfw::-1] = data[0:(halfw + 1), halfh]
    ret[halfh, halfw:(halfw * 2 + 1)] = data[0:(halfw + 1), height + width - 2 + halfh]
    ret[halfh:(halfh * 2 + 1), halfw] = data[0:(halfh + 1), height - 1 + halfw]
    ret[halfh::-1, halfw] = data[0:(halfh + 1), perimeter - halfw]

    # This section is responsible for triangles incl. corners
    for i in range(0, halfh):
        slope = (halfh - i) / (halfw)
        diagx = ((halfdiag ** 2)/(slope ** 2 + 1)) ** 0.5
        unit_xstep = diagx / (halfdiag - 1)
        unit_ystep = diagx * slope / (halfdiag - 1)
        for row in range(halfdiag):
            ystep = round(row * unit_ystep)
            xstep = round(row * unit_xstep)
            if ( (halfh >= ystep) and halfw >= xstep):
                ret[halfh - ystep, halfw - xstep] = data[row, i]
                ret[halfh + ystep, halfw - xstep] = data[row, height - 1 - i]
                ret[halfh + ystep, halfw + xstep] = data[row, height + width - 2 + i]
                ret[halfh - ystep, halfw + xstep] = data[row, height + width + height - 3 - i]
            else:
                break

    for j in range(1, halfw):
        slope = (halfh) / (halfw - j)
        diagx = ((halfdiag ** 2)/(slope ** 2 + 1)) ** 0.5
        unit_xstep = diagx / (halfdiag - 1)
        unit_ystep = diagx * slope / (halfdiag - 1)
        for row in range(halfdiag):
            ystep = round(row * unit_ystep)
            xstep = round(row * unit_xstep)
            if ( halfw >= xstep and halfh >= ystep ):
                ret[halfh + ystep, halfw - xstep] = data[row, height - 1 + j]
                ret[halfh + ystep, halfw + xstep] = data[row, height + width - 2 - j]
                ret[halfh - ystep, halfw + xstep] = data[row, height + width + height - 3 + j]
                ret[halfh - ystep, halfw - xstep] = data[row, perimeter - j]
            else:
                break
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if ret[i,j] == 0:
                ret[i,j] = (ret[i - 1,j] + ret[i + 1,j]) / 2
    return ret

# https://stackoverflow.com/questions/11209115/creating-gaussian-filter-of-required-length-in-python
def get_gauss(n):
    sigma = 0.3 * (n/2 - 1) + 0.8
    r = range(-int(n/2),int(n/2)+1)
    new_sum = sum([1 / (sigma * math.sqrt(2*math.pi)) * math.exp(-float(x)**2/(2*sigma**2)) for x in r])
    return [(1 / (sigma * math.sqrt(2*math.pi)) * math.exp(-float(x)**2/(2*sigma**2))) / new_sum for x in r]

# n is the radius (1 pixel radius means no blur)
def vertical_gaussian(data, n):
    padding = n - 1
    width = data.shape[1]
    height = data.shape[0]
    padded_data = np.zeros((height + padding * 2, width))
    padded_data[padding: -padding, :] = data
    ret = np.zeros((height, width))
    kernel = None
    old_radius = - 1
    for i in range(height):
        radius = round(i * padding / (height - 1)) + 1
        if (radius != old_radius):
            old_radius = radius
            kernel = np.tile(get_gauss(1 + 2 * (radius - 1)), (width,1)).transpose()
        ret[i, :] = np.sum(np.multiply(padded_data[padding + i - (radius - 1):padding + i + radius, :], kernel),axis = 0)
    return ret

def add_chromatic(im, blurfactor = 1):
    r, g, b = im.split()
    rdata = np.asarray(r)
    gdata = np.asarray(g)
    bdata = np.asarray(b)
        
    rpolar = cartesian_to_polar(rdata)
    gpolar = cartesian_to_polar(gdata)
    bpolar = cartesian_to_polar(bdata)

    bluramount = (im.size[0] + im.size[1] - 2) / 100 * blurfactor
    if round(bluramount) > 0:
        rpolar = vertical_gaussian(rpolar,round(bluramount))
        gpolar = vertical_gaussian(gpolar,round(bluramount*1.2))
        bpolar = vertical_gaussian(bpolar,round(bluramount*1.4))

    rcartes = polar_to_cartesian(rpolar, width = rdata.shape[1], height = rdata.shape[0])
    gcartes = polar_to_cartesian(gpolar, width = gdata.shape[1], height = gdata.shape[0])
    bcartes = polar_to_cartesian(bpolar, width = bdata.shape[1], height = bdata.shape[0])

    rfinal = Image.fromarray(np.uint8(rcartes) , 'L')
    gfinal = Image.fromarray(np.uint8(gcartes) , 'L')
    bfinal = Image.fromarray(np.uint8(bcartes) , 'L')

    gfinal = gfinal.resize((round((1 + 0.018 * blurfactor) * rcartes.shape[1]), round((1 + 0.018 * blurfactor) * rcartes.shape[0])), Image.ANTIALIAS)
    bfinal = bfinal.resize((round((1 + 0.044 * blurfactor) * rcartes.shape[1]), round((1 + 0.044 * blurfactor) * rcartes.shape[0])), Image.ANTIALIAS)

    rheight = rfinal.size[1]
    rwidth = rfinal.size[0]
    gheight = gfinal.size[1]
    gwidth = gfinal.size[0]
    bheight = bfinal.size[1]
    bwidth = bfinal.size[0]
    rhdiff = (bheight - rheight) // 2
    rwdiff = (bwidth - rwidth) // 2
    ghdiff = (bheight - gheight) // 2
    gwdiff = (bwidth - gwidth) // 2

    im = Image.merge("RGB", (rfinal.crop((-rwdiff, -rhdiff, bwidth - rwdiff, bheight - rhdiff)), gfinal.crop((-gwdiff, -ghdiff, bwidth - gwdiff, bheight - ghdiff)), bfinal))
    return im.crop((rwdiff, rhdiff, rwidth + rwdiff, rheight + rhdiff))

# Get Start Time
start = time.time()
if len(sys.argv) < 2:
    exit()
ifile = sys.argv[1]
im = Image.open(ifile)
print("Original Image details:", im.format, im.size, im.mode)

# Ensure width and height are odd numbers
if (im.size[0] % 2 == 0 or im.size[1] % 2 == 0):
    print("Dimensions must be odd, automatically cropping...")
    if (im.size[0] % 2 == 0):
        im = im.crop((0, 0, im.size[0] - 1, im.size[1]))
        im.load()
    if (im.size[1] % 2 == 0):
        im = im.crop((0, 0, im.size[0], im.size[1] - 1))
        im.load()
    print("New dimensions:", im.size)

final_im = add_chromatic(im, blurfactor = 0.5)

# Save Final Image
final_im.save(ifile.split('.')[0] + "_chromatic.jpg", quality=99)

# Get Finish Time
end = time.time()
print("Completed in: " + str(end - start) +"s")
