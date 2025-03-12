#!/usr/bin/env python

import sys
from pathlib import Path
import xml.etree.ElementTree as ET
import xml.dom.minidom

def main() -> None:
    # TODO: Refactoring and better error/exception handling
    try:
        infile = ''.join(sys.argv[1])
        tag_to_search = ''.join(sys.argv[2])
        target_path = ''.join(sys.argv[3])
    except Exception:
        print("Invalid input.")
        return

    try:
        tree = ET.parse(infile)
        root = tree.getroot()
    except ET.ParseError:
        print("Could not parse XML file.")
        return

    try:
        output_root = ET.Element(root.tag)
        outfile_list = target_path.split('/')
        path_to_outfile_list = outfile_list.copy()
        path_to_outfile_list.pop()
        path_to_outfile = '/'.join(path_to_outfile_list)
        Path(path_to_outfile).mkdir(exist_ok=True)
        outfile = outfile_list[-1]
    except Exception:
        print("Could not construct output path.")

    try:
        for item in root.findall(tag_to_search):
            children = list(item)

            if children:
                new_item = ET.Element(item.tag, attrib=item.attrib)
                for child in children:
                    new_item.append(child)
                output_root.append(new_item)
    except Exception:
        print("Could not filter XML file.")

    try:
        rough_string = ET.tostring(output_root, encoding='utf-8')
        parsed_xml = xml.dom.minidom.parseString(rough_string)
        formatted_xml = parsed_xml.toprettyxml(indent="  ")
        cleaned_xml = "\n".join([line for line in formatted_xml.split("\n") if line.strip()])

        with open(path_to_outfile + '/' + outfile, 'w', encoding='utf-8') as f:
            f.write(cleaned_xml)
    except Exception:
        print("Could not write to output file.")

if __name__ == '__main__':
    main()
