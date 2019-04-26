"""
The MIT License (MIT)

@author: Stephen J. Maher
"""
import os.path
from .smps_instance import *
from .smps_instance_classes import *

instances = {
      "rrtailassign" : RRTailAssignInstance,
      "sslp" : SSLPInstance,
      "noswot" : NoswotInstance,
      "snip" : SnipInstance,
      }

def validInputs(instanceclass, instancename, extensions = ["cor"],
      numscenarios = None, stochtype = None):
   '''
   verifies whether the inputs are valid. All inputs are checked, so that the
   warning message is returned for any error.

   Parameters
   ----------
   instanceclass : string
      the name of the instance class
   instancename : string
      the basename for the instance (no extension)
   extensions : list of strings. Default ["cor"]
      a list of the extensions for the necessary files
   numscenarios : int
      the number of scenarios that will be generated
   stochtype : string
      the stochasticity type

   Returns
   -------
   bool
      True if all inputs are valid, False otherwise
   '''
   valid = True
   valid = validInstanceClass(instanceclass) and valid
   valid = validInstanceFiles(instancename, extensions) and valid
   if numscenarios is not None:
      valid = validNumScenarios(numscenarios) and valid
   if stochtype is not None:
      valid = validStochasticityType(stochtype) and valid

   return valid

def validInstanceClass(instanceclass):
   '''
   verifies that the instance class is valid

   Parameters
   ----------
   instanceclass : string
      the name of the instance class

   Returns
   -------
   bool
      True if the class exists, False otherwise
   '''
   if instanceclass not in instances.keys():
      print("   ERROR: Instance class <%s> is invalid. Available instance classes (%s)"\
            %(instanceclass, ", ".join(map(str, instances.keys()))))
      return False

   return True

def validInstanceFiles(instancename, extensions = ["cor"]):
   '''
   verifies whether the necessary files associated with the instancename exist.
   The necessary files are given by the extensions.

   Parameters
   ----------
   instancename : string
      the basename for the instance (no extension)
   extensions : list of strings. Default ["cor"]
      a list of the extensions for the necessary files

   Returns
   -------
   bool
      True if the all necessary files exists, False otherwise
   '''
   for ext in extensions:
      if not os.path.isfile("%s.%s"%(instancename, ext)):
         print("   ERROR: <%s.%s> must exist. Please input a valid instance name."\
               %(instancename, ext))
         return False

   return True

def validNumScenarios(numscenarios):
   '''
   verifies whether the number of scenarios is greater than 0

   Parameters
   ----------
   numscenarios : int
      the number of scenarios that will be generated

   Returns
   -------
   bool
      True if the number of scenarios is greater than 0, False otherwise
   '''
   if int(numscenarios) <= 0:
      print("   ERROR: Number of scenarios must be greater than 0.")
      return False

   return True

def validStochasticityType(stochtype):
   '''
   verifies that a valid stochasticity type is input

   Parameters
   ----------
   stochtype : string
      the stochasticity type

   Returns
   -------
   bool
      True if the stochasticity type is valid, False otherwise
   '''
   if stochtype not in STOCH_TYPES:
      print("   ERROR: Stochasicity type <%s> is invalid. Available stochasticity "\
            "types (%s) (default %s)"\
            %(stochtype, ", ".join(map(str, STOCH_TYPES)), str(STOCH_TYPES[0])))
      return False

   return True

