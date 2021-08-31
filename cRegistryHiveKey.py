import winreg;
from mWindowsSDK import *
# There are more imports at the end that need to be there and not here to prevent import loops.

class cRegistryHiveKey(object):
  def __init__(oSelf, xUnused = None, sKeyPath = None, oRegistryHive = None, oWinRegKey = None, bWinRegKeyOpenForWriting = False, uRegistryBits = 0, **dxRegistryHiveArguments):
    assert xUnused is None, \
        "Constructor arguments must be named values!";
    assert sKeyPath, \
        "You must provide a valid value for sKeyPath, not %s" % repr(sKeyPath);
    if oRegistryHive is None:
      oRegistryHive = cRegistryHive(**dxRegistryHiveArguments);
    else:
      assert not dxRegistryHiveArguments, \
          "You must provide either oRegistryHive or dxRegistryHiveArguments, not both";
    
    oSelf.__oRegistryHive = oRegistryHive;
    oSelf.__sKeyPath = sKeyPath;
    oSelf.__oWinRegKey = oWinRegKey;
    oSelf.__bKeyOpenForWriting = bWinRegKeyOpenForWriting;
    oSelf.__uRegistryBits = uRegistryBits;
  
  @property
  def oRegistryHive(oSelf):
    # Getter for oRegistryHive
    return oSelf.__oRegistryHive;
  @oRegistryHive.setter
  def oRegistryHive(oSelf, oRegistryHive):
    # Setter for oRegistryHive deletes cached oWinRegKey
    oSelf.__oWinRegKey = None;
    oSelf.__oRegistryHive = oRegistryHive;
  
  @property
  def sKeyName(oSelf):
    # Getter for sKeyName
    return oSelf.__sKeyPath.rsplit("\\", 1)[-1];
  @property
  def sKeyPath(oSelf):
    # Getter for sKeyName
    return oSelf.__sKeyPath;
  @sKeyName.setter
  def sKeyName(oSelf, sKeyName):
    assert sKeyName, \
        "You must provide a valid value for sKeyName, not %s" % repr(sKeyName);
    # Setter for sKeyName deletes cached oWinRegKey
    oSelf.__oWinRegKey = None;
    oSelf.__sKeyPath = "\\".join(oSelf.__sKeyPath.rsplit("\\")[:-1] + [sKeyName]);
  @sKeyPath.setter
  def sKeyPath(oSelf, sKeyPath):
    assert sKeyPath, \
        "You must provide a valid value for sKeyPath, not %s" % repr(sKeyPath);
    # Setter for sKeyName deletes cached oWinRegKey
    oSelf.__oWinRegKey = None;
    oSelf.__sKeyPath = sKeyPath;
  def __fo0OpenWinRegKey(oSelf, bForWriting = False, bThrowErrors = False):
    # return cached oWinRegKey if appropriate or create a new oWinRegKey
    if (bForWriting and not oSelf.__bKeyOpenForWriting):
      oSelf.__oWinRegKey = None;
    if oSelf.__oWinRegKey is None:
      oSelf.__oWinRegKey = oSelf.__oRegistryHive.foOpenWinRegKey(
        oSelf.__sKeyPath,
        bForWriting = bForWriting,
        uRegistryBits = oSelf.__uRegistryBits,
        bThrowErrors = bThrowErrors,
      );
      oSelf.__bKeyOpenForWriting = bForWriting;
    return oSelf.__oWinRegKey;
  
  def __foCreateWinRegKey(oSelf, bForWriting = False): # Always throws errors
    # return cached oWinRegKey if appropriate or create a new oWinRegKey
    if (bForWriting and not oSelf.__bKeyOpenForWriting):
      oSelf.__oWinRegKey = None;
    if oSelf.__oWinRegKey is None:
      oSelf.__oWinRegKey = oSelf.__oRegistryHive.foCreateWinRegKey(
        oSelf.__sKeyPath,
        bForWriting = bForWriting,
        uRegistryBits = oSelf.__uRegistryBits,
      );
      oSelf.__bKeyOpenForWriting = bForWriting;
    return oSelf.__oWinRegKey;
  
  @property
  def bExists(oSelf):
    return oSelf.__fo0OpenWinRegKey() is not None;

  def fbCreate(oSelf, bForWriting = False, bThrowErrors = False):
    if oSelf.bExists:
      return True;
    oSelf.__oWinRegKey = oSelf.__oRegistryHive.foCreateWinRegKey(
      oSelf.__sKeyPath,
      bForWriting = bForWriting,
      uRegistryBits = oSelf.__uRegistryBits,
      bThrowErrors = bThrowErrors
    );
    bSuccess = oSelf.__oWinRegKey is not None;
    oSelf.__bKeyOpenForWriting = bSuccess and bForWriting;
    return bSuccess;
  
  def fbDelete(oSelf, bThrowErrors = False):
    for sSubKeyName in list(oSelf.doSubKey_by_sName.keys()):
      if not oSelf.fbDeleteSubKey(sSubKeyName, bThrowErrors = bThrowErrors):
        return False;
    return oSelf.o0ParentHiveKey.fbDeleteSubKey(oSelf.sKeyName, bThrowErrors = bThrowErrors) if oSelf.o0ParentHiveKey else True;
  
  def fbDeleteSubKey(oSelf, sSubKeyName, bThrowErrors = False):
    return oSelf.__oRegistryHive.fbDeleteHiveKeySubKey(
      oSelf,
      sSubKeyName,
      uRegistryBits = oSelf.__uRegistryBits,
      bThrowErrors = bThrowErrors
    );
  
  @property
  def o0ParentHiveKey(oSelf):
    try:
      sParentKeyPath = oSelf.__sKeyPath[:oSelf.__sKeyPath.rindex("\\")];
    except ValueError:
      return None; # This is a root key; there is no parent
    return cRegistryHiveKey(
      sKeyPath = sParentKeyPath,
      oRegistryHive = oSelf.__oRegistryHive,
      uRegistryBits = oSelf.__uRegistryBits,
    );
  
  def foCreateSubKey(oSelf, sSubKeyName, bForWriting = False, bThrowErrors = False):
    return oSelf.__oRegistryHive.foCreateHiveKey(
      "%s\\%s" % (oSelf.__sKeyPath, sSubKeyName),
      bForWriting = bForWriting,
      uRegistryBits = oSelf.__uRegistryBits,
      bThrowErrors = bThrowErrors,
    );
  
  def foGetSubKey(oSelf, sSubKeyName):
    return cRegistryHiveKey(
      sKeyName = "%s\\%s" % (oSelf.__sKeyPath, sSubKeyName),
      oRegistryHive = oSelf.__oRegistryHive,
    );
  
  @property
  def aoSubKeys(oSelf):
    doSubKey_by_sName = oSelf.doSubKey_by_sName;
    if doSubKey_by_sName is None:
      return None;
    return list(doSubKey_by_sName.values());
  
  @property
  def doSubKey_by_sName(oSelf):
    o0WinRegKey = oSelf.__fo0OpenWinRegKey();
    if not o0WinRegKey:
      return None;
    doSubKey_by_sName = {};
    while 1:
      try:
        sSubKeyName = winreg.EnumKey(o0WinRegKey, len(doSubKey_by_sName));
      except WindowsError:
        return doSubKey_by_sName;
      doSubKey_by_sName[sSubKeyName] = cRegistryHiveKey(
        sKeyPath = "%s\\%s" % (oSelf.__sKeyPath, sSubKeyName),
        oRegistryHive = oSelf.__oRegistryHive,
      );
  
  @property
  def aoNamedValues(oSelf):
    o0WinRegKey = oSelf.__fo0OpenWinRegKey();
    if not o0WinRegKey:
      return None;
    aoNamedValues = [];
    while 1:
      try:
        (sValueName, xValue, uValueType) = winreg.EnumValue(o0WinRegKey, len(aoNamedValues));
      except WindowsError:
        return aoNamedValues;
      aoNamedValues.append(cRegistryHiveKeyNamedValue(sValueName = sValueName, oRegistryHiveKey = oSelf));
  
  @property
  def doValue_by_Name(oSelf):
    o0WinRegKey = oSelf.__fo0OpenWinRegKey();
    if not o0WinRegKey:
      return None;
    doValue_by_Name = {};
    while 1:
      try:
        (sValueName, xValue, uType) = winreg.EnumValue(o0WinRegKey, len(doValue_by_Name));
      except WindowsError:
        return doValue_by_Name;
      doValue_by_Name[sValueName] = cRegistryValue(uType = uType, xValue = xValue);
  
  def foCreateNamedValue(oSelf, sValueName):
    return cRegistryHiveKeyNamedValue(sValueName = sValueName, oRegistryHiveKey = oSelf);
  def fo0GetNamedValue(oSelf, sValueName, bThrowErrors = False):
    o0WinRegKey = oSelf.__fo0OpenWinRegKey(bThrowErrors = bThrowErrors);
    if not o0WinRegKey:
      return None;
    try:
      xValue, uType = winreg.QueryValueEx(o0WinRegKey, sValueName);
    except WindowsError as oWindowsError:
      if not bThrowErrors and oWindowsError.errno == ERROR_FILE_NOT_FOUND:
        return None; # The value does not exist.
      raise;
    return cRegistryHiveKeyNamedValue(sValueName = sValueName, oRegistryHiveKey = oSelf);
  
  def foGetValueForName(oSelf, sValueName, bThrowErrors = False):
    o0WinRegKey = oSelf.__fo0OpenWinRegKey(bThrowErrors = bThrowErrors);
    if not o0WinRegKey:
      return None;
    try:
      xValue, uType = winreg.QueryValueEx(o0WinRegKey, sValueName);
    except WindowsError as oWindowsError:
      if not bThrowErrors and oWindowsError.errno == ERROR_FILE_NOT_FOUND:
        return None; # The value does not exist.
      raise;
    return cRegistryValue(uType = uType, xValue = xValue);
  
  def foSetValueForName(oSelf, sValueName, oRegistryValue = None, **dxRegistryValueArguments):
    if oRegistryValue is None:
      assert dxRegistryValueArguments, \
          "You must provide a value for either oRegistryValue or dxRegistryValueArguments";
      oRegistryValue = cRegistryValue(**dxRegistryValueArguments);
    oWinRegKey = oSelf.__foCreateWinRegKey(bForWriting = True);
    winreg.SetValueEx(oWinRegKey, sValueName, 0, oRegistryValue.uType, oRegistryValue.xValue);
    return oRegistryValue;
  
  def fbDeleteValueForName(oSelf, sValueName, bThrowErrors = False):
    if not oSelf.bExists:
      return True; # The key does not exist.
    o0WinRegKey = oSelf.__fo0OpenWinRegKey(bForWriting = True, bThrowErrors = bThrowErrors);
    if not o0WinRegKey:
      return False; # Could not open the key.
    try:
      winreg.DeleteValue(o0WinRegKey, sValueName);
    except WindowsError as oWindowsError:
      if not bThrowErrors and oWindowsError.errno == ERROR_FILE_NOT_FOUND:
        return False; # The value does not exist.
      raise;
    return True;
  
  @property
  def sFullPath(oSelf):
    return "%s\\%s" % (oSelf.__oRegistryHive.sFullPath, oSelf.__sKeyPath);
  
  def fsToString(oSelf):
    return "%s{path=%s}" % (oSelf.__class__.__name__, oSelf.sFullPath);
  def __repr__(oSelf):
    return "<%s %s>" % (oSelf.__class__.__name__, oSelf.sFullPath);
  def __str__(oSelf):
    return "%s %s" % (oSelf.__class__.__name__, oSelf.sFullPath);

from .cRegistryHive import cRegistryHive;
from .cRegistryHiveKeyNamedValue import cRegistryHiveKeyNamedValue;
from .cRegistryValue import cRegistryValue;
