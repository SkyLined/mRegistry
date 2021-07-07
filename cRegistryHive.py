import winreg;
from mWindowsSDK import *;

gduHive_by_sName = {
  "HKCR":                             winreg.HKEY_CLASSES_ROOT,
  "HKEY_CLASSES_ROOT":                winreg.HKEY_CLASSES_ROOT,
  "HKCU":                             winreg.HKEY_CURRENT_USER,
  "HKEY_CURRENT_USER":                winreg.HKEY_CURRENT_USER,
  "HKLM":                             winreg.HKEY_LOCAL_MACHINE,
  "HKEY_LOCAL_MACHINE":               winreg.HKEY_LOCAL_MACHINE,
  "HKU":                              winreg.HKEY_USERS,
  "HKEY_USERS":                       winreg.HKEY_USERS,
  "HKCC":                             winreg.HKEY_CURRENT_CONFIG,
  "HKEY_CURRENT_CONFIG":              winreg.HKEY_CURRENT_CONFIG,
};
gdsName_by_uHive = {
  winreg.HKEY_CLASSES_ROOT:           "HKEY_CLASSES_ROOT",
  winreg.HKEY_CURRENT_USER:           "HKEY_CURRENT_USER",
  winreg.HKEY_LOCAL_MACHINE:          "HKEY_LOCAL_MACHINE",
  winreg.HKEY_USERS:                  "HKEY_USERS",
  winreg.HKEY_CURRENT_CONFIG:         "HKEY_CURRENT_CONFIG",
};

class cRegistryHive(object):
  duHive_by_sName = gduHive_by_sName;
  dsName_by_uHive = gdsName_by_uHive;
  
  def __init__(oSelf, xUnused = None, uHive = None, sHiveName = None):
    assert xUnused is None, \
        "Constructor arguments must be named values!";
    if uHive is None:
      assert sHiveName is not None, \
          "You must provide either uHive or sHiveName, not both";
      uHive = cRegistryHive.duHive_by_sName.get(sHiveName);
      assert uHive is not None, \
          "You must provide a valid sHiveName, not %s" % repr(sHiveName);
    else:
      assert uHive in cRegistryHive.dsName_by_uHive, \
          "You must provide a valid uHive, not %s" % repr(uHive);
    
    oSelf.__uHive = uHive;
    oSelf.__oHive = None;
  
  @property
  def uHive(oSelf):
    # Getter for uHive
    return oSelf.__uHive;
  
  @uHive.setter
  def uHive(oSelf, uHive):
    # Setter for uHive deletes cached oHive
    oSelf.__oHive = None;
    oSelf.__uHive = uHive;
    return uHive;
  
  @property
  def sHiveName(oSelf):
    # Getter for sHiveName
    return cRegistryHive.dsName_by_uHive[oSelf.__uHive];
  
  @sHiveName.setter
  def sHiveName(oSelf, sHiveName):
    # Setter for sHiveName sets uHive, which deletes cached oHive
    assert sHiveName in cRegistryHive.duHive_by_sName, \
        "Unknown hive name %s" % sHiveName;
    oSelf.uHive = cRegistryHive.duHive_by_sName[sHiveName];
  
  @property
  def oHive(oSelf):
    if oSelf.__oHive is None:
      oSelf.__oHive = winreg.ConnectRegistry(None, oSelf.uHive);
    return oSelf.__oHive;

  def foCreateWinRegKey(oSelf, sKeyName, bForWriting = False, uRegistryBits = 0):
    uAccessMask = winreg.KEY_READ | (bForWriting and winreg.KEY_SET_VALUE or 0) | {32: winreg.KEY_WOW64_32KEY, 64:winreg.KEY_WOW64_64KEY}.get(uRegistryBits, 0);
    return winreg.CreateKeyEx(oSelf.oHive, sKeyName, 0, uAccessMask);
    
  def foCreateHiveKey(oSelf, sKeyName, bForWriting = False, uRegistryBits = 0):
    oWinRegKey = oSelf.foCreateWinRegKey(sKeyName, bForWriting = bForWriting, uRegistryBits = uRegistryBits);
    return cRegistryHiveKey(
      sKeyName = sKeyName,
      oRegistryHive = oSelf,
      oWinRegKey = oWinRegKey,
      bWinRegKeyOpenForWriting = bForWriting,
    );
  
  def foOpenWinRegKey(oSelf, sKeyName, bForWriting = False, uRegistryBits = 0):
    uAccessMask = winreg.KEY_READ | (bForWriting and winreg.KEY_SET_VALUE or 0) | {32: winreg.KEY_WOW64_32KEY, 64:winreg.KEY_WOW64_64KEY}.get(uRegistryBits, 0);
    try:
      return winreg.OpenKey(oSelf.oHive, sKeyName, 0, uAccessMask);
    except WindowsError as oWindowsError:
      if oWindowsError.errno != ERROR_FILE_NOT_FOUND:
        raise;
      return None; # The key does not exist.
  
  def foOpenHiveKey(oSelf, sKeyName, bForWriting = False, uRegistryBits = 0):
    oWinRegKey = oSelf.foOpenWinRegKey(sKeyName, bForWriting = bForWriting, uRegistryBits = uRegistryBits);
    return oWinRegKey and cRegistryHiveKey(
      sKeyName = sKeyName,
      oRegistryHive = oSelf,
      oWinRegKey = oWinRegKey,
      bWinRegKeyOpenForWriting = bForWriting,
    );
  
  def fbDeleteHiveKeySubKey(oSelf, oHiveKey, sSubKeyName, uRegistryBits = 0):
    oWinRegKey = oSelf.foOpenWinRegKey(oHiveKey.sKeyName, bForWriting = True, uRegistryBits = uRegistryBits);
    if not oWinRegKey:
      return False;
    try:
      winreg.DeleteKey(oWinRegKey, sSubKeyName);
    except WindowsError as oWindowsError:
      if oWindowsError.errno != ERROR_FILE_NOT_FOUND:
        raise;
      return False; # The value does not exist.
    return True;
  
  @property
  def sFullPath(oSelf):
    return oSelf.sHiveName;
  
  def fsToString(oSelf):
    return "%s{path=%s}" % (oSelf.__class__.__name__, oSelf.sFullPath);
  def __repr__(oSelf):
    return "<%s %s>" % (oSelf.__class__.__name__, oSelf.sFullPath);
  def __str__(oSelf):
    return "%s %s" % (oSelf.__class__.__name__, oSelf.sFullPath);

from .cRegistryHiveKey import cRegistryHiveKey;