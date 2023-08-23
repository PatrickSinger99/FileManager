# -*- coding: utf-8 -*-

import os
from lxml import etree as ET


class DirectoryHandler:
    def __init__(self, root_directory):
        self.root_dir = root_directory  # Path to the root directory for all files to be synced
        self.save_file_path = "master_data.xml"  # Name/Path of the xml save file
        self.element_tree = None

        # Initialize element tree: Load from save file if exists, otherwise create new one
        self.initialize_tree()

    def build_element_tree(self):
        """
        Overwrite the current element tree with root directory structure
        """
        # Function to parse directory recursively. Returns an ET Element for the given folder
        def recurse_dir(dir_path):
            # Define return element with subelements and get directory data
            return_element = ET.Element("folder", name=os.path.basename(dir_path), path=dir_path)
            return_files_elem = ET.SubElement(return_element, "files")
            return_folders_elem = ET.SubElement(return_element, "folders")
            files, folders = self.get_dir_content(dir_path)

            # Run function recursively for every folder. Add returned elements as folder subelements
            for folder in folders:
                return_folders_elem.append(recurse_dir(os.path.join(dir_path, folder)))

            # Add single files of current directory to return element
            for file in files:
                ET.SubElement(return_files_elem, "file", name=file, path=os.path.join(dir_path, file))

            return return_element

        # Update element tree class variable with new element tree
        try:
            root = ET.Element("data", root_directory=self.root_dir)
            root.append(recurse_dir(self.root_dir))
            self.element_tree = ET.ElementTree(root)
        except Exception as e:
            print(f"(!) Save file creation failed due to the following reason: {e}")

    def update_element_tree(self):
        """
        Update the element tree by comparing it to the current state of the root directory
        """
        removed_counters = {"file": 0, "folder": 0}
        added_counters = {"file": 0, "folder": 0}

        # Remove elements that are no longer present in the root directory
        for elem in self.element_tree.iter():
            if elem.tag in ("folder", "file"):
                if not os.path.exists(elem.get("path")):
                    elem.getparent().remove(elem)  # Remove element if path does not exist anymore
                    removed_counters[elem.tag] += 1

        # Add elements that have been added to the root directory
        for elem in self.element_tree.iter():
            if elem.tag == "folder":
                tree_folders = [folder_elem.get("name") for folder_elem in elem.find("folders").getchildren()]
                current_folders = [obj for obj in os.listdir(elem.get("path")) if os.path.isdir(os.path.join(elem.get("path"), obj))]
                new_folders = [folder for folder in current_folders if folder not in tree_folders]

                for folder in new_folders:
                    folder_elem = self.recurse_dir(os.path.join(elem.get("path"), folder))
                    elem.find("folders").append(folder_elem)

                tree_files = [file_elem.get("name") for file_elem in elem.find("files").getchildren()]
                current_files = [obj for obj in os.listdir(elem.get("path")) if os.path.isfile(os.path.join(elem.get("path"), obj))]
                new_files = [file for file in current_files if file not in tree_files]

                for file in new_files:
                    elem.find("files").append("temp")

        print(removed_counters)

    def recurse_dir(self, dir_path):
        """
        Function to parse directory recursively. Returns an ET Element for the given folder
        :param dir_path:
        :return:
        """
        # Define return element with subelements and get directory data
        return_element = ET.Element("folder", name=os.path.basename(dir_path), path=dir_path)
        return_files_elem = ET.SubElement(return_element, "files")
        return_folders_elem = ET.SubElement(return_element, "folders")
        files, folders = self.get_dir_content(dir_path)

        # Run function recursively for every folder. Add returned elements as folder subelements
        for folder in folders:
            return_folders_elem.append(self.recurse_dir(os.path.join(dir_path, folder)))

        # Add single files of current directory to return element
        for file in files:
            ET.SubElement(return_files_elem, "file", name=file, path=os.path.join(dir_path, file))

        return return_element

    @staticmethod
    def get_dir_content(directory):
        """
        Gets folder and file names in the given directory path
        :param directory: path for directory to be searched
        :return: List of folder and file names (only names, no paths)
        """
        dir_content = os.listdir(directory)
        # Filter content by type (files & folders)
        files = [obj for obj in dir_content if os.path.isfile(os.path.join(directory, obj))]
        folders = [obj for obj in dir_content if os.path.isdir(os.path.join(directory, obj))]

        return files, folders

    def initialize_tree(self):
        """
        Load the tree structure from the save file. If not possible, create new one.
        """
        try:
            # Try to open save file and update element tree with its data
            with open(self.save_file_path, encoding='utf-8') as file:  # encoding specification necessary bc of Umlaute
                self.element_tree = ET.parse(file)
                print(f"Data loaded from {self.save_file_path}.")
        except:
            # If no save file could be read, create a new save file for the root directory
            print(f"No valid save file found. Creating new save file...")
            self.build_element_tree()
            self.update_save_file()

    def update_save_file(self):
        """
        Update/Create the save file with the current tree structure.
        """
        try:
            with open(self.save_file_path, "wb") as file:
                self.element_tree.write(file, encoding='utf-8', xml_declaration=True, pretty_print=True)
                print(f"Saved data under {self.save_file_path}.")
        except Exception as e:
            print(f"(!) Could not save data due to the following reason: {e}")


if __name__ == "__main__":
    root_dir = r"C:\Users\sip4abt\Documents\python_scripts\dir_scan_test\test"
    d = DirectoryHandler(root_dir)
    d.update_element_tree()
    d.update_save_file()
