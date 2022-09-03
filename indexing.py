import os
import time
from lxml import etree as ET
from os.path import join, isfile, splitext, getsize, getmtime
import canny_detection


def parse_folder(folder_path, parent_element):
    try:
        folder_content = os.listdir(folder_path)
    except FileNotFoundError:
        print("    (!) Skipped " + folder_path + " because file name exceeded length limit")
        return

    file_count = 0
    subfolder_count = 0

    files_element = ET.SubElement(parent_element, "files")
    folders_element = ET.SubElement(parent_element, "folders")

    for file in folder_content:

        if isfile(join(folder_path, file)):
            ET.SubElement(files_element, "file",
                          name=file,
                          type=splitext(file)[-1][1:].upper(),
                          size=str(getsize(join(folder_path, file))),
                          modified=str(time.ctime(getmtime(join(folder_path, file)))),
                          compared="0",
                          full_path=str(join(folder_path, file))
                          ).text = canny_detection.get_canny_from_img(join(folder_path, file))

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
        print("\n>> Master data file creation started")
        root = ET.Element("root_directory", path=path)

        parse_folder(path, root)

        tree = ET.ElementTree(root)
        tree.write("master_data.xml", encoding='utf-8', xml_declaration=True, pretty_print=True)
        print("    (i) Successfully created master data file")

    except:
        print("    (!) Failed to create master data file")


def get_master_data_file_count(file_type=""):
    data = ET.parse("master_data.xml")
    count = 0

    if file_type == "":
        for elem in data.iter():
            if elem.tag == "folder":
                count += int(elem.get("file_count"))

    else:
        for elem in data.iter():
            if elem.tag == "file":
                if elem.get("type") == file_type.upper():
                    count += 1

    return count


def fetch_changes():
    print("\n>> Fetching changes...", end="")

    # Open master file
    with open("master_data.xml") as master_file:
        data = ET.parse(master_file)
        removed_files = 0
        removed_folders = 0
        removed_files_through_folder = 0

        # Parse through every element
        for elem in data.iter():

            # Folder element
            if elem.tag == "folder":
                # Delete xml folder element if folder not found in path
                if not os.path.exists(elem.get("full_path")):
                    parent = elem.getparent()
                    parent.remove(elem)
                    removed_files_through_folder += int(elem.get("file_count"))
                    removed_folders += 1

            # File element
            elif elem.tag == "file":
                # Delete xml file element if file not found in path
                if not os.path.exists(elem.get("full_path")):
                    parent = elem.getparent()
                    parent.remove(elem)
                    removed_files += 1
                # Delete xml file element if it has changed the properties size or modified date
                else:
                    if elem.get("size") != str(getsize(elem.get("full_path"))) or \
                            elem.get("modified") != str(time.ctime(getmtime(elem.get("full_path")))):
                        parent = elem.getparent()
                        parent.remove(elem)
                        removed_files += 1

        # Check for new files in system path
        root = data.getroot()
        folder_path = data.getroot().get("path")
        folder_content = os.listdir(folder_path)

        # Get all elements in xml folder
        all_xml_folder_content = []
        for file in root.find("files"):
            all_xml_folder_content.append(file.get("full_path"))
        for folder in root.find("folders"):
            all_xml_folder_content.append(folder.get("full_path"))

        for element in folder_content:
            if join(folder_path, element) not in all_xml_folder_content:
                pass

        # Save new master file
        data.write("master_data.xml", encoding='utf-8', xml_declaration=True, pretty_print=True)

    # Print results
    print("finished.")
    if removed_files == 1:
        print("    1 file removed")
    else:
        print("    " + str(removed_files) + " files removed")

    if removed_folders == 0:
        print("    0 folders removed")
    else:
        if removed_folders == 1:
            print("    1 folder removed, ", end="")
        else:
            print("    " + str(removed_folders) + " folders removed, ", end="")

        if removed_files_through_folder == 1:
            print("including 1 file")
        else:
            print("including " + str(removed_files_through_folder) + " files")


if __name__ == "__main__":
    create_master_data_xml(r"E:\=Eigene Dateien=\Bilder\Verschiedene Bilder\xd")
    # fetch_changes()
