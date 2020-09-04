from enigma import *
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.GUIComponent import GUIComponent
from Components.HTMLComponent import HTMLComponent
from Tools.Directories import fileExists, crawlDirectory
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Button import Button
from Components.Label import Label
from Components.ConfigList import ConfigListScreen
from Components.config import ConfigSelection, getConfigListEntry, config
from Plugins.Extensions.spazeMenu.plugin import esHD
import os
import sys
import re

class HddInfo(ConfigListScreen, Screen):
    if esHD():
        skin = '\n\t\t<screen name="HddInfo" position="center,center" size="840,645" title="Hard Drive Info">\n\t\t<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/spazeMenu/imgvk/hdred.png" position="0,0" size="210,60" alphatest="blend" />\n\t\t<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/spazeMenu/imgvk/hdgreen.png" position="210,0" size="210,60" alphatest="blend" />\n\t\t<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/spazeMenu/imgvk/hdyellow.png" position="420,0" size="210,60" alphatest="blend" />\n\t\t<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/spazeMenu/imgvk/hdblue.png" position="630,0" size="210,60" alphatest="blend" />\n\t\t<widget name="key_red" position="0,0" zPosition="1" size="210,60" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="210,0" zPosition="1" size="210,60" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t<widget name="key_yellow" position="420,0" zPosition="1" size="210,60" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t<widget name="key_blue" position="630,0" zPosition="1" size="210,60" font="Regular;20" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />\n\t\t<widget font="Regular;18" halign="left" name="model" position="30,67" size="780,37" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="serial" position="30,112" size="780,37" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="firmware" position="30,157" size="780,37" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="cylinders" position="30,202" size="780,37" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="heads" position="30,247" size="780,37" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="sectors" position="30,292" size="780,37" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="readDisk" position="30,337" size="780,37" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="readCache" position="30,382" size="780,37" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="temp" position="30,427" size="780,37" valign="center" />\n\t\t<widget name="config" position="30,487" scrollbarMode="showOnDemand" size="780,45" itemHeight="42" />\n\t\t</screen>'
    else:
        skin = '\n\t\t<screen name="HddInfo" position="center,center" size="560,430" title="Hard Drive Info">\n\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,0" size="140,40" alphatest="on" />\n\t\t<ePixmap pixmap="skin_default/buttons/blue.png" position="420,0" size="140,40" alphatest="on" />\n\t\t<widget name="key_red" position="0,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t<widget name="key_green" position="140,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t<widget name="key_yellow" position="280,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t<widget name="key_blue" position="420,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />\n\t\t<widget font="Regular;18" halign="left" name="model" position="20,45" size="520,25" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="serial" position="20,75" size="520,25" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="firmware" position="20,105" size="520,25" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="cylinders" position="20,135" size="520,25" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="heads" position="20,165" size="520,25" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="sectors" position="20,195" size="520,25" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="readDisk" position="20,225" size="520,25" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="readCache" position="20,255" size="520,25" valign="center" />\n\t\t<widget font="Regular;18" halign="left" name="temp" position="20,285" size="520,25" valign="center" />\n\t\t<widget name="config" position="20,325" scrollbarMode="showOnDemand" size="520,30" />\n\t\t</screen>'

    def __init__(self, session, device):
        Screen.__init__(self, session)
        self.device = device
        self.list = []
        self.list.append(getConfigListEntry(_('Harddisk standby after'), config.usage.hdd_standby))
        ConfigListScreen.__init__(self, self.list)
        self['key_green'] = Button('')
        self['key_red'] = Button(_('Ok'))
        self['key_blue'] = Button(_('Exit'))
        self['key_yellow'] = Button('')
        self['model'] = Label(_('Model: unknown'))
        self['serial'] = Label(_('Serial: unknown'))
        self['firmware'] = Label(_('Firmware: unknown'))
        self['cylinders'] = Label(_('Cylinders: unknown'))
        self['heads'] = Label(_('Heads: unknown'))
        self['sectors'] = Label(_('Sectors: unknown'))
        self['readDisk'] = Label(_('Read disk speed: unknown'))
        self['readCache'] = Label(_('Read disk cache speed: unknown'))
        self['temp'] = Label(_('Disk temperature: unknown'))
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'blue': self.keyCancel,
         'red': self.keySave,
         'cancel': self.keyCancel}, -2)
        self.onLayoutFinish.append(self.drawInfo)
        self.onShown.append(self.setWindowTitle)

    def setWindowTitle(self):
        self.setTitle(_('Device Details'))

    def drawInfo(self):
        device = '/dev/%s' % self.device
        modelRe = re.compile('Model Number:\\s*([\\w\\-]+)')
        serialRe = re.compile('Serial Number:\\s*([\\w\\-]+)')
        firmwareRe = re.compile('Firmware Revision:\\s*([\\w\\-]+)')
        cylindersRe = re.compile('cylinders\\s*(\\d+)\\s*(\\d+)')
        headsRe = re.compile('heads\\s*(\\d+)\\s*(\\d+)')
        sectorsRe = re.compile('sectors/track\\s*(\\d+)\\s*(\\d+)')
        readDiskRe = re.compile('Timing buffered disk reads:\\s*(.*)')
        readCacheRe = re.compile('Timing buffer-cache reads:\\s*(.*)')
        tempRe = re.compile('%s:.*:(.*)' % device)
        os.system('/sbin/hdparm -S 0 %s' % device)
        hdparm = os.popen('/sbin/hdparm -I %s' % device)
        for line in hdparm:
            model = re.findall(modelRe, line)
            if model:
                self['model'].setText(_('Model: %s') % model[0].lstrip())
            serial = re.findall(serialRe, line)
            if serial:
                self['serial'].setText(_('Serial: %s') % serial[0].lstrip())
            firmware = re.findall(firmwareRe, line)
            if firmware:
                self['firmware'].setText(_('Firmware: %s') % firmware[0].lstrip())
            cylinders = re.findall(cylindersRe, line)
            if cylinders:
                self['cylinders'].setText(_('Cylinders: %s (max) %s (current)') % (cylinders[0][0].lstrip(), cylinders[0][1].lstrip()))
            heads = re.findall(headsRe, line)
            if heads:
                self['heads'].setText(_('Heads: %s (max) %s (current)') % (heads[0][0].lstrip(), heads[0][1].lstrip()))
            sectors = re.findall(sectorsRe, line)
            if sectors:
                self['sectors'].setText(_('Sectors: %s (max) %s (current)') % (sectors[0][0].lstrip(), sectors[0][1].lstrip()))

        hdparm.close()
        hdparm = os.popen('/sbin/hdparm -t %s' % device)
        for line in hdparm:
            readDisk = re.findall(readDiskRe, line)
            if readDisk:
                self['readDisk'].setText(_('Read speed: %s') % readDisk[0].lstrip())

        hdparm.close()
        hdparm = os.popen('/sbin/hdparm -T %s' % device)
        for line in hdparm:
            readCache = re.findall(readCacheRe, line)
            if readCache:
                self['readCache'].setText(_('Read cache speed: %s') % readCache[0].lstrip())

        hdparm.close()
        hddtemp = os.popen('/usr/sbin/hddtemp -q %s' % device)
        for line in hddtemp:
            temp = re.findall(tempRe, line)
            if temp:
                self['temp'].setText(_('Disk temperature: %s') % temp[0].lstrip())

        hddtemp.close()
