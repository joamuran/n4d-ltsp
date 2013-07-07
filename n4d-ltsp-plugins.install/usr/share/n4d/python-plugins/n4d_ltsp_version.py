class n4dLTSPVersion:
   import subprocess
   def getVersion(self):
      info=subprocess.check_output(["apt-cache","policy","n4d-ltsp-plugins"])
      lines=str(info).split('\n')
      version=lines[1][13:]
      
      return (version)

