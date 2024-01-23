import xml.etree.ElementTree as ET
import os


def xml_to_tex(xml_files, tex_file):
    try:
        def create_content(xml_file, content_type):
            xml_file = "./input/" + xml_file
            tree = ET.parse(xml_file)
            root = tree.getroot()

            title = os.path.splitext(xml_file)[0]

            if not list(root):
                raise ValueError(f"Plik {xml_file} XML nie zawiera odpowiednich danych.")

            # Tworzenie nazw kolumn
            col_header = []
            for child in root:
                for data in child:
                    tag = data.tag
                    if tag not in col_header:
                        col_header.append(tag)

            content = ""
            # Tworzenie tabeli
            if content_type == "table":
                content += "\\section*{" + title.capitalize() + "}\n"
                content += "\\begin{tabular}{" + "|c" * len(col_header) + "|}\n\\hline\n"
                content += " & ".join(col_header) + "\\\\ \\hline\n"
                for child in root:
                    if any(data.text for data in child):
                        row_data = [
                            child.find(tag).text.replace("$", "\\$") if child.find(tag) is not None and child.find(
                                tag).text is not None else "N/A"
                            for tag in col_header
                        ]
                        content += " & ".join(row_data) + "\\\\ \\hline\n"
                content += "\\end{tabular}\n\\vspace{1cm}\n"

            # Tworzenie list
            elif content_type == "itemize" or content_type == "enumerate":
                content += "\\section*{" + title.capitalize() + "}\n"
                content += "\\begin{" + content_type + "}\n"
                for child in root:
                    list_item_values = [
                        data.text.replace("$", "\\$") if data.text is not None else "N/A"
                        for data in child
                    ]
                    if any(value != "N/A" for value in list_item_values):
                        list_item = ", ".join(list_item_values)
                        content += "\\item " + list_item + "\n"
                content += "\\end{" + content_type + "}\n\\vspace{1cm}\n"

            return content

        latex_body = "\\documentclass{article}\n\\usepackage[margin=1cm]{geometry}\n\\usepackage{tabularx}\n\\begin{document}\n"
        latex_body += "\\begin{center}\n"

        # Łączenie wszystkich tabel i list w jedną całość
        for xml_file, content_type in xml_files:
            content = create_content(xml_file, content_type)
            if content:
                latex_body += content

        latex_body += "\\end{center}\n\\end{document}"

        # Zapisywanie do pliku
        with open(tex_file, 'w') as file:
            file.write(latex_body)

    except ET.ParseError:
        return "Błąd: Plik XML może być źle sformatowany."
    except FileNotFoundError:
        return "Błąd: Plik nie został znaleziony."
    except ValueError as ve:
        return str(ve)
    except Exception as e:
        return "Nieoczekiwany błąd: " + str(e)


if __name__ == "__main__":
    xml_files = [("plants.xml", "table"), ("fruits.xml", "itemize"),
                 ("fruits.xml", "enumerate")]  # [(INPUT, TYPE(table, itemize, enumerate))]
    xml_to_tex(xml_files, "./output/result.tex")
