from bs4 import BeautifulSoup

def html_to_pug(html):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Convert HTML to Pug
    def convert_tag(tag, indent_level=0):
        # Ensure we only process actual tags (not Doctype or other non-tag elements)
        if isinstance(tag, str):
            return tag  # If it's a text node, just return the text
        
        tag_name = tag.name
        attributes = tag.attrs
        
        # Handle self-closing tags
        if tag_name in ['br', 'img', 'hr', 'input', 'link', 'meta', 'area']:
            if attributes:
                attributes_str = ' '.join([f'{key}="{value}"' for key, value in attributes.items()])
                return f"{'  ' * indent_level}{tag_name} {attributes_str}"
            else:
                return f"{'  ' * indent_level}{tag_name}"
        
        # For other tags, handle indentation and attributes
        indent = "  " * indent_level
        attribute_str = ' '.join([f'{key}="{value}"' for key, value in attributes.items()]) if attributes else ''
        content = ''.join([convert_tag(child, indent_level + 1) for child in tag.children])  # Increase indent level for children
        
        if content:
            if attribute_str:
                return f"{indent}{tag_name}({attribute_str})\n{content}"
            else:
                return f"{indent}{tag_name}\n{content}"
        else:
            if attribute_str:
                return f"{indent}{tag_name}({attribute_str})"
            else:
                return f"{indent}{tag_name}"

    # Start the conversion with the root tag
    pug_code = convert_tag(soup)
    return pug_code.strip()

# Read the HTML file
def convert_html_file_to_pug(input_file, output_file):
    with open(input_file, 'r') as f:
        html_content = f.read()

    pug_content = html_to_pug(html_content)
    
    with open(output_file, 'w') as f:
        f.write(pug_content)

    print(f"Conversion complete! Pug code has been saved to {output_file}")



# Example Usage
input_file = 'views/index.html'  # Your HTML file path
output_file = 'views/output.pug'  # Pug file output path
convert_html_file_to_pug(input_file, output_file)
