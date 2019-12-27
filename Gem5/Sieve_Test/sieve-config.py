import m5
from m5.objects import *
from caches import *
from optparse import OptionParser

#------------Command line parameters options added------------------------------------------------------------------

parser = OptionParser()
parser.add_option('--l1i_size', help="L1 Instruction cache size")
parser.add_option('--l1d_size', help="L1 Data cache size")
parser.add_option('--l2_size', help="Unified L2 cache size")
parser.add_option('--clock_frequency', help="Clock frequency of the CPU")

(options, args) = parser.parse_args()

#-------------------------------------------------------------------------------------------------------------------
system = System()

system.clk_domain = SrcClockDomain()
if not options or not options.clock_frequency:
    system.clk_domain.clock = '1GHz'                                    # Setting Clock Frequency
else:    
    system.clk_domain.clock = options.clock_frequency
system.clk_domain.voltage_domain = VoltageDomain()                      # Setting Volatage 

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

                                          
system.cpu = TimingSimpleCPU()                                        # CPU Model                 

system.cpu.icache = L1ICache(options)                                   # L1 Inst. Cache
system.cpu.dcache = L1DCache(options)                                   # L1 Data Cache

system.cpu.icache.connectCPU(system.cpu)                                # Connecting with CPU
system.cpu.dcache.connectCPU(system.cpu)

system.l2bus = L2XBar()                                                 # L2 Cache Bus

system.cpu.icache.connectBus(system.l2bus)                              # Connecting ICache with L2 Cache Bus
system.cpu.dcache.connectBus(system.l2bus)                              # Connecting DCache with L2 Cache Bus

system.membus = SystemXBar()                                            # Memory Bus

system.l2cache = L2Cache(options)                                       # Init L2 Cache
system.l2cache.connectCPUSideBus(system.l2bus)                          # Connecting L2 Cache to L2 Bus

system.l2cache.connectMemSideBus(system.membus)                         # Connecting L2 Cache to Memory Bus

#Port Abstraction - Each memory object can have two kinds of ports - master and slave.
#memobject1.master = memobject2.slave	# connecting master port to slave port

#Create an IO Controller on the CPU and connect it to the memory bus.
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.slave

#Create a memory controller to connect it to the membus.
system.mem_ctrl = DDR3_1600_8x8()                                # Memory Controller
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Set up a process for the CPU to execute
process = Process()
process.cmd = ['tests/test-progs/SieveOfEratosthenes/a.out']
system.cpu.workload = process
system.cpu.createThreads()

# Instantiate the system and begin the execution
root = Root(full_system = False, system = system)
m5.instantiate()

print ("Beginning Simulation!")
exit_event = m5.simulate()

#Once simulation finishes we can inspect the state of the system.
print ('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))
