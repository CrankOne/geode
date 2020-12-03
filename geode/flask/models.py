import copy

class Model(object):
    """
    Defines a data model interface for geometry setups.
    """
    def __init__(self, common, setups):
        self.common = copy.deepcopy(common)
        self.setups = setups

    def __setitem__(self, ID, payload):
        raise NotImplementedError('Adding geometries is not yet implemented.')

    def asdict(self, ID, client):
        """
        Returns common+setup configuration
        """
        return { **self.common, **self.setups[ID], **client )

