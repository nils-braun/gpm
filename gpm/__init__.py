from gpm.instances.instance import ListInstance, GitInstance
from gpm.manager import GPM


# TODO: Later it should not be allowed to set the externals etc. from python, but only via config file
def gpm(base_dir=".", externals=None):
    # As a default, use the current folder as a single git external
    if externals is None:
        externals = ListInstance([GitInstance(".")])
    else:
        externals = ListInstance([GitInstance(external) for external in externals])

    return GPM(base_dir, externals)
