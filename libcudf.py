from ctypes import *

class QCDCL(object):
    __lib = None
    __LIB_NAME = 'libcudf.so*'

    def __load_libs(self):
        if not self.__lib:
            if self.__lib_path:
                if path.isabs(self.__lib_path):
                    module_path = self.__lib_path
                else:
                    module_path = path.realpath('%s/%s' % (path.dirname(__file__), self.__lib_path))
            else:
                module_path = path.dirname(__file__)

            self.__lib_path = '%s/%s' % (module_path, self.__LIB_NAME)
            logging.info('Loading library from path=%s', self.__lib_path)
            libs = glob(self.__lib_path)
            logging.info('Found the following matching libs=%s', libs)
            assert (sum(1 for _ in libs) == 1)
            self.__LIB_NAME = libs[0]
            logging.debug('Shared Lib: Loading...')
            logging.debug('Shared Lib: %s', self.__LIB_NAME)
            self.__lib = cdll.LoadLibrary(self.__LIB_NAME)

    def __init__(self, lib_path=None):
        logging.debug('libcudf: Initializing...')
        self.__lib_path = lib_path
        self.__load_libs()
        #qdpll_create = self.__lib.qdpll_create
        #qdpll_create.restype = QDPLL_P
        #self.__depqbf = qdpll_create()
        logging.debug('libcudf: Initialized')

#/* Call cudf_init() before doing anything else with libCUDF. (Or you will get a
# * segfault, you've been warned.) */
#void cudf_init();

    def cudf_parse_from_file(self, filename):
        "Parse a CUDF document from file, without doing any further processing."
        #cudf_doc_t *cudf_parse_from_file(char *fname);

    def cudf_load_from_file(self, filename):
        """Load a CUDF document from file, i.e. parse it and then store the contained
        packages as an universe structure.
        
        Note: to load solutions you should prefer cudf_load_solution_from_file,
        which can be invoked after CUDF document loading."""
        #cudf_t *cudf_load_from_file(char *fname);


/* Get dependencies of a package */
cudf_vpkgformula_t cudf_pkg_depends(cudf_package_t pkg);

/* Get conflicts of a package */
cudf_vpkglist_t cudf_pkg_conflicts(cudf_package_t pkg);

/* Get provided features of a package */
cudf_vpkglist_t cudf_pkg_provides(cudf_package_t pkg);

/* Get extra properties of a package. */
cudf_extra_t cudf_pkg_extra(cudf_package_t pkg);

    #def configure(self, *args):
    #    logging.debug('QCDCL: Configure Parameter')
    #    for e in args:
    #        logging.info('Parameter "%s"', e)
    #        configure = self.__lib.qdpll_configure
    #        configure.restype = c_char_p
    #        ret = configure(self.__depqbf, e)
    #        if ret:
    #            raise ValueError, "%s:%s" % (ret, e)
