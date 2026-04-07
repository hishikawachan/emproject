import xml.etree.ElementTree as ET
from pprint import pprint
#ns = {'pt':'http://schemas.brother.info/ptouch/2007/lbx/main','style':'http://schemas.brother.info/ptouch/2007/lbx/style','text':'http://schemas.brother.info/ptouch/2007/lbx/text','draw':'http://schemas.brother.info/ptouch/2007/lbx/draw', 'image':'http://schemas.brother.info/ptouch/2007/lbx/image', 'barcode':'http://schemas.brother.info/ptouch/2007/lbx/barcode','database':'http://schemas.brother.info/ptouch/2007/lbx/database','table':'http://schemas.brother.info/ptouch/2007/lbx/table','cable':'http://schemas.brother.info/ptouch/2007/lbx/cable'}

ns = {'pt': 'http://schemas.brother.info/ptouch/2007/lbx/main'}
tree = ET.parse(r"C:\Users\hishi\OneDrive\Labo\em\emproject\src\label.xml")
root = tree.getroot()

# pt:objects以下を取得したい
fmeNodes = root.findall('pt:document', ns)

records = []
#for itemNode in fmeNodes:
#    pprint ("pt:data = " + itemNode.find('barcode:barcode/pt:objectStyle/pt:data', ns).text.strip())
