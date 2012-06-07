---
layout: default
sections: ["Authors", "License", "Contributors", "Notes", "Installation", "Usage"]
---

Luck isn't a factor when you're using **The Thresher**.

You have taken lots of very fast imaging (think "lucky imaging"),
hoping for good seeing.  What to do with your data?  The great
advantage of **The Thresher** is that *We Don't Throw Away Data&trade;*.
Our goal is to deliver the signal-to-noise contained in the entire
data set, but at the resolution of the *best* images in the data set.

### Authors

- **[Dan Foreman-Mackey](http://danfm.ca/)**, New York University
- **[David W. Hogg](http://cosmo.nyu.edu/hogg/)**, New York University

### License

Copyright 2012 the authors.

The Thresher is free software licensed under the **GNU General Public
License Version 2**.  See the file `LICENSE` for the full terms of this
license.

### Contributors

- **Federica Bianco**, Las Cumbres Observatory
- **BJ Fulton**, Las Cumbres Observatory
- **Dustin Lang**, Princeton University Observatory
- **Phil Marshall**, Oxford University

Partial financial support was provided by the
**National Science Foundation** and the
**National Aeronautics and Space Administration**.

### Notes

**The Thresher** is based on a mash-up of

- Hirsch et al (2011, A&A, 26, 531) *[Online multi-frame blind deconvolution
  with super-resolution and saturation correction](http://adsabs.harvard.edu/abs/2011A%26A...531A...9H>)* and
- Magain et al (1998, ApJ 494, 472) *[Deconvolution with correct sampling](http://adsabs.harvard.edu/abs/1998ApJ...494..472M)*.

At its current version, **The Thresher** is expecting to a set of
single-band constant-pixel-scale band-limited images of the same
unvarying scene.  **The Thresher** returns the best
(maximum-likelihood) band-limited scene that can explain those images,
plus a set of point-spread functions, one per image.

For generalizations to multi-band or multi-instrument imaging, or
generalizations to time-variable scenes, watch this space.  For
generalizations that permit sampling the posterior PDF in scene space,
or full marginalization over PSF choices, don't hold your breath.

### Installation

*Watch this space.*

### Usage

The data should be in a set of `FITS` files in a directory somewhere.
To run the pipeline on this directory, run `bin/thresh` as follows:

```
bin/thresh '/path/to/data/*.fits' -o /directory/for/output --size 64
```

You can run `bin/thresh -h` for more command line options.

To plot the inference in real time, start the `bin/thresh-plot` daemon,
which will monitor the output directory and generate the plots:

```
bin/thresh-plot /path/to/outputs -m -o /path/to/plots
```

To generate all of the plots for an existing run, use:

```
bin/thresh-plot /path/to/outputs -o /path/to/plots
```

You can also run TLI (traditional lucky imaging) on the same data as
follows:

```
bin/tli '/path/to/data/*.fits' 64 -o tli.fits
```