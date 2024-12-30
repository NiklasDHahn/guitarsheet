from fpdf import FPDF
import os
import argparse


class SongParser:
    def __init__(self, input_file):
        self.input_file = input_file
        self.title = "Unkown"
        self.author = "Unkown"
        self.date = "xx.xx.xxxx"
        self.tuning = "Unkown"
        self.chords = {}
        self.abelton_settings = {}
        self.sections = []
        self.lines = {}
        self.capo = None

    def parse(self):
        with open(self.input_file, "r") as file:
            lines = file.readlines()

        lines = [line for line in lines if line.strip()]
        current_section = None
        song_sections = [
            "Verse",
            "Chorus",
            "Bridge",
            "Interlude",
            "Intro",
            "Pre-Chorus",
        ]
        song_line = 1
        for line in lines:
            line = line.strip()
            if line.startswith("Date:"):
                self.date = line.split("Date:")[1].strip()
            elif line.startswith("Author:"):
                self.author = line.split("Author:")[1].strip()
            elif line.startswith("Title:"):
                self.title = line.split("Title:")[1].strip()
            elif line.startswith("Tuning:"):
                self.tuning = line.split("Tuning:")[1].strip()
            elif line.startswith("Capo:"):
                self.capo = line.split("Capo:")[1].strip()
            elif line.startswith("[") and line.endswith("]"):
                current_section = line.strip("[]")
                self.sections.append(current_section)
            elif current_section == "Chords":
                chord = line.split("|")
                chord_name, chord_shape = chord[0].strip(), chord[1].strip()
                self.chords[chord_name.strip()] = "|" + chord_shape.strip() + "|"
            elif current_section == "Abelton Live Settings":
                option = line.split(":")
                option_name, option_value = option[0].strip(), option[1].strip()
                self.abelton_settings[option_name] = option_value
            elif current_section.split(" ")[0] in song_sections:
                self.lines[song_line] = (current_section, line)
                song_line += 1
            else:
                pass

    def generate_pdf(self, output_file):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=17)

        pdf.cell(200, 10, txt=self.title, ln=True, align="C")
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 5, txt=f"Author: {self.author}", ln=True, align="L")
        pdf.cell(200, 5, txt=f"Date: {self.date}", ln=True, align="L")
        pdf.cell(200, 5, txt=f"Tuning: {self.tuning}", ln=True, align="L")
        if self.capo:
            pdf.cell(200, 5, txt=f"Capo: {self.capo}", ln=True, align="L")

        pdf.set_font("Arial", size=12)
        for section in self.sections:
            pdf.cell(200, 10, txt=f"[{section}]", ln=True, align="L")
            if section == "Chords":
                for chord, shape in self.chords.items():
                    pdf.cell(50, 5, txt=f"{chord}", ln=False, align="L")
                    pdf.set_x(40)  # Set the x-coordinate for the shape values
                    pdf.cell(0, 5, txt=f"{shape}", ln=True, align="L")
            elif section == "Abelton Live Settings":
                for option, value in self.abelton_settings.items():
                    pdf.cell(50, 5, txt=f"{option}: {value}", ln=True, align="L")
            else:
                pdf.set_font("Courier", size=12)
                section_lines = [
                    content
                    for _, (sec, content) in self.lines.items()
                    if sec == section
                ]
                for line in section_lines:
                    line = line.replace("\t", "    ")
                    pdf.cell(200, 5, txt=line, ln=True, align="L")
            pdf.set_font("Arial", size=12)

        pdf.output(output_file)

    def generate_html(self, output_file):
        html_content = f"<h1>{self.title}</h1>\n\n"
        html_content += f"<strong>Author:</strong> {self.author}<br>\n"
        html_content += f"<strong>Date:</strong> {self.date}<br>\n"
        html_content += f"<strong>Tuning:</strong> {self.tuning}<br>\n"
        if self.capo:
            html_content += f"<strong>Capo:</strong> {self.capo}<br>\n"

        # Add dropdown list for each section
        html_content += '<select onchange="location = this.value;">\n'
        html_content += '<option value="#">Select Section</option>\n'
        for section in self.sections:
            html_content += f'<option value="#{section}">{section}</option>\n'
        html_content += "</select>\n"

        # Add button to scroll to the top
        html_content += """
        <button onclick="scrollToTop()" style="position:fixed;bottom:10px;right:10px;">Back to Top</button>
        <script>
        function scrollToTop() {
            window.scrollTo({top: 0, behavior: 'smooth'});
        }
        </script>
        """

        for section in self.sections:
            html_content += f"<h2 id='{section}'>[{section}]</h2>\n"
            if section == "Chords":
                for chord, shape in self.chords.items():
                    html_content += f"<pre>{chord}\t{shape}</pre>\n"
            elif section == "Abelton Live Settings":
                for option, value in self.abelton_settings.items():
                    html_content += f"<pre>{option}: {value}</pre>\n"
            else:
                section_lines = [
                    content
                    for _, (sec, content) in self.lines.items()
                    if sec == section
                ]
                for line in section_lines:
                    line = line.replace("\t", "    ")
                    for chord in self.chords:
                        line = line.replace(
                            chord, f"<span style='color:blue'>{chord}</span>"
                        )
                    html_content += f"<pre>{line}</pre>\n"

        with open(output_file, "w") as file:
            file.write(html_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process song file and generate PDF and HTML."
    )
    parser.add_argument("input_file", type=str, help="Path to the input text file")
    parser.add_argument(
        "output_dir", type=str, help="Directory to save the PDF and HTML files"
    )
    args = parser.parse_args()

    input_file = args.input_file
    output_dir = args.output_dir

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    pdf_output_file = os.path.join(output_dir, f"{base_name}.pdf")
    html_output_file = os.path.join(output_dir, f"{base_name}.html")

    parser = SongParser(input_file)
    parser.parse()
    parser.generate_pdf(pdf_output_file)
    parser.generate_html(html_output_file)
