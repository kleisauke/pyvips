#!/bin/bash

set -e

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    sw_vers

    brew update

    # install gcc
    # if there are conflicts, try overwriting the files
    # (these are in /usr/local anyway so it should be ok)
    brew install gcc || brew link --overwrite gcc

    # install optional add-ons for libvips
    brew install cfitsio libmatio

    # FIXME:
    # Excluding GObject Introspection (`--without-gobject-introspection`),
    # Python (`--without-python`) and PyGObject (`--without-pygobject3`)
    # is currently not possible because those dependencies don't have
    # a `=> :recommended` tag (it's a hard dependency currently).

    # install libvips (full-fat version)
    brew install vips \
      --env=std \
      --with-imagemagick \
      --with-mozjpeg \
      --with-openexr \
      --with-openslide \
      --with-webp \
      --without-python \
      --without-pygobject3 \
      --without-gobject-introspection
else
    uname -a

    # the vips7 py binding won't work with pypy, make sure it's off
    . $TRAVIS_BUILD_DIR/.travis/install-vips.sh \
      --disable-debug \
      --disable-dependency-tracking \
      --disable-introspection \
      --disable-static \
      --enable-gtk-doc-html=no \
      --enable-gtk-doc=no \
      --enable-pyvips8=no \
      --without-python
fi