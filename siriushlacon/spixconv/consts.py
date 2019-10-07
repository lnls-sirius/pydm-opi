import pkg_resources

def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)

SPIXCONV_MAIN = get_abs_path('ui/main.ui')