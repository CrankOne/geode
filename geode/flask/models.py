from flask_shelve import get_shelve

class GeometriesStorageInterface(object):
    """Interfaces setup's persistent storage"""
    def __init__(self):
        pass

    def create(self, data):
        """Creates new setup in storage, returns its ID"""
        raise NotImplementedError('Creation of new setup.')

    def get(self, setupID):
        """Returns setup data by its ID."""
        raise NotImplementedError('Retrieving a setup.')

    def setup_exists(self, setupID):
        """Returns, whether the setup with this ID exists."""
        raise NotImplementedError('Lookup for a setup.')

    def wipe(self, setupID):
        """Removes setup with ID returning whether or not it existed."""
        raise NotImplementedError('Remove a setup.')

    def list(self):
        """Returns list of available setups"""
        raise NotImplementedError('List setups.')
