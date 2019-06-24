import wmi
import dataclasses

@dataclasses.dataclass
class DiskInfo:
    device_path: str
    caption: str
    size: int

def get_removable_disks():
    w = wmi.WMI()
    ret = []
    for disk in w.Win32_DiskDrive():
        if "Fixed" in disk.MediaType: continue
        ret.append(DiskInfo(caption=disk.Caption, device_path=disk.DeviceID, size=int(disk.Size)))
    return ret