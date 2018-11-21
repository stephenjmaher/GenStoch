import instancegen as ig



if __name__ == "__main__":
   import sys

   if len(sys.argv) < 3:
      print "Usage: %s instance-name numscenarios [type]" % sys.argv[0]
      exit(1)
   else:
      print sys.argv

      stochtype = 0
      if len(sys.argv) == 4:
         stochtype = int(sys.argv[3])
         assert stochtype >= ig.STOCH_RHS and stochtype < ig.STOCH_COUNT

      instance = ig.instances["noswot"](
            "%s.cor"%(sys.argv[1]),"%s.tim"%(sys.argv[1]),
            "%s_%s.sto"%(sys.argv[1], sys.argv[2]))
      instance.readInstance(readCor = True, readTim = True)
      instance.writeStoFile(int(sys.argv[2]), stochtype)
      instance.writeSmpsFile()
