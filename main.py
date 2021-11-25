import indexing
import comparison
import xml.etree.ElementTree as ET


data = ET.parse("master_data.xml")
path = "E:\=Eigene Dateien=\Bilder\Verschiedene Bilder\Whats App\Bilder\Sent"

all_files = []
for elem in data.iter():

    if elem.tag == "folder":

        if elem.get("full_path") == path:
            files_elem = elem.find("files")
            files = files_elem.findall("file")

            for file in files:
                all_files.append([file.get("name"), file.text])

            break

comparison.compare_list(all_files)