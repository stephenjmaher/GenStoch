import numpy as np
from .smps_instance import Instance

class RRTailAssignInstance(Instance):
   '''
   SMPS output functions for the recoverable robustness tail assignment problem
   '''

   def writeCoefStochasticFile(self, outfile, nscenarios):
      '''
      writes the scenarios with coefficient stochasticity
      '''
      # storing the first stage RHS to compute the standard deviationi
      stage = 0
      secondstagecons = []
      for cons in self.constraints:
         if cons == self.periods[1][2]:
            stage += 1

         if stage == 1:
            secondstagecons.append(cons)

      secondstagevars = []
      stage = 0
      for var in self.variables:
         if var == self.periods[1][1]:
            stage += 1

         if stage == 1:
            secondstagevars.append(var)

      # writing the scenarios to the STO file
      weight = 1.0/float(nscenarios)
      for i in range(nscenarios):
         outfile.write(" SC SCEN%d      ROOT         %g        %s        0.0\n"%(i + 1, weight, self.periods[1][0]))
         for cons in secondstagecons:
            if cons.startswith("RecoveryFlight"):
               for var in secondstagevars:
                  if var.startswith("Recovery") and (var, cons) in self.coeffs and self.coeffs[var, cons] == 1:
                     randcoef = 1 - np.random.binomial(1, 0.01)
                     if randcoef == 0:
                        outfile.write("    %s      %s               %g\n"%(var, cons, randcoef))

   def writeObjStochasticFile(self, outfile, nscenarios):
      '''
      writes the scenarios with objective stochasticity
      '''
      secondstagevars = []
      stage = 0
      for var in self.variables:
         if var == self.periods[1][1]:
            stage += 1

         if stage == 1:
            if var.startswith('Recovery'):
               secondstagevars.append(var)

      # writing the scenarios to the STO file
      weight = 1.0/float(nscenarios)
      for i in range(nscenarios):
         outfile.write(" SC SCEN%d      ROOT         %g        %s        0.0\n"%(i + 1, weight, self.periods[1][0]))
         for var in secondstagevars:
            if np.random.binomial(1, 0.1) == 1:
               randobj = (np.random.poisson() + 1)*100
               outfile.write("    %s      obj               %g\n"%(var, randobj))



class SSLPInstance(Instance):
   '''
   SMPS output functions for SSLP instances
   '''

   def writeStageFile(self, outfile):
      '''
      writes the stages file for a given core file
      '''
      stageconsstart = []
      stagevarstart = []

      # scanning all of the constraints to find the different stages
      stageconsstart.append(self.constraints[0])
      for cons in self.constraints[1:]:
         if cons.startswith("c2"):
            stageconsstart.append(cons)
            break

      # scanning all of the variables to find the different stages
      stagevarstart.append(self.variables[0])
      for var in self.variables[1:]:
         if var.startswith("y_1_1"):
            stagevarstart.append(var)
            break

      # writing the stages to the TIM file
      assert len(stageconsstart) == len(stagevarstart)
      for i in range(len(stageconsstart)):
         outfile.write("     %s     %s     STAGE-%d\n"%(stagevarstart[i],
            stageconsstart[i], i + 1))

   def writeRhsStochasticFile(self, outfile, nscenarios):
      '''
      writes the scenarios with RHS stochasticity
      '''
      # storing the first stage RHS to compute the standard deviationi
      #pdb.set_trace()
      stage = 0
      stagerhs = []
      secondstagecons = []
      for cons in self.constraints:
         if cons == self.periods[1][2]:
            stage += 1

         if stage == 0:
            stagerhs.append(self.rhs[cons])
         else:
            secondstagecons.append(cons)

      # computing the standard deviation
      stagestd = np.std(stagerhs)*2

      # writing the scenarios to the STO file
      weight = 1.0/float(nscenarios)
      for i in range(nscenarios):
         outfile.write(" SC SCEN%d      ROOT         %g        %s\n"%(i + 1, weight, self.periods[1][0]))
         for cons in secondstagecons:
            # computing the RHS of the constraint from a normal distribution
            #randrhs = int(np.random.normal(self.rhs[cons], stagestd))
            randrhs = round(np.random.random_sample())
            outfile.write("    RHS      %s               %g\n"%(cons, randrhs))


class NoswotInstance(Instance):
   '''
   SMPS output functions for the MIPLIB noswot instance
   '''

   def writeStageFile(self, outfile):
      '''
      writes the stages file for a given core file
      '''
      stageconsstart = []
      stagevarstart = []

      # scanning all of the constraints to find the different stages
      stageconsstart.append(self.constraints[0])
      for cons in self.constraints[1:]:
         if cons.startswith("p"):
            stageconsstart.append(cons)
            break

      # scanning all of the variables to find the different stages
      stagevarstart.append(self.variables[0])
      for var in self.variables[1:]:
         if var.startswith("pr"):
            stagevarstart.append(var)
            break

      # writing the stages to the TIM file
      assert len(stageconsstart) == len(stagevarstart)
      for i in range(len(stageconsstart)):
         outfile.write("     %s     %s     STAGE-%d\n"%(stagevarstart[i],
            stageconsstart[i], i + 1))

   def writeRhsStochasticFile(self, outfile, nscenarios):
      '''
      writes the scenarios with RHS stochasticity
      '''
      # storing the first stage RHS to compute the standard deviationi
      stage = 0
      stagerhs = []
      secondstagecons = []
      for cons in self.constraints:
         if cons == self.periods[1][2]:
            stage += 1

         if stage == 0:
            stagerhs.append(self.rhs[cons])
         else:
            secondstagecons.append(cons)

      # computing the standard deviation
      stagestd = np.std(stagerhs)*2

      # writing the scenarios to the STO file
      weight = 1.0/float(nscenarios)
      for i in range(nscenarios):
         outfile.write(" SC SCEN%d      ROOT         %g        %s\n"%(i + 1, weight, self.periods[1][0]))
         #for cons in secondstagecons:
            ## computing the RHS of the constraint from a normal distribution
            ##randrhs = int(np.random.normal(self.rhs[cons], stagestd))
            #randrhs = round(np.random.random_sample())
            #outfile.write("    RHS      %s               %g\n"%(cons, randrhs))


class SnipInstance(Instance):
   '''
   SMPS output functions for the SNIP instances
   '''

   def writeStageFile(self, outfile):
      '''
      writes the stages file for a given core file
      '''
      stageconsstart = []
      stagevarstart = []

      # scanning all of the constraints to find the different stages
      stageconsstart.append(self.constraints[0])
      for cons in self.constraints[1:]:
         if cons.startswith("sinkcons"):
            stageconsstart.append(cons)
            break

      # scanning all of the variables to find the different stages
      stagevarstart.append(self.variables[0])
      for var in self.variables[1:]:
         if var.startswith("node"):
            stagevarstart.append(var)
            break

      # writing the stages to the TIM file
      assert len(stageconsstart) == len(stagevarstart)
      for i in range(len(stageconsstart)):
         outfile.write("     %s     %s     STAGE-%d\n"%(stagevarstart[i],
            stageconsstart[i], i + 1))
