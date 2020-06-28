#!/usr/bin/python3
# -*- mode: python; coding: utf-8 -*-

from bluetooth.ble import BeaconService
from pathlib import Path
import sys
import time
from uuid import uuid1
import yaml

# Default configuration
DEFAULT_CONFIG = {
    'scanner': {
        'timeout': None,
        'revisit': 1,
        'filters': {}
        }
    }

# Universal settings
BLE_DEVICE = "hci0"
CONTROL_INTERVAL = 1 # (s)
MAX_TIMEOUT = 600 # (s)

INTERVAL_LIMITS = [20, 10000] # (ms)

class Scanner(object):

    def __init__(self, **kwargs):
        """Instance initialization.

        Args:
            logger (logging.Logger): Configured logger.
            **kwargs: Keyword arguments corresponding to instance attributes. 
                Any unassociated keyword arguments are ignored.
        """
        # Beacon settings
        for key, value in DEFAULT_CONFIG['scanner'].items():
            if key in kwargs and kwargs[key]:
                setattr(self, key, kwargs[key])
        # Create beacon
        self.__service = BeaconService(BLE_DEVICE)
        self.__timeout = None
    
    @property
    def timeout(self):
        """BLE beacon scanner timeout getter."""
        return self.__timeout
    
    @timeout.setter
    def timeout(self, value):
        """BLE beacon scanner timeout setter.

        Raises:
            TypeError: Beacon scanner timeout must be a float, integer, or 
                NoneType.
            ValueError: Beacon scanner timeout must be strictly positive.
            ValueError: Beacon scanner cannot exceed maximum allowable timeout.
        """
        if value is not None:
            if not isinstance(value, (float, int)):
                raise TypeError("Beacon scanner timeout must be a float, "
                        "integer, or NoneType.")
            elif value <= 0:
                raise ValueError("Beacon scanner timeout must be strictly "
                        "positive.")
            elif value > MAX_TIMEOUT:
                raise ValueError("Beacon scanner timeout cannot exceed "
                        "maximum allowable timeout.")
        self.__timeout = value
    
    @property
    def revisit(self):
        """BLE beacon scanner revisit interval getter."""
        return self.__revisit

    @revisit.setter
    def revisit(self, value):
        """BLE beacon scanner revisit interval setter.

        Raises:
            TypeError: Beacon scanner revisit interval must be an integer.
            ValueError: Beacon scanner revisit interval must be strictly 
                positive.
         """
        if not isinstance(value, int):
            raise TypeError("Beacon scanner revisit interval must be an "
                    "integer.")
        elif value <= 0:
            raise ValueError("Beacon scanner revisit interval must strictly "
                    "positive.")
        self.__revisit = value
    
    def scan(self, scan_prefix='', timeout=0, revisit=1):
        """Execute BLE beacon scan.
            
        Returns:
            Filtered advertisements by address 
            first, timestamp second, and then remainder of advertisement 
            payload, e.g., UUID, major, minor, etc.
        """
        # Parse inputs
        if timeout == 0:
            timeout = self.timeout
        # Start advertising
        run = True        
        scan_count = 0
        start_time = time.monotonic()
        advertisements = []
        while run:
            scan_count += 1
            scans = []
            scans.append(self.__service.scan(self.revisit))
            print(scans[-1])
            if timeout is not None:
                if (time.monotonic()-start_time) > timeout:
                    run = False
    
def load_config(parsed_args):
    """Load configuration."""
    config = DEFAULT_CONFIG
    return config
    
def main(args):
    """Creates beacon and starts scanning.
    
    Returns:
        scanned advertisements are returned
    """
    # Create and start beacon advertiser or scanner
    scanner = Scanner(**DEFAULT_CONFIG['scanner'])
    advertisements = scanner.scan()
    output = advertisements
    return output
    
if __name__ == "__main__":
    """Script execution."""
    main(sys.argv)
    
