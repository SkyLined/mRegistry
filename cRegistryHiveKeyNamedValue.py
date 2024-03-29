# There are imports at the end that need to be there and not here to prevent import loops.

class cRegistryHiveKeyNamedValue(object):
  def __init__(oSelf, xUnused = None, sValueName = None, oRegistryHiveKey = None, **dxRegistryHiveKeyArguments):
    assert xUnused is None, \
        "Constructor arguments must be named values!";
    assert sValueName is not None and "\\" not in sValueName, \
        "You must provide a valid value for sValueName, not %s (use \"\" for default value)" % repr(sValueName);
    if oRegistryHiveKey is None:
      oRegistryHiveKey = cRegistryHiveKey(**dxRegistryHiveKeyArguments);
    else:
      assert not dxRegistryHiveKeyArguments, \
          "You must provide either oRegistryHiveKey or dxRegistryHiveKeyArguments, not both";
    oSelf.sValueName = sValueName;
    oSelf.__oRegistryHiveKey = oRegistryHiveKey;
    
  # Getter/setter for oRegistryHive
  @property
  def oRegistryHive(oSelf):
    return oSelf.__oRegistryHiveKey.oRegistryHive;
  @oRegistryHive.setter
  def oRegistryHive(oSelf, oRegistryHive):
    oSelf.__oRegistryHiveKey.oRegistryHive = oRegistryHive;
  # Getter/setter for oRegistryHiveKey
  @property
  def oRegistryHiveKey(oSelf):
    return oSelf.__oRegistryHiveKey;
  @oRegistryHiveKey.setter
  def oRegistryHiveKey(oSelf, oRegistryHiveKey):
    oSelf.__oRegistryHiveKey = oRegistryHiveKey;
  
  # Getter/setter for oRegistryValue
  def foGet(oSelf, bThrowErrors = False):
    return oSelf.__oRegistryHiveKey.foGetValueForName(oSelf.sValueName, bThrowErrors = bThrowErrors);
  def fo0Get(oSelf, bThrowErrors = False):
    return oSelf.__oRegistryHiveKey.fo0GetValueForName(oSelf.sValueName, bThrowErrors = bThrowErrors);
  def foSet(oSelf, oRegistryValue):
    return oSelf.__oRegistryHiveKey.foSetValueForName(oSelf.sValueName, oRegistryValue);
  def fbDelete(oSelf, bThrowErrors = False):
    return oSelf.__oRegistryHiveKey.fbDeleteValueForName(oSelf.sValueName, bThrowErrors = bThrowErrors);
  
  @property
  def sFullPath(oSelf):
    return "%s\\%s" % (oSelf.__oRegistryHiveKey.sFullPath, oSelf.sValueName);
  
  def fsToString(oSelf):
    return "%s{path=%s}" % (oSelf.__class__.__name__, oSelf.sFullPath);
  def __repr__(oSelf):
    return "<%s %s>" % (oSelf.__class__.__name__, oSelf.sFullPath);
  def __str__(oSelf):
    return "%s %s" % (oSelf.__class__.__name__, oSelf.sFullPath);

from .cRegistryHiveKey import cRegistryHiveKey;
from .cRegistryValue import cRegistryValue;
