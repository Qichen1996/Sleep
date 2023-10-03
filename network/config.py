import numpy as np
from utils import dB2lin, lin2dB

renderMode = 'none'

# base station params
numBS = 19
interBSDist = 400  # the distance between two adjacent BSs
# cellRadius = 750  # the radius of a hexagon cell in meters
txPower = 0.2  # average transmit power per antenna in watts
maxPAPower = 3  # maximum antenna power in watts
fixedPC = 18  # load-independent power consumption in watts
bsFrequency = 5e9  # carrier frequency in Hz
# feederLoss = 1  # feeder loss in dB (XXX: include in antennaGain)
# antennaGain = 19 - feederLoss  # power gain in dB of each antenna of a BS
signalThreshold = 2e-12  # signal threshold in watts
maxAntennas = 64  # max number of antennas
minAntennas = 16  # min number of antennas
bandWidth = 10e6  # communication bandwidth in Hz
bsHeight = 25  # height of a BS in meters
# powerAllocWeights = [95, 4, 1]  # weights of the power allocation
powerAllocBase = 2.
antennaSwitchOpts = [-4, 0, 4]
sleepModeDeltas = [1, 0.69, 0.50, 0.29]
wakeupDelays = [0, 1e-3, 1e-2, 1e-1]
antSwitchEnergy = 0.01  # energy consumption of switch per antenna in Joules
sleepSwitchEnergy = [0.02, 0.01, 0.01, 0.01]  # energy consumption of switching sleep mode in Joules
disconnectEnergy = 0.01  # energy consumption of a disconnection (before UE is done) in Joules
bufferShape = (50, 1)  # shape of the buffer used to record past observations
bufferChunkSize = 50  # chunk size to apply average pooling
bufferNumChunks = bufferShape[0] // bufferChunkSize

# channel model params
noiseSpectralDensity = dB2lin(-174 - 30 + 7)
# thermal noise variance

# user equipment params
ueHeight = 1.5  # height of a UE in meters

# default network configuration
areaSize = np.array([2.5, 2.5]) * interBSDist * 2
bsPositions_inner = np.vstack([
    [areaSize / 2],
    np.array(
        [[areaSize[0]/2 + interBSDist * np.cos(a + np.pi/6),
          areaSize[1]/2 + interBSDist * np.sin(a + np.pi/6)]
         for a in np.linspace(0, 2*np.pi, 6, endpoint=False)]),
])
r = interBSDist * 2
l = r * np.sin(np.pi/3)
bsPositions = np.vstack([
    bsPositions_inner,
    np.array([[areaSize[0]/2 + r * np.cos(a + np.pi/6), areaSize[1]/2 + r * np.sin(a + np.pi/6)] for a in np.linspace(0, 2*np.pi, 6, endpoint=False)]),
    np.array([[areaSize[0]/2 + l * np.cos(a), areaSize[1]/2 + l * np.sin(a)] for a in np.linspace(0, 2*np.pi, 6, endpoint=False)])
])
probeGridSize = 20

# obs names
public_obs_keys = ['pc', 'num_antennas', 'responding', 'sleep_mode']
hist_stats_keys = ['arrival_rate']
ue_groups = ['covered', 'serving', 'queued', 'idle']
ue_stats_keys = ['num', 'sum_rate', 'sum_rate_req', 'sum_tx_power', 'num_urgent']
private_obs_keys = ['next_sleep_mode', 'wakeup_time',
                    *[f'{k}{i}' for i in range(-bufferNumChunks, 0) for k in hist_stats_keys],
                    *[f'{u}_{k}' for u in ue_groups for k in ue_stats_keys]]
mutual_obs_keys = ['dist', *ue_stats_keys]
other_obs_keys = [f'nb{i}_{k}' for i in range(6) for k in public_obs_keys + mutual_obs_keys]
all_obs_keys = public_obs_keys + private_obs_keys + other_obs_keys
