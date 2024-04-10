import os, sys;
sModulePath = os.path.dirname(__file__);
sys.path = [sModulePath] + [sPath for sPath in sys.path if sPath.lower() != sModulePath.lower()];

from fTestDependencies import fTestDependencies;
fTestDependencies("--automatically-fix-dependencies" in sys.argv);
sys.argv = [s for s in sys.argv if s != "--automatically-fix-dependencies"];

try: # mDebugOutput use is Optional
  import mDebugOutput as m0DebugOutput;
except ModuleNotFoundError as oException:
  if oException.args[0] != "No module named 'mDebugOutput'":
    raise;
  m0DebugOutput = None;

guExitCodeInternalError = 1; # Use standard value;
try:
  try:
    from mConsole import oConsole;
  except:
    import sys, threading;
    oConsoleLock = threading.Lock();
    class oConsole(object):
      @staticmethod
      def fOutput(*txArguments, **dxArguments):
        sOutput = "";
        for x in txArguments:
          if isinstance(x, str):
            sOutput += x;
        sPadding = dxArguments.get("sPadding");
        if sPadding:
          sOutput.ljust(120, sPadding);
        oConsoleLock.acquire();
        print(sOutput);
        sys.stdout.flush();
        oConsoleLock.release();
      @staticmethod
      def fStatus(*txArguments, **dxArguments):
        pass;
  
  import sys;
  #Import the test subject
  import mRegistry;

  # Test registry access
  print("* Testing Registry access...");sys.stdout.flush();
  oTestRegistryValue = mRegistry.cRegistryValue(
    sTypeName = "SZ",
    xValue = "Test value",
  );
  oRegistryHiveKeyNamedValue = mRegistry.cRegistryHiveKeyNamedValue(
    sHiveName = "HKCU",
    sKeyPath = "Software\\SkyLined\\mRegistry",
    sValueName = "Test value name",
  );
  assert oRegistryHiveKeyNamedValue.sValueName == "Test value name", \
      "Unexpected registry hive key value name: %s" % oRegistryHiveKeyNamedValue.sValueName;
  assert oRegistryHiveKeyNamedValue.sFullPath == r"HKEY_CURRENT_USER\Software\SkyLined\mRegistry\Test value name", \
      "Unexpected registry hive key value path: %s" % oRegistryHiveKeyNamedValue.sFullPath;
  
  oRegistryHiveKey = oRegistryHiveKeyNamedValue.oRegistryHiveKey;
  assert oRegistryHiveKey.sKeyPath == r"Software\SkyLined\mRegistry", \
      "Unexpected registry hive key name: %s" % oRegistryHiveKey.sKeyPath;
  assert oRegistryHiveKey.sFullPath == r"HKEY_CURRENT_USER\Software\SkyLined\mRegistry", \
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
  o0ParentHiveKey = oRegistryHiveKey.o0ParentHiveKey;
  assert o0ParentHiveKey, \
      "Unexpected lack of parent hive key!";
  assert o0ParentHiveKey.sFullPath == r"HKEY_CURRENT_USER\Software\SkyLined", \
      "Unexpected parent hive key path: %s" % o0ParentHiveKey.sFullPath;
  
  for oParentSubHiveKey in o0ParentHiveKey.aoSubKeys:
    if oParentSubHiveKey.sFullPath == oRegistryHiveKey.sFullPath:
      break;
  else:
    raise AssertionError("%s is missing from sub keys (%s)" % (oRegistryHiveKey, o0ParentHiveKey.aoSubKeys));
  oSubKey = oRegistryHiveKey.foCreateSubKey("Test key name");
  oSubKey2 = oRegistryHiveKey.foGetSubKey("Test key name");
  assert oSubKey.sFullPath == oSubKey2.sFullPath, \
      "Unexpected sub key path mismatch (%s vs %s)" % (oSubKey.sFullPath, oSubKey2.sFullPath);
  assert oSubKey.o0ParentHiveKey, \
      "Unexpected lack of parent hive key in sub key!";
  assert oSubKey.o0ParentHiveKey.sFullPath == oRegistryHiveKey.sFullPath, \
      "Unexpected sub key parent path mismatch (%s vs %s)" % \
      (oSubKey.o0ParentHiveKey.sFullPath, oRegistryHiveKey.sFullPath);

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
  assert oRegistryHiveKeyNamedValue.fo0Get() is None, \
      "Deleting named registry value failed!";
  try:
    oRegistryHiveKeyNamedValue.foGet();
  except AssertionError:
    pass;
  else:
    raise AssertionError("Deleting named registry value failed!");
  print(oRegistryHiveKey.foSetValueForName(oRegistryHiveKeyNamedValue.sValueName, oTestRegistryValue));
  print(oRegistryHiveKey.foGetValueForName(oRegistryHiveKeyNamedValue.sValueName))
  print(oRegistryHiveKey.fbDeleteValueForName(oRegistryHiveKeyNamedValue.sValueName))
  print(oRegistryHiveKey.sFullPath);
  
  print("+ Done.");
  
except Exception as oException:
  if m0DebugOutput:
    m0DebugOutput.fTerminateWithException(oException, guExitCodeInternalError, bShowStacksForAllThread = True);
  raise;
