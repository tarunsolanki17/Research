""" Caches with options for a simple gem5 configuration script

This file contains L1 I/D and L2 caches to be used in the simple
gem5 configuration script. It uses the options wrapper to set up command
line options from each individual class.
"""

from m5.objects import BaseCache
from m5 import fatal

import options

# Some specific options for caches
# For all options see src/mem/cache/BaseCache.py

class L1Cache(BaseCache):
    """Simple L1 Cache with default values"""

    assoc = 2
    hit_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    is_top_level = True

    def __init__(self, options=None):
        super(L1Cache, self).__init__()
        pass

    def connectCPU(self, cpu_port):
        """"Connect this cache's port to a CPU port"""
        self.cpu_side = cpu_port

    def connectBus(self, bus):
        """"Connect this cache to a memory-side bus"""
        self.mem_side = bus.slave

class L1ICache(L1Cache):
    """Simple L1 instruction cache with default values"""

    # Set the default size
    size = '16kB'

    options.add_option('--l1i_size', 
                       help="L1 instruction cache size. Default: %s" % size)

    def __init__(self, opts=None):
        super(L1ICache, self).__init__(opts)
        if not opts or not opts.l1i_size:
            return
        self.size = opts.l1i_size

class L1DCache(L1Cache):
    """Simple L1 data cache with default values"""

    # Set the default size
    size = '32kB'
    assoc = 8

    options.add_option('--replacement_policy',
                       help="L1 cache replacement policy. [PLRU,NMRU,Random]")

    options.add_option('--l1d_size', 
                       help="L1 data cache size. Default: %s" % size)

    options.add_option('--l1d_assoc',
                       help="L1 data cache associativity. Default: %s" % assoc)

    def __init__(self, opts=None):
        super(L1DCache, self).__init__(opts)
        if not opts:
            return

        if opts.l1d_size:
            self.size = opts.l1d_size

        if opts.l1d_assoc:
            self.assoc = opts.l1d_assoc

        if opts.replacement_policy == "PLRU":
            from m5.objects import PLRU
            self.tags = PLRU()
        elif opts.replacement_policy == "NMRU":
            from m5.objects import NMRU
            self.tags = NMRU()
        elif opts.replacement_policy == "Random":
            from m5.objects import RandomRepl
            self.tags = RandomRepl()
        elif opts.replacement_policy:
            fatal("Unsupported replacement policy: %s" % opts.replacement_policy)

class L2Cache(BaseCache):
    """Simple L2 Cache with default values"""

    # Default parameters
    size = '256kB'
    assoc = 8
    hit_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    options.add_option('--l2_size', help="L2 cache size. Default: %s" % size)

    def __init__(self, opts=None):
        super(L2Cache, self).__init__()
        if not opts or not opts.l2_size:
            return
        self.size = opts.l2_size

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.master

    def connectMemSideBus(self, bus):
        self.mem_side = bus.slave

