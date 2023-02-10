import wmi

# cpu_list = c.Win32_Processor()
# for cpu in cpu_list:
#   print (cpu)


class SystemUtil:
    _system = wmi.WMI()

    def getCpu(self):
        tmpdict = {}
        tmpdict['cpi_cores'] = 0
        for cpu in self._system.Win32_Processor():
            tmpdict['cpuid'] = cpu.ProcessorId
            tmpdict['cpu_type'] = cpu.Name
            tmpdict['ststem_name'] = cpu.SystemName
            try:
                tmpdict['cpi_cores'] = cpu.NumberOfCores
            except:
                tmpdict['cpi_cores'] += 1
                tmpdict['cpu_clock'] = cpu.MaxClockSpeed
                tmpdict['data_width'] = cpu.DataWidth
        return tmpdict['cpuid']

    # def getDisk(self):
    #     num = ''
    #     for disk in self._system.Win32_DiskDrive():
    #         num = num + disk.SerialNumber
    #     return num.strip()

    def getBoard(self):
        num = ''
        for board in self._system.Win32_BaseBoard():
            num = num + board.SerialNumber
        return num.strip()

    # def getMac(self):
    #     num = ''
    #     for mac in self._system.Win32_NetworkAdapter():
    #         if(mac.MACAddress):
    #             num = num + str(mac.MACAddress)
    #     return num.strip()

    # def getBios(self):
    #     num = ''
    #     for bios in c.Win32_BIOS():
    #         num = num + bios.SerialNumber.strip()
    #         print(bios)
    #     return num.strip()

    def uuid(self):
        cpuid = self.getCpu()
        boardid = self.getBoard()
        # diskid = self.getDisk()
        # macid = self.getMac()
        # biosid = self.getBios()
        # uuid = cpuid + diskid + boardid + macid
        uuid = cpuid + boardid
        return uuid