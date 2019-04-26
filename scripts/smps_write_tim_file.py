import sys
import os.path
import instancegen as ig

if __name__ == "__main__":
   # printing the help message
   if (len(sys.argv) == 2 and sys.argv[1] == "--help")\
         or len(sys.argv) < 3 or len(sys.argv) == 1:
      print("Usage: %s instance-class instance-name"%sys.argv[0])
      print("  instance-class : the instance class. Available classes (%s)"%", ".join(map(str, ig.instances.keys())))
      print("  instance-name  : the name of the instance (without extension)")
      exit(1)

   print("Arguments:", sys.argv)

   instanceclass = sys.argv[1]
   instancename = sys.argv[2]
   extensions = ["cor"]

   # verifying the inputs for the script
   if not ig.validInputs(instanceclass, instancename, extensions):
      exit(1)

   # initialises the instance given the instance class
   instance = ig.instances[instanceclass](
         "%s.cor"%(instancename),"%s.tim"%(instancename))

   # reads the core file to store the constraint and variable names
   instance.readInstance(readCor = True)

   # writes the stages (.tim) file
   instance.writeTimFile()
