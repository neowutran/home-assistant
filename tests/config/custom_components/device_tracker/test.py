"""
config.custom_components.device_tracker.test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provides a mock device scanner.
"""


def get_scanner(hass, config):
    """ Returns a mock scanner. """
    return SCANNER


class MockScanner(object):
    """ Mock device scanner. """

    def __init__(self):
        """ Initialize the MockScanner. """
        self.devices_home = []

    def come_home(self, device):
        """ Make a device come home. """
        self.devices_home.append(device)

    def leave_home(self, device):
        """ Make a device leave the house. """
        self.devices_home.remove(device)

    def reset(self):
        """ Resets which devices are home. """
        self.devices_home = []

    def scan_devices(self):
        """ Returns a list of fake devices. """

        return list(self.devices_home)

    def get_device_name(self, device):
        """
        Returns a name for a mock device.
        Returns None for dev1 for testing.
        """
        return None if device == 'DEV1' else device.lower()

SCANNER = MockScanner()
