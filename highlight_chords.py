import fitz  # PyMuPDF

def highlight_chords(input_pdf, output_pdf, key='Piano'):
    # Open the PDF file
    pdf_document = fitz.open(input_pdf)

    # Chord colors in RGB format (0-255)
    chord_colors = {
        "Piano": {
            "C©‹": (0.89, 0.12, 0.13),
            "D©‹": (0.62, 0.4, 0.18),
            "E©‹": (0.78, 0.78, 0.78),
            "F©‹": (0, 0.51, 0.79),
            "G©‹": (0.13, 0.13, 0.13),
            "A©‹": (0.99, 0.89, 0),
            "B©‹": (0.24, 0.68, 0.17),
            "H©‹": (0.24, 0.68, 0.17),
            "C©": (0.89, 0.12, 0.13),
            "D©": (0.62, 0.4, 0.18),
            "E©": (0.78, 0.78, 0.78),
            "F©": (0, 0.51, 0.79),
            "G©": (0.13, 0.13, 0.13),
            "A©": (0.99, 0.89, 0),
            "B©": (0.24, 0.68, 0.17),
            "H©": (0.24, 0.68, 0.17),
            "Cm": (0.89, 0.12, 0.13),
            "Dm": (0.62, 0.4, 0.18),
            "Em": (0.78, 0.78, 0.78),
            "Fm": (0, 0.51, 0.79),
            "Gm": (0.13, 0.13, 0.13),
            "Am": (0.99, 0.89, 0),
            "Bm↑": (0.24, 0.68, 0.17),
            "Hm↑": (0.24, 0.68, 0.17),
            "Bm": (0.24, 0.68, 0.17),
            "Hm": (0.24, 0.68, 0.17),
            "C‹": (0.89, 0.12, 0.13),
            "D‹": (0.62, 0.4, 0.18),
            "E‹": (0.78, 0.78, 0.78),
            "F‹": (0, 0.51, 0.79),
            "G‹": (0.13, 0.13, 0.13),
            "A‹": (0.99, 0.89, 0),
            "B‹": (0.24, 0.68, 0.17),
            "H‹": (0.24, 0.68, 0.17),
            "C": (0.89, 0.12, 0.13),
            "D": (0.62, 0.4, 0.18),
            "E": (0.78, 0.78, 0.78),
            "F": (0, 0.51, 0.79),
            "G": (0.13, 0.13, 0.13),
            "A": (0.99, 0.89, 0),
            "B": (0.24, 0.68, 0.17),
            "H": (0.24, 0.68, 0.17)
        },
        "Boomwhacker": {
            "C©‹": (1.0, 0.0, 0.0),
            "D©‹": (1.0, 0.65, 0.0),
            "E©‹": (1.0, 1.0, 0.0),
            "F©‹": (0.0, 0.5, 0.0),
            "G©‹": (0.0, 1.0, 1.0),
            "A©‹": (0.5, 0.0, 0.5),
            "B©‹": (1.0, 0.0, 1.0),
            "H©‹": (1.0, 0.0, 1.0),
            "C©": (1.0, 0.0, 0.0),
            "D©": (1.0, 0.65, 0.0),
            "E©": (1.0, 1.0, 0.0),
            "F©": (0.0, 0.5, 0.0),
            "G©": (0.0, 1.0, 1.0),
            "A©": (0.5, 0.0, 0.5),
            "B©": (1.0, 0.0, 1.0),
            "H©": (1.0, 0.0, 1.0),
            "Cm": (1.0, 0.0, 0.0),
            "Dm": (1.0, 0.65, 0.0),
            "Em": (1.0, 1.0, 0.0),
            "Fm": (0.0, 0.5, 0.0),
            "Gm": (0.0, 1.0, 1.0),
            "Am": (0.5, 0.0, 0.5),
            "Bm↑": (1.0, 0.0, 1.0),
            "Hm↑": (1.0, 0.0, 1.0),
            "Bm": (1.0, 0.0, 1.0),
            "Hm": (1.0, 0.0, 1.0),
            "C‹": (1.0, 0.0, 0.0),
            "D‹": (1.0, 0.65, 0.0),
            "E‹": (1.0, 1.0, 0.0),
            "F‹": (0.0, 0.5, 0.0),
            "G‹": (0.0, 1.0, 1.0),
            "A‹": (0.5, 0.0, 0.5),
            "B‹": (1.0, 0.0, 1.0),
            "H‹": (1.0, 0.0, 1.0),
            "C": (1.0, 0.0, 0.0),
            "D": (1.0, 0.65, 0.0),
            "E": (1.0, 1.0, 0.0),
            "F": (0.0, 0.5, 0.0),
            "G": (0.0, 1.0, 1.0),
            "A": (0.5, 0.0, 0.5),
            "B": (1.0, 0.0, 1.0),
            "H": (1.0, 0.0, 1.0)
        }
    }

    # Padding and line strength
    padding = 1
    line_strength = 2

    # Memorize starting coordinates to avoid duplicate borders
    processed_coordinates = set()
    index = 0
    # Loop through each page in the PDF
    for page_num in range(pdf_document.page_count):
        # Get the page
        page = pdf_document[page_num]

        # Loop through the chords and highlight them using search_for()
        for chord, color in chord_colors[key].items():
            # Use a case-sensitive search to find occurrences of the chord
            instances = page.search_for(chord)

            for instance in instances:
                # Extract the coordinates from the search result
                x0, y0, x1, y1 = instance

                # Adjust coordinates for padding and line strength
                x0 -= padding
                y0 -= padding
                x1 += padding
                y1 += padding

                # Extract the text inside the bounding box
                text_in_box = page.get_text("text", clip=(x0, y0, x1, y1)).strip()
                if '\n' in text_in_box:
                    text_in_box = text_in_box.split('\n')[1]

                # Check if the extracted text matches the chord exactly
                if chord == text_in_box:
                    index += 1
                    #print(page.get_text("text", clip=(x0, y0, x1, y1)))
                    #print(chord, '***', text_in_box, '***', instance, '***', index)
                    # Check if the starting coordinates have already been processed
                    if (x0, y0) not in processed_coordinates:
                        # Draw lines around the chord on the original page
                        page.draw_line((x0, y0), (x1, y0), color=color, width=line_strength)  # Top line
                        page.draw_line((x1, y0), (x1, y1), color=color, width=line_strength)  # Right line
                        page.draw_line((x0, y1), (x1, y1), color=color, width=line_strength)  # Bottom line
                        page.draw_line((x0, y0), (x0, y1), color=color, width=line_strength)  # Left line

                    # Memorize the starting coordinates
                    processed_coordinates.add((x0, y0))
                    
                # else:
                #     print(page.get_text("text", clip=(x0, y0, x1, y1)))

    # Save the modified PDF
    pdf_document.save(output_pdf)

    # Close the original PDF document
    pdf_document.close()

if __name__ == "__main__":
    input_pdf_file = "input.pdf"
    output_pdf_file = "output.pdf"

    highlight_chords(input_pdf_file, output_pdf_file)
