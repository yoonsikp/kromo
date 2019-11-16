# kromo
`kromo` is a play on words, combining "chromatic aberration" and "lo-mo photography". I made `kromo` because perfect optics are overrated.
## Before & After
<p align="center">
  <img src=https://github.com/yoonsikp/kromo/blob/master/beforeafter.gif?raw=true width=60%>
 </p>
 <p align="center">
  Image of Berries, 1.0 strength
</p>

## [Image Gallery](https://github.com/yoonsikp/kromo/blob/master/gallery.md)

## Quick Start
```
$ python3 kromo.py -v flower.jpg 

Original Image: JPEG (1962, 2615) RGB
Dimensions must be odd numbers, cropping...
New Dimensions: (1961, 2615)
Completed in:  80.14s

```

## Usage
```
$ python3 kromo.py --help

usage: kromo.py [-h] [-s STRENGTH] [-j JITTER] [-y OVERLAY] [-n] [-o OUTPUT]
                [-v]
                filename

Apply chromatic aberration and lens blur to images

positional arguments:
  filename              input filename

optional arguments:
  -h, --help            show this help message and exit
  -s STRENGTH, --strength STRENGTH
                        set blur/aberration strength, defaults to 1.0
  -j JITTER, --jitter JITTER
                        set color channel offset pixels, defaults to 0
  -y OVERLAY, --overlay OVERLAY
                        alpha of original image overlay, defaults to 1.0
  -n, --noblur          disable radial blur
  -o OUTPUT, --output OUTPUT
                        write to OUTPUT (supports multiple formats)
  -v, --verbose         print status messages
```

## Runtime
`kromo` is slow, just like how film photography used to be. Clone the repo for a blast from the past.

The time complexity is O(n), so a 12MP picture takes 4 times longer than a 3MP picture.

## See also
[Circular & radial blur](http://chemaguerra.com/circular-radial-blur/)

[Use depth-of-field and other lens effects](https://doc.babylonjs.com/how_to/using_depth-of-field_and_other_lens_effects)
