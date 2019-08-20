import os, re, sys, subprocess, threading, time;
sTestsFolderPath = os.path.dirname(os.path.abspath(__file__));
sMainFolderPath = os.path.dirname(sTestsFolderPath);
sParentFolderPath = os.path.dirname(sMainFolderPath);
sModulesFolderPath = os.path.join(sMainFolderPath, "modules");
asOriginalSysPath = sys.path[:];
sys.path = [sMainFolderPath, sParentFolderPath, sModulesFolderPath] + sys.path;
# Save the list of names of loaded modules:
asOriginalModuleNames = sys.modules.keys();

from mRegistry import *;

# Sub-packages should load all modules relative, or they will end up in the global namespace, which means they may get
# loaded by the script importing it if it tries to load a differnt module with the same name. Obviously, that script
# will probably not function when the wrong module is loaded, so we need to check that we did this correctly.
for sModuleName in sys.modules.keys():
  assert (
    sModuleName in asOriginalModuleNames # This was loaded before cBugId was loaded
    or sModuleName.lstrip("_").split(".", 1)[0] in [
      "mRegistry", "mWindowsSDK", # This was loaded as part of the mWindowsAPI package
      # These built-in modules are loaded by mRegistry and mWindowsSDK:
#      "base64", "binascii", "contextlib", "cStringIO", "ctypes", "encodings", "json", "nturl2path", "platform",
#      "socket", "ssl", "string", "strop", "struct", "textwrap", "urllib", "urlparse", "winreg",
    ]
  ), \
      "Module %s was unexpectedly loaded outside of the mWindowsAPI package!" % sModuleName;
# Restore the search path
sys.path = asOriginalSysPath;

if __name__ == "__main__":
  # Test registry access
  print "* Testing Registry access...";sys.stdout.flush();
  oTestRegistryValue = cRegistryValue(
    sTypeName = "SZ",
    xValue = "Test value",
  );
  oRegistryHiveKeyNamedValue = cRegistryHiveKeyNamedValue(
    sHiveName = "HKCU",
    sKeyName = r"Software\SkyLined\mWindowsAPI",
    sValueName = "Test value name",
  );
  assert oRegistryHiveKeyNamedValue.foSet(oTestRegistryValue), \
      "Could not set named registry value!";
  assert oRegistryHiveKeyNamedValue.foGet() == oTestRegistryValue, \
      "Could not get named registry value!";
  assert oRegistryHiveKeyNamedValue.fbDelete(), \
      "Could not delete named registry value";
  assert oRegistryHiveKeyNamedValue.foGet() is None, \
      "Deleting named registry value failed!";
