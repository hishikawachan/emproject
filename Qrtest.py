import xml.etree.ElementTree as ET

xml_path = "label.xml"
output_path = "abel_modified.xml"

# XML読み込み
tree = ET.parse(xml_path)
root = tree.getroot()

# 名前空間を定義（※ 実際のURIに合わせて変更）
namespaces = {
    "pt": "http://schemas.brother.info/ptouch/2007/lbx/main" 
}

# <pt:data> をすべて書き換え
for elem in root.findall(".//pt:data", namespaces):
    elem.text = "test-a"

# 保存
tree.write(output_path, encoding="utf-8", xml_declaration=True)

print("完了:", output_path)
