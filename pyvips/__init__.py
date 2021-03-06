import logging
import os
import sys
import atexit

# flake8: noqa

from cffi import FFI

logger = logging.getLogger(__name__)

# user code can override this null handler
logger.addHandler(logging.NullHandler())

ffi = FFI()

_is_windows = os.name == 'nt'
_is_mac = sys.platform == 'darwin'
_is_64bits = sys.maxsize > 2 ** 32

# yuk
if _is_windows:
    _glib_libname = 'libglib-2.0-0.dll'
    _gobject_libname = 'libgobject-2.0-0.dll'
    _vips_libname = 'libvips-42.dll'
elif _is_mac:
    _glib_libname = None
    _vips_libname = 'libvips.42.dylib'
    _gobject_libname = 'libgobject-2.0.dylib'
else:
    _glib_libname = None
    _vips_libname = 'libvips.so'
    _gobject_libname = 'libgobject-2.0.so'

# possibly use ctypes.util.find_library() to locate the lib?
gobject_lib = ffi.dlopen(_gobject_libname)
vips_lib = ffi.dlopen(_vips_libname)
if _glib_libname:
    glib_lib = ffi.dlopen(_glib_libname)
else:
    glib_lib = gobject_lib

logger.debug('Loaded lib %s', vips_lib)
logger.debug('Loaded lib %s', gobject_lib)

# GType is an int the size of a pointer ... I don't think we can just use
# size_t, sadly
if _is_64bits:
    ffi.cdef('''
        typedef uint64_t GType;
    ''')
else:
    ffi.cdef('''
        typedef uint32_t GType;
    ''')

from .error import *

# redirect all vips warnings to logging

ffi.cdef('''
    typedef void (*GLogFunc) (const char* log_domain,
        int log_level,
        const char* message, void* user_data);
    int g_log_set_handler (const char* log_domain,
        int log_levels,
        GLogFunc log_func, void* user_data);

    void g_log_remove_handler (const char* log_domain, int handler_id);

''')

class GLogLevelFlags(object):
    # log flags 
    FLAG_RECURSION          = 1 << 0
    FLAG_FATAL              = 1 << 1

    # GLib log levels 
    LEVEL_ERROR             = 1 << 2       # always fatal 
    LEVEL_CRITICAL          = 1 << 3
    LEVEL_WARNING           = 1 << 4
    LEVEL_MESSAGE           = 1 << 5
    LEVEL_INFO              = 1 << 6
    LEVEL_DEBUG             = 1 << 7

def _log_handler(domain, level, message, user_data):
    if level == GLogLevelFlags.LEVEL_WARNING: 
        logger.warning('{0}: {1}'.format(_to_string(ffi.string(domain)), 
                                         _to_string(ffi.string(message))))

# keep a ref to the cb to stop it being GCd
_log_handler_cb = ffi.callback('GLogFunc', _log_handler)
_log_handler_id = glib_lib.g_log_set_handler(_to_bytes('VIPS'), 
                           GLogLevelFlags.LEVEL_WARNING | 
                           GLogLevelFlags.FLAG_FATAL | 
                           GLogLevelFlags.FLAG_RECURSION,
                           _log_handler_cb, ffi.NULL)

# we must remove the handler on exit or libvips may try to run the callback
# during shutdown
def _remove_log_handler():
    glib_lib.g_log_remove_handler(_to_bytes('VIPS'), _log_handler_id)

atexit.register(_remove_log_handler)

ffi.cdef('''
    int vips_init (const char* argv0);
''')

if vips_lib.vips_init(_to_bytes(sys.argv[0])) != 0:
    raise Error('unable to init libvips')

logger.debug('Inited libvips')
logger.debug('')

from .enums import *
from .base import *
from .gobject import GObject
from .gvalue import GValue
from .vobject import VipsObject
from .vinterpolate import Interpolate
from .voperation import Operation
from .vimage import Image

__all__ = [
    'Error', 'Image', 'Operation', 'GValue', 'Interpolate', 'GObject',
    'VipsObject', 'type_find', 'type_name'
]
