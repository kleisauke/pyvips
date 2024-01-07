set -xe

# Download and install vips
basedir=$(python download-vips.py)

if [[ $RUNNER_OS == "Linux" ]]; then
  linkname="-l:libvips.so.42"
elif [[ $RUNNER_OS == "Windows" ]]; then
  # MSVC convention: import library is called "libvips.lib"
  linkname="-llibvips"
  # GLib is compiled as a shared library in the "-static-ffi" variant
  linkname+=" -llibglib-2.0 -llibgobject-2.0"
elif [[ $RUNNER_OS == "macOS" ]]; then
  # -l:<LIB> syntax is unavailable with ld on macOS
  ln -sf libvips.42.dylib $basedir/lib/libvips.dylib
  # Allow delocate to find @loader_path/libvips.42.dylib
  cp -f $basedir/lib/libvips.42.dylib /usr/local/lib
  linkname="-lvips"
fi

mkdir -p $basedir/lib/pkgconfig
cat > $basedir/lib/pkgconfig/vips.pc << EOL
prefix=${basedir}
libdir=\${prefix}/lib
includedir=\${prefix}/include

Name: vips
Description: Image processing library
Version: 8.15.0
Requires:
Libs: -L\${libdir} ${linkname}
Cflags: -I\${includedir} -I\${includedir}/glib-2.0 -I\${libdir}/glib-2.0/include
EOL
