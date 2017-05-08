INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_PMT_CPP pmt_cpp)

FIND_PATH(
    PMT_CPP_INCLUDE_DIRS
    NAMES pmt_cpp/api.h
    HINTS $ENV{PMT_CPP_DIR}/include
        ${PC_PMT_CPP_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    PMT_CPP_LIBRARIES
    NAMES gnuradio-pmt_cpp
    HINTS $ENV{PMT_CPP_DIR}/lib
        ${PC_PMT_CPP_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(PMT_CPP DEFAULT_MSG PMT_CPP_LIBRARIES PMT_CPP_INCLUDE_DIRS)
MARK_AS_ADVANCED(PMT_CPP_LIBRARIES PMT_CPP_INCLUDE_DIRS)

