"""
This file is part of The Thresher

"""

__all__ = ["plot_inference_step"]

import itertools

import numpy as np
from scipy.signal import convolve
from scipy.special import erf


def plot_image(ax, img, size=None, vrange=None):
    """
    A wrapper to nicely plot an image the way that Hogg likes it.

    ## Arguments

    * `ax` (matplotlib.Axes): The axes to plot into.
    * `img` (numpy.ndarray): The image.

    ## Keyword Arguments

    * `size` (int): The size to crop/pad the image to.
    * `vrange` (tuple): The image stretch range.

    """
    if vrange is None:
        a, b = np.median(img), np.max(img)
        vmin, vmax = a - 0.2 * b, a + b
    else:
        vmin, vmax = vrange

    if size is None:
        size = np.mean(img.shape)

    # Invert the image.
    vmin, vmax = -vmax, -vmin

    ax.imshow(-img, cmap="gray", interpolation="nearest",
            vmin=vmin, vmax=vmax)

    # Crop/pad to the right size.
    xmin, xmax = (img.shape[0] - size) / 2, (img.shape[0] + size) / 2 - 1
    ymin, ymax = (img.shape[1] - size) / 2, (img.shape[1] + size) / 2 - 1
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)


def estimate_sigma(scene, nsigma=3.5, tol=0.0):
    img = scene.flatten()
    mask = ~np.isnan(img)
    ms_old = 0.0
    for i in range(500):
        m = np.median(img[mask])
        ms = np.mean((img[mask] - m) ** 2)
        mask = (img - m) ** 2 < nsigma ** 2 * ms
        if i > 1 and np.abs(ms - ms_old) < tol:
            break
        ms_old = ms
    return np.sqrt(ms)


def plot_inference_step(fig, data, old_scene, new_scene, dpsf, dlds,
        meta=[], sky=0.0, dc=0.0):
    """
    Plot the images produced by a single update step.

    NOTE: The stretch is the _same_ in most of the plots.

    ## Arguments

    * `fig` (matplotlib.Figure): The figure to clear and plot into.
    * `data` (numpy.ndarray): The data image.
    * `this_scene` (numpy.ndarray): The scene implied by _this datapoint
      only_.
    * `new_scene` (numpy.ndarray): The updated scene.
    * `dpsf` (numpy.ndarray): The deconvolved PSF image.
    * `kernel` (numpy.ndarray): The user-defined kernel.

    """
    fig.clf()
    fig.subplots_adjust(left=0.02, bottom=0.02, right=0.98, top=0.95,
            wspace=0.05, hspace=0.1)

    # Build the subplots.
    rows, cols = 2, 3
    axes = []

    for ri, ci in itertools.product(range(rows), range(cols)):
        axes.append(fig.add_subplot(rows, cols, ri * cols + ci + 1))
        axes[-1].set_xticklabels([])
        axes[-1].set_yticklabels([])

    # Calculate stretch.
    scene_sigma = estimate_sigma(new_scene)
    data_sigma = estimate_sigma(data)

    # scene_range = np.array([-2.5, 5]) * sigma

    # Compute the predicted image.
    predicted = convolve(old_scene, dpsf, mode="valid")

    # Medians.
    scene_median = np.median(new_scene)
    data_median = np.median(data)

    # Arcsinh.
    asinh = lambda img, mu, sigma, f: f * np.arcsinh((img - mu) / sigma) + 0.2
    plot_scene = asinh(new_scene, 0.0, scene_sigma, 0.15)
    plot_data = asinh(data, sky, data_sigma, 0.2)
    plot_predicted = asinh(predicted, 0.0, data_sigma, 0.2)

    # Set up which data will go in which panel.
    norm = np.sum(dpsf)
    panels = [
        [("Scene", plot_scene, [0, 1]),
         ("PSF", dpsf),
         (r"$\mathrm{d}\ell / \mathrm{d} s$", dlds)],
        [("Predicted", plot_predicted, [0, 1]),
         ("Data", plot_data, [0, 1]),
         ("annotations", None)]]

    # Do the plotting.
    size = data.shape[0]  # The size to pad/crop to.
    for i, (ri, ci) in enumerate(itertools.product(range(rows), range(cols))):
        ax = axes[i]
        panel = panels[ri][ci]
        title, content = panel[0], panel[1]
        if len(panel) > 2:
            vrange = panel[2]
        else:
            vrange = None

        if content is not None:
            plot_image(ax, content, size=size, vrange=vrange)
            ax.set_title(title)
        elif title == "annotations":
            # Put some stats in this axis.
            line_height = 0.13
            txt = meta
            txt.append("Sky: {0:0.4f}".format(sky))
            txt.append(r"$\sum \mathrm{{dPSF}} = {0:.4f}$"
                    .format(norm))
            txt.append("median(Data) = {0:.4f}".format(data_median))
            txt.append("median(New Scene) = {0:.4f}"
                    .format(scene_median))

            for i in range(len(txt)):
                ax.text(0, 1 - i * line_height, txt[i], ha="left", va="top",
                        transform=ax.transAxes)

            ax.set_axis_off()
        else:
            ax.set_axis_off()
