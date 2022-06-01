# Example 2 from: https://stackoverflow.com/questions/21259070/struggling-to-append-a-relative-path-to-my-sys-path
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'src')) # If src code is moved, the path input must be changed here

from Building import Building
from Elevator import Elevator
from ElevatorAlgorithm import ElevatorAlgorithm
from Floor import Floor
from Person import Person
import Schedule
import Simulation
import constants