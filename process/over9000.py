import os
import time

import shutil


def over9000(adb, fastboot, platform):

    '''
    This function is to used to flash factory images.
    '''

    if platform == "win32":
        path = "tmp\\"
        flashall = path + "flash-all.bat"
        oneplus_check = path + "sbl1.mbn"
        oneplus = os.path.exists(oneplus_check)
    else:
        path = "tmp/"
        flashall = path + "flash-all.sh"
        oneplus_check = path + "sbl1.mbn"
        oneplus = os.path.exists(oneplus_check)
        if not oneplus:
            os.system("chmod 755 " + flashall)

    print("Rebooting into bootloader")
    os.system(adb + " reboot bootloader")
    time.sleep(5)
    if not oneplus:
        print("Flasing Stock Rom\n!!!! DONT UNPLUG THE DEVICE !!!!")
        os.system(flashall)
        print("Flasing Stock Rom DONE")
        print("Removing untar'd factory files")
        if os.path.exists(path):
            shutil.rmtree(path)
        print("Removed folder " + path)
        print("\nThe device should be rebooting, once it is booted do the initial setup,")
        print("enable developer options and USB debugging again.\n\n")
        raw_input("Press any key to continue...")
    else:
        print("Detected a OnePlus factory image")
        answer = True
        userdata_size = "16"
        while answer:
            try:
                print("[1] 16gb Version")
                print("[2] 64gb Version")
                menu_choice = raw_input("Select size of device:")
                if menu_choice == 1:
                    userdata_size = "userdata.img"
                    answer = None
                if menu_choice == 2:
                    userdata_size = "userdata_64G.img"
                    answer = None
            except:
                print("Incorrect selection")
        os.system(fastboot + " flash sbl1 sbl1.mbn")
        time.sleep(3)
        os.system(fastboot + " flash dbi sdi.mbn")
        time.sleep(3)
        os.system(fastboot + " flash aboot emmc_appsboot.mbn")
        time.sleep(3)
        os.system(fastboot + " reboot-bootloader")
        time.sleep(5)
        os.system(fastboot + " flash modem NON-HLOS.bin")
        time.sleep(3)
        os.system(fastboot + " flash rpm rpm.mbn")
        time.sleep(3)
        os.system(fastboot + " flash tz tz.mbn")
        time.sleep(3)
        os.system(fastboot + " flash LOGO logo.bin")
        time.sleep(3)
        os.system(fastboot + " flash oppostanvbk static_nvbk.bin")
        time.sleep(3)
        os.system(fastboot + " reboot-bootloader")
        time.sleep(5)
        os.system(fastboot + " flash boot boot.img")
        time.sleep(3)
        os.system(fastboot + " flash recovery recovery.img")
        time.sleep(3)
        os.system(fastboot + " erase system")
        time.sleep(3)
        os.system(fastboot + " flash system system.img")
        time.sleep(3)
        os.system(fastboot + " erase userdata")
        time.sleep(3)
        os.system(fastboot + " flash userdata %s" % userdata_size)
        time.sleep(3)
        os.system(fastboot + " erase cache")
        time.sleep(3)
        os.system(fastboot + " flash cache cache.img")
        time.sleep(3)
        os.system(fastboot + " continue")
        time.sleep(3)
        print("OnePlus factory is flashed")


def over9001(adb, fastboot, platform, twrp, nethunter, supersu):
    '''
    This function is to used to flash SuperSU, TWRP, and Nethunter.
    '''

    if platform == "win32":
        nh_path = "nhzip\\" + nethunter
        twrp_path = "TWRP\\" + twrp
        supersu_path = "supersu\\supersu.zip"
    else:
        nh_path = "nhzip/" + nethunter
        twrp_path = "TWRP/" + twrp
        supersu_path = "supersu/supersu.zip"

    sdnh = "/sdcard/nethunter.zip"
    sdsu = "/sdcard/supersu.zip"

    # adb push -p nhzip/nhfilename.zip /sdcard/nethunter.zip
    print("Sending nethunter to /sdcard")
    os.system(adb + " push -p " + nh_path + " " + sdnh)
    time.sleep(3)
    # adb push -p supersu/supersu.zip /sdcard/supersu.zip
    print("Sending SuperSU to /sdcard")
    os.system(adb + " push -p " + supersu_path + " " + sdsu)
    time.sleep(3)

    # adb push -p supersu/supersu.zip /sdcard/supersu.zip
    os.system(adb + " push -p " + supersu_path + " " + sdsu)
    time.sleep(3)
    print("Rebooting into bootloader")
    os.system(adb + " reboot bootloader")
    time.sleep(5)
    print("Flashing TWRP recovery image")
    os.system(fastboot + " fastboot flash recovery " + twrp_path)
    time.sleep(3)
    print("Flashing TWRP done!")
    os.system(fastboot + " fastboot boot " + twrp_path)
    time.sleep(20)
    print("Booted into TWRP")
    print("Installing SuperSU")
    os.system(adb + ' shell "twrp install %s"' % sdsu)
    print("SuperSU installed")
    time.sleep(5)
    print("Installing Kali Nethunter")
    os.system(adb + ' shell "twrp install %s"' % sdnh)
    print("Kali Nethunter is installed")
    print("Rebooting into Kali Linux Nethunter")
    os.system(adb + " reboot")