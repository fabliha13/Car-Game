'''OpenGL extension EXT.EGL_sync

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.EGL_sync to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension extends EGL_KHR_fence_sync with client API support for
	OpenGL (compatibility or core profiles) as an EXT extension.
	
	The "GL_EXT_EGL_sync" string indicates that a fence sync object can be
	created in association with a fence command placed in the command stream
	of a bound OpenGL context.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/EGL_sync.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.EXT.EGL_sync import *
from OpenGL.raw.GL.EXT.EGL_sync import _EXTENSION_NAME

def glInitEglSyncEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION