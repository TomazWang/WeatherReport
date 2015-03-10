# xml parsing exercise

import xml.etree.ElementTree as ET


xmlFile = open('./res/data.xml','rU')
xml = xmlFile.read()
xmlFile.close()

root = ET.fromstring(xml)
print 'root -> ',root

dataset = root.findall('.//dataid')
print 'dataset -> ',dataset