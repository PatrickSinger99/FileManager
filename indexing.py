import os
import time
from lxml import etree as ET
from os.path import join, isfile, splitext, getsize, getmtime


def parse_folder(folder_path, parent_element):
    folder_content = os.listdir(folder_path)
    file_count = 0
    subfolder_count = 0

    files_element = ET.SubElement(parent_element, "files")
    folders_element = ET.SubElement(parent_element, "folders")

    for file in folder_content:

        if isfile(join(folder_path, file)):
            ET.SubElement(files_element, "file",
                          type=splitext(file)[-1][1:].upper(),
                          size=str(getsize(join(folder_path, file))),
                          modified=str(time.ctime(getmtime(join(folder_path, file))))
                          ).text = file

            file_count += 1

        else:
            subfolder = ET.SubElement(folders_element, "folder", name=file)
            counters = parse_folder(join(folder_path, file), subfolder)

            subfolder.set("file_count", str(counters[0]))
            subfolder.set("subfolder_count", str(counters[1]))
            subfolder.set("full_path", join(folder_path, file))

            subfolder_count += 1

    return [file_count, subfolder_count]


def create_master_data_xml(path):
    try:
        print("(i) Master data file creation started")
        root = ET.Element("root_directory", path=path)

        parse_folder(path, root)

        tree = ET.ElementTree(root)
        tree.write("master_data.xml", encoding='utf-8', xml_declaration=True, pretty_print=True)
        print("(i) Successfully created master data file")

    except:
        print("(!) Failed to create master data file")


if __name__ == "__main__":
    create_master_data_xml(r"E:\=Eigene Dateien=")
