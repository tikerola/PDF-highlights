import fitz  # PyMuPDF
import re

def highlight_chords(input_pdf, output_pdf):
    # Open the PDF file
    pdf_document = fitz.open(input_pdf)

    # Chord colors in RGB format (0-255)
    chord_colors = {
        "E‹": (0, 0, 0),  # Yellow
        "A‹": (0, 0, 0),  # Yellow
        "CŒ„Š7": (0, 0, 0),  # Yellow
        "C": (1, 0, 0),     # Red
        "D/F©": (1, 0, 0),     # Red
        "D": (1, 0, 0),     # Red
        "GŒ„Š7": (0, 0, 0),  # Yellow
        "G": (1, 1, 0),      # Yellow
        # Add more chords and colors as needed
    }

    # Padding and line strength
    padding = 3
    line_strength = 2

    # Memorize starting coordinates to avoid duplicate borders
    processed_coordinates = set()

    # Loop through each page in the PDF
    for page_num in range(pdf_document.page_count):
        # Get the page
        page = pdf_document[page_num]

        # Loop through the chords and highlight them using search_for()
        for chord, color in chord_colors.items():
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

                # Check if the extracted text matches the chord exactly
                if text_in_box == chord:
                    # Check if the starting coordinates have already been processed
                    if (x0, y0) not in processed_coordinates:
                        # Draw lines around the chord on the original page
                        page.draw_line((x0, y0), (x1, y0), color=color, width=line_strength)  # Top line
                        page.draw_line((x1, y0), (x1, y1), color=color, width=line_strength)  # Right line
                        page.draw_line((x0, y1), (x1, y1), color=color, width=line_strength)  # Bottom line
                        page.draw_line((x0, y0), (x0, y1), color=color, width=line_strength)  # Left line

                        # Memorize the starting coordinates
                        processed_coordinates.add((x0, y0))

    # Save the modified PDF
    pdf_document.save(output_pdf)

    # Close the original PDF document
    pdf_document.close()

if __name__ == "__main__":
    input_pdf_file = "input.pdf"
    output_pdf_file = "output.pdf"

    highlight_chords(input_pdf_file, output_pdf_file)
