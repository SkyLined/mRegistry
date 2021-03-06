import _winreg;
from mWindowsSDK import *;

gduHive_by_sName = {
  "HKCR":                             _winreg.HKEY_CLASSES_ROOT,
  "HKEY_CLASSES_ROOT":                _winreg.HKEY_CLASSES_ROOT,
  "HKCU":                             _winreg.HKEY_CURRENT_USER,
  "HKEY_CURRENT_USER":                _winreg.HKEY_CURRENT_USER,
  "HKLM":                             _winreg.HKEY_LOCAL_MACHINE,
  "HKEY_LOCAL_MACHINE":               _winreg.HKEY_LOCAL_MACHINE,
  "HKU":                              _winreg.HKEY_USERS,
  "HKEY_USERS":                       _winreg.HKEY_USERS,
  "HKCC":                             _winreg.HKEY_CURRENT_CONFIG,
  "HKEY_CURRENT_CONFIG":              _winreg.HKEY_CURRENT_CONFIG,
};
gdsName_by_uHive = {
  _winreg.HKEY_CLASSES_ROOT:          "HKEY_CLASSES_ROOT",
  _winreg.HKEY_CURRENT_USER:          "HKEY_CURRENT_USER",
  _winreg.HKEY_LOCAL_MACHINE:         "HKEY_LOCAL_MACHINE",
  _winreg.HKEY_USERS:                 "HKEY_USERS",
  _winreg.HKEY_CURRENT_CONFIG:        "HKEY_CURRENT_CONFIG",
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
      oSelf.__oHive = _winreg.ConnectRegistry(None, oSelf.uHive);
    return oSelf.__oHive;

  def foCreateWinRegKey(oSelf, sKeyName, bForWriting = False, uRegistryBits = 0):
    uAccessMask = _winreg.KEY_READ | (bForWriting and _winreg.KEY_SET_VALUE or 0) | {32: _winreg.KEY_WOW64_32KEY, 64:_winreg.KEY_WOW64_64KEY}.get(uRegistryBits, 0);
    return _winreg.CreateKeyEx(oSelf.oHive, sKeyName, 0, uAccessMask);
    
  def foCreateHiveKey(oSelf, sKeyName, bForWriting = False, uRegistryBits = 0):
    oWinRegKey = oSelf.foCreateWinRegKey(sKeyName, bForWriting = bForWriting, uRegistryBits = uRegistryBits);
    return cRegistryHiveKey(
      sKeyName = sKeyName,
      oRegistryHive = oSelf,
      oWinRegKey = oWinRegKey,
      bWinRegKeyOpenForWriting = bForWriting,
    );
  
  def foOpenWinRegKey(oSelf, sKeyName, bForWriting = False, uRegistryBits = 0):
    uAccessMask = _winreg.KEY_READ | (bForWriting and _winreg.KEY_SET_VALUE or 0) | {32: _winreg.KEY_WOW64_32KEY, 64:_winreg.KEY_WOW64_64KEY}.get(uRegistryBits, 0);
    try:
      return _winreg.OpenKey(oSelf.oHive, sKeyName, 0, uAccessMask);
    except WindowsError, oWindowsError:
      if oWindowsError.errno != WIN32_FROM_HRESULT(HRESULT(ERROR_FILE_NOT_FOUND)):
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
      _winreg.DeleteKey(oWinRegKey, sSubKeyName);
    except WindowsError, oWindowsError:
      if oWindowsError.errno != WIN32_FROM_HRESULT(HRESULT(ERROR_FILE_NOT_FOUND)):
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