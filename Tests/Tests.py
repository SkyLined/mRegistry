from fTestDependencies import fTestDependencies;
fTestDependencies();

try:
  import mDebugOutput;
except:
  mDebugOutput = None;
try:
  try:
    from oConsole import oConsole;
  except:
    import sys, threading;
    oConsoleLock = threading.Lock();
    class oConsole(object):
      @staticmethod
      def fOutput(*txArguments, **dxArguments):
        sOutput = "";
        for x in txArguments:
          if isinstance(x, (str, unicode)):
            sOutput += x;
        sPadding = dxArguments.get("sPadding");
        if sPadding:
          sOutput.ljust(120, sPadding);
        oConsoleLock.acquire();
        print sOutput;
        sys.stdout.flush();
        oConsoleLock.release();
      fPrint = fOutput;
      @staticmethod
      def fStatus(*txArguments, **dxArguments):
        pass;
  
  import sys;
  #Import the test subject
  import mRegistry;

  # Test registry access
  print "* Testing Registry access...";sys.stdout.flush();
  oTestRegistryValue = mRegistry.cRegistryValue(
    sTypeName = "SZ",
    xValue = "Test value",
  );
  oRegistryHiveKeyNamedValue = mRegistry.cRegistryHiveKeyNamedValue(
    sHiveName = "HKCU",
    sKeyName = r"Software\SkyLined\mRegistry",
    sValueName = "Test value name",
  );
  assert oRegistryHiveKeyNamedValue.sValueName == "Test value name", \
      "Unexpected registry hive key value name: %s" % oRegistryHiveKeyNamedValue.sValueName;
  assert oRegistryHiveKeyNamedValue.sFullPath == r"HKEY_CURRENT_USER\Software\SkyLined\mRegistry\Test value name", \
      "Unexpected registry hive key value path: %s" % oRegistryHiveKeyNamedValue.sFullPath;
  
  oRegistryHiveKey = oRegistryHiveKeyNamedValue.oRegistryHiveKey;
  assert oRegistryHiveKey.sKeyName == "Software\SkyLined\mRegistry", \
      "Unexpected registry hive key name: %s" % oRegistryHiveKey.sKeyName;
  assert oRegistryHiveKey.sFullPath == "HKEY_CURRENT_USER\Software\SkyLined\mRegistry", \
      "Unexpected registry hive key path: %s" % oRegistryHiveKey.sFullPath;
  
  oRegistryHive = oRegistryHiveKey.oRegistryHive;
  assert oRegistryHive.sHiveName == "HKEY_CURRENT_USER", \
      "Unexpected registry hive name: %s" % (oRegistryHive.sHiveName);
  assert oRegistryHive.sFullPath == "HKEY_CURRENT_USER", \
      "Unexpected registry hive path: %s" % (oRegistryHive.sFullPath);
  
  assert oRegistryHive == oRegistryHiveKeyNamedValue.oRegistryHive, \
      "Registry hive mismatch: %s vs %s" % (oRegistryHive, oRegistryHiveKeyNamedValue.oRegistryHive);
  
  assert oRegistryHiveKeyNamedValue.foSet(oTestRegistryValue), \
      "Could not set named registry value!";
  assert oRegistryHiveKeyNamedValue.foGet() == oTestRegistryValue, \
      "Could not get named registry value!";

  assert oRegistryHiveKey.doValue_by_Name["Test value name"].xValue == oTestRegistryValue.xValue, \
      "Unexpected registry value mismatch (%s vs %s)" % \
      (oRegistryHiveKey.doValue_by_Name["Test value name"].xValue, oTestRegistryValue.xValue);
  
  assert oRegistryHiveKey.bExists, \
      "Expected %s to exist!" % oRegistryHiveKey;
  oParentHiveKey = oRegistryHiveKey.oParentHiveKey;
  assert oParentHiveKey.sFullPath == r"HKEY_CURRENT_USER\Software\SkyLined", \
      "Unexpected parent hive key path: %s" % oParentHiveKey.sFullPath;
  
  for oParentSubHiveKey in oParentHiveKey.aoSubKeys:
    if oParentSubHiveKey.sFullPath == oRegistryHiveKey.sFullPath:
      break;
  else:
    raise AssertionError("%s is missing from sub keys (%s)" % (oRegistryHiveKey, oParentHiveKey.aoSubKeys));
  oSubKey = oRegistryHiveKey.foCreateSubKey("Test key name");
  oSubKey2 = oRegistryHiveKey.foGetSubKey("Test key name");
  assert oSubKey.sFullPath == oSubKey2.sFullPath, \
      "Unexpected sub key path mismatch (%s vs %s)" % (oSubKey.sFullPath, oSubKey2.sFullPath);
  assert oSubKey.oParentHiveKey.sFullPath == oRegistryHiveKey.sFullPath, \
      "Unexpected sub key parent path mismatch (%s vs %s)" % \
      (oSubKey.oParentHiveKey.sFullPath, oRegistryHiveKey.sFullPath);

  assert oRegistryHiveKey.doSubKey_by_sName["Test key name"].sFullPath == oSubKey.sFullPath, \
      "Unexpected sub key path mismatch (%s vs %s)" % \
      (oRegistryHiveKey.doSubKey_by_sName["Test key name"].sFullPath, oSubKey.sFullPath);
  for oNamedValue in oRegistryHiveKey.aoNamedValues:
    if oNamedValue.sFullPath == oRegistryHiveKeyNamedValue.sFullPath:
      break;
  else:
    raise AssertionError("%s is missing from named values (%s)" % (oNamedValue, oRegistryHiveKey.aoNamedValues));
  
  assert oRegistryHiveKeyNamedValue.fbDelete(), \
      "Could not delete named registry value";
  assert oRegistryHiveKeyNamedValue.foGet() is None, \
      "Deleting named registry value failed!";
  print oRegistryHiveKey.foSetNamedValue(oRegistryHiveKeyNamedValue.sValueName, oTestRegistryValue);
  print oRegistryHiveKey.foGetNamedValue(oRegistryHiveKeyNamedValue.sValueName)
  print oRegistryHiveKey.fbDeleteNamedValue(oRegistryHiveKeyNamedValue.sValueName)
  print oRegistryHiveKey.sFullPath;
  
  print "+ Done.";
  
except Exception as oException:
  if mDebugOutput:
    mDebugOutput.fTerminateWithException(oException, bShowStacksForAllThread = True);
  raise;
