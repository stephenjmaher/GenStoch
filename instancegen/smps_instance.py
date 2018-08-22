import numpy as np

RHS = "RHS"
ROWS = "ROWS"
COLUMNS = "COLUMNS"
PERIODS = "PERIODS"

class Instance:
   def __init__(self, corfile = None, timfile = None, stofile = None):
      self.corfile = corfile
      self.timfile = timfile
      self.stofile = stofile;
      self.constraints = []
      self.variables = []
      self.coeffs = {}
      self.rhs = {}
      self.periods = []

      self.readCorFile()
      self.readTimFile()

   def readCorFile(self):
      '''
      reads a COR file for an SMPS instance
      '''
      assert self.corfile is not None
      with open(self.corfile, "rb") as infile:
         while True:
            line = infile.readline()
            if not line: break

            # if the line does not start with a space, then we are in a new
            # section
            if not line.startswith(" "):
               section = None

            # reading each line and storing the important information
            if line.startswith(ROWS):
               section = ROWS
            if line.startswith(COLUMNS):
               section = COLUMNS
            if line.startswith(RHS):
               section = RHS

            if line.startswith(" "):
               if section == ROWS:
                  self.storeConstraints(line)
               if section == COLUMNS:
                  self.storeVariables(line)
               if section == RHS:
                  self.storeConsRhs(line)

   def readTimFile(self):
      '''
      reads a TIM file for an SMPS instance
      '''
      assert self.timfile is not None
      with open(self.timfile, "rb") as infile:
         while True:
            line = infile.readline()
            if not line: break

            # if the line does not start with a space, then we are in a new
            # section
            if not line.startswith(" "):
               section = None

            # reading each line and storing the important information
            if line.startswith(PERIODS):
               section = PERIODS

            if line.startswith(" "):
               if section == PERIODS:
                  self.storePeriods(line)

   def readStoFile(self):
      '''
      reads a STO file for an SMPS instance
      '''
      pass

   def writeStoFile(self, nscenarios, stochtype = STOCH_RHS):
      '''
      writes an STO file
      '''
      assert self.stofile is not None
      np.random.seed(1)
      with open(self.stofile, 'w') as outfile:
         # writing the header of the STO file
         outfile.write("STOCH\n")
         outfile.write("SCENARIOS     DISCRETE\n")

         if stochtype == STOCH_RHS:
            self.writeRhsStochasticFile(outfile, nscenarios)
         elif stochtype == STOCH_COEF:
            self.writeCoefStochasticFile(outfile, nscenarios)
         elif stochtype == STOCH_OBJ:
            self.writeObjStochasticFile(outfile, nscenarios)

         outfile.write("ENDATA")

   def writeSmpsFile(self):
      '''
      writes the SMPS file for the generated problem
      '''
      smpsfile = "%s.smps"%(self.stofile.split('.')[0])
      with open(smpsfile, 'w') as outfile:
         outfile.write("%s\n"%self.corfile)
         outfile.write("%s\n"%self.timfile)
         outfile.write("%s\n"%self.stofile)





   def storeConstraints(self, line):
      '''
      stores the constraints of the problem
      '''
      linelist = line.split()
      if linelist[0] != 'N':
         # storing the constraint name as the key of the dictionary. The
         # constraints are initials given an rhs of 0
         self.constraints.append(linelist[1])

   def storeVariables(self, line):
      '''
      stores the variables of the problem
      '''
      # if the INTSTART or INTEND keywords are found, then we exit the function
      if "INTSTART" in line or "INTEND" in line:
         return

      linelist = line.split()
      # if the variables array is empty or the new variable name differs from
      # the last stored name, then we store the variable
      if len(self.variables) == 0 or linelist[0] != self.variables[-1]:
         self.variables.append(linelist[0])

      self.coeffs[linelist[0], linelist[1]] = float(linelist[2])

      if len(linelist) == 5:
         self.coeffs[linelist[0], linelist[3]] = float(linelist[4])



   def storeConsRhs(self, line):
      '''
      stores the RHS for constraints given by the line
      '''
      linelist = line.split()

      self.rhs[linelist[1]] = float(linelist[2])

      # the line list will be of length 5 if there are two RHS
      if len(linelist) == 5:
         self.rhs[linelist[3]] = float(linelist[4])

   def storePeriods(self, line):
      '''
      stores the periods for the variables and constraints
      '''
      linelist = line.split()

      self.periods.append([linelist[2], linelist[0], linelist[1]])

   def writeRhsStochasticFile(self, outfile, nscenarios):
      '''
      writes the scenarios with RHS stochasticity
      '''
      pass

   def writeCoefStochasticFile(self, outfile, nscenarios):
      '''
      writes the scenarios with coefficient stochasticity
      '''
      pass

   def writeObjStochasticFile(self, outfile, nscenarios):
      '''
      writes the scenarios with coefficient stochasticity
      '''
      pass
