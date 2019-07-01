from typing import List
import wmi
import dataclasses
import ctypes
import zipfile
import msvcrt
import wx
import threading
from .local_storage import IMAGE_FILE

@dataclasses.dataclass
class DiskInfo:
    device_path: str
    caption: str
    size: int
    mounted_volumes: List[str]

def get_removable_disks():
    w = wmi.WMI()
    ret = []
    for disk in w.Win32_DiskDrive():
        if "Fixed" in disk.MediaType: continue
        mounted_volumes = []
        for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
            print(f"Partition {partition.Caption}")
            logical = partition.associators("Win32_LogicalDiskToPartition")
            if logical:
                mounted_volumes.append(logical[0].Caption)

        ret.append(DiskInfo(caption=disk.Caption, device_path=disk.DeviceID, size=int(disk.Size), mounted_volumes=mounted_volumes))
    return ret




def write_image_worker(target_disk, progress_callback=None):
    kernel32 = ctypes.windll.kernel32
    volume_handles = []
    for volume in target_disk.mounted_volumes:
        print(f"Locking {volume}")
        volume_fp = open(rf"\\.\{volume}", "rb+")
        volume_handle = msvcrt.get_osfhandle(volume_fp.fileno())
        s = ctypes.c_int()
        # Lock the volume
        ret = kernel32.DeviceIoControl(volume_handle, 0x00090018,None, 0, None, 0, ctypes.byref(s), None )
        if ret == 0:
            raise ctypes.WinError()
        volume_handles.append(volume_handle)

        
    zf = zipfile.ZipFile(IMAGE_FILE)
    infos = zf.infolist()
    if len(infos) > 1:
        raise ValueError("Too many files in archive, only one was expected.")
    img_file = infos[0]
    source_fp = zf.open(img_file.filename)
    target_fp = open(target_disk.device_path, "rb+")
    print("Opened disk.")
    target_handle = msvcrt.get_osfhandle(target_fp.fileno())
    s = ctypes.c_int()
    # Lock volume
    ret = kernel32.DeviceIoControl(target_handle, 0x00090018,None, 0, None, 0, ctypes.byref(s), None )
    if ret == 0:
        raise ctypes.WinError()
    print("Locked disk.")
    CHUNK_SIZE = 1024*1024
    so_far = 0
    while True:
        chunk = source_fp.read(CHUNK_SIZE)
        if not chunk:
            break
        so_far += len(chunk)
        target_fp.write(chunk)
        if progress_callback:
            wx.CallAfter(progress_callback, img_file.file_size, so_far)
    target_fp.close()

def write_image_to(target_disk, progress_callback=None):
    threading.Thread(target=write_image_worker, args=(target_disk, progress_callback)).start()