import os
import xml.etree.cElementTree as ET
from xml.dom import minidom


def generateForm(path, hashkey, matcaps, matcap_path):
    configuration = ET.Element("configuration")
    attribute = ET.SubElement(configuration, "atom", type='Attributes')

    sheet = ET.SubElement(attribute, "hash", type='Sheet', key="%s:sheet" % hashkey)

    ET.SubElement(sheet, "atom", type="Label").text = "Tila_Matcaps"
    ET.SubElement(sheet, "atom", type="Desc").text = ""
    ET.SubElement(sheet, "atom", type="Tooltip").text = ""
    ET.SubElement(sheet, "atom", type="Help").text = ""
    ET.SubElement(sheet, "atom", type="ShowLabel").text = "1"
    ET.SubElement(sheet, "atom", type="PopupFace").text = "option"
    ET.SubElement(sheet, "atom", type="Enable").text = "1"
    ET.SubElement(sheet, "atom", type="Alignment").text = "default"
    ET.SubElement(sheet, "atom", type="Style").text = "inline"
    ET.SubElement(sheet, "atom", type="Export").text = "0"
    ET.SubElement(sheet, "atom", type="Filter").text = ""
    ET.SubElement(sheet, "atom", type="Layout").text = "vtoolbar"
    ET.SubElement(sheet, "atom", type="Justification").text = "left"
    ET.SubElement(sheet, "atom", type="Columns").text = "1"
    ET.SubElement(sheet, "atom", type="IconMode").text = "both"
    ET.SubElement(sheet, "atom", type="IconSize").text = "large"
    ET.SubElement(sheet, "atom", type="IconImage").text = ""
    ET.SubElement(sheet, "atom", type="IconResource").text = ""
    ET.SubElement(sheet, "atom", type="StartCollapsed").text = "0"
    ET.SubElement(sheet, "atom", type="EditorColor").text = "none"
    ET.SubElement(sheet, "atom", type="Proficiency").text = "basic"
    ET.SubElement(sheet, "atom", type="Group").text = "Tilapiatsu/Tila_MatcapManager"

    for m in range(len(matcaps)):
        list = ET.SubElement(sheet, "list", type="Control", val='cmd tila.matcap.manager %s' % m)
        ET.SubElement(list, "atom", type="ShowWhenDisabled").text = "1"
        ET.SubElement(list, "atom", type="booleanStyle").text = "default"
        ET.SubElement(list, "atom", type="Enable").text = "1"
        ET.SubElement(list, "atom", type="Label").text = os.path.splitext(matcaps[m])[0]
        ET.SubElement(list, "atom", type="Help").text = ""
        ET.SubElement(list, "atom", type="Tooltip").text = ""
        ET.SubElement(list, "atom", type="Desc").text = ""
        ET.SubElement(list, "atom", type="ShowLabel").text = "1"
        ET.SubElement(list, "atom", type="PopupFace").text = "option"
        ET.SubElement(list, "atom", type="Alignment").text = "default"
        ET.SubElement(list, "atom", type="Style").text = "default"
        ET.SubElement(list, "atom", type="IconImage").text = os.path.join(matcap_path, matcaps[m])
        ET.SubElement(list, "atom", type="IconResource").text = ""
        ET.SubElement(list, "atom", type="StartCollapsed").text = "0"
        ET.SubElement(list, "atom", type="Proficiency").text = "basic"
        ET.SubElement(list, "atom", type="ProficiencyOverride").text = "default"

    indent(configuration)

    tree = ET.ElementTree(configuration)

    tree.write(os.path.join(path, "MatcapsForm.cfg"), method='xml', encoding='utf-8', xml_declaration=True)


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


def indent(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i