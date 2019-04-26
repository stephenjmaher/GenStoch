import sys
import os.path
import instancegen as ig

if __name__ == "__main__":
   # printing the help message
   if (len(sys.argv) == 2 and sys.argv[1] == "--help")\
         or len(sys.argv) < 4 or len(sys.argv) == 1:
      print("Usage: %s instance-class instance-name numscenarios [type]"%sys.argv[0])
      print("  instance-class : the instance class. Available classes (%s)"%", ".join(map(str, ig.instances.keys())))
      print("  instance-name  : the name of the instance (without extension)")
      print("  numscenarios   : the number of scenarios to generate")
      print("  type           : the type of stochasticity. Available types (%s) (default %s)"\
                  %(", ".join(map(str, ig.STOCH_TYPES)), str(ig.STOCH_TYPES[0])))
      exit(1)

   print("Arguments:", sys.argv)

   instanceclass = sys.argv[1]
   instancename = sys.argv[2]
   extensions = ["cor", "tim"]
   numscenarios = sys.argv[3]
   stochtype = ig.STOCH_RHS
   if len(sys.argv) == 5:
      stochtype = int(sys.argv[4])

   # verifying the inputs for the script
   if not ig.validInputs(instanceclass, instancename, extensions, numscenarios,
         stochtype):
      exit(1)

   # initialising the instance
   instance = ig.instances[instanceclass](
         "%s.cor"%(instancename),"%s.tim"%(instancename),
         "%s_%s.sto"%(instancename, numscenarios))

   # reading the instance core and time-stages files
   instance.readInstance(readCor = True, readTim = True)

   # writing the stochastic file
   instance.writeStoFile(int(numscenarios), stochtype)

   # writing the SMPS file (used by SCIP).
   instance.writeSmpsFile()
