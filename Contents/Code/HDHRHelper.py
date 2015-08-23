#!/usr/bin/env python

import httplib
import re

class Tuner:
  def __init__(self, ipAddress, tunerId):
    self.ipAddress = str(ipAddress)
    self.tunerId = str(tunerId)

  def __str__(self):
    return "Tuner(%s, %s)" % (self.ipAddress, self.tunerId)

class HDHRHelper:
  def __init__(self, tunerList=[]):
    if not isinstance(tunerList, list):
      raise Exception("Invalid tuner list, not List object type")
    self.tunerList = tunerList

  def setTunerList(self, tunerList):
    self.tunerList = []
    for tuner in tunerList:
      self.tunerList.append(tuner)

  def __str__(self):
    retVal = ""
    for tuner in self.tunerList:
      retVal += "%s available: %s, " % (tuner,
                            self.checkTuner(tuner.ipAddress, tuner.tunerId))
    return retVal

  def getNextStreamURL(self):
    for tuner in self.tunerList:
      if self.checkTuner(tuner.ipAddress, tuner.tunerId):
        return tuner
    # No tuners found
    return False

  # Cheks specific tuner on HDHR device
  def checkTuner(self, ipAddress, tunerId):
    retVal = False
    conn = httplib.HTTPConnection(ipAddress)
    conn.request("GET", "/tuners.html?page=tuner%s" % (tunerId))
    r1 = conn.getresponse()
    if r1.status >= 200 and r1.status < 300:
      data1 = r1.read()
      match = re.search("Frequency</td><td>none", data1)
      if match:
        # Tuner is available
        return True
    # Tuner is not available
    return False

  def getPrimaryTunerIp(self):
    return self.tunerList[0].ipAddress

if __name__ == "__main__":
  print "HDHRHelper test starting..."
  tunerList = [Tuner("172.16.1.40",0), Tuner("172.16.1.40",1),
               Tuner("172.16.1.34",0), Tuner("172.16.1.34",1)]

  hdhrHelper = HDHRHelper(tunerList)
  print "getNextStreamURL: %s" % (hdhrHelper.getNextStreamURL())

  print "HDHRHeler: %s" % (hdhrHelper)

  print "hdhrHelper.getPrimaryTunerIp(): %s" % (hdhrHelper.getPrimaryTunerIp())

  print "HDHRHelper test finished"
