
import json
import sys
import re
from html.parser import HTMLParser

class HTMLToMarkdownParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.md = ""
        self.in_table = False
        self.table_rows = []
        self.current_row = []
        self.in_cell = False
        self.cell_content = ""
        self.links = []
        self.list_depth = 0
        self.in_list_item = False

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.md += "\n"
        elif tag == 'strong' or tag == 'b':
            self.md += "**"
        elif tag == 'em' or tag == 'i':
            self.md += "_"
        elif tag == 'a':
            href = dict(attrs).get('href')
            if href:
                self.links.append(href)
                self.md += "["
        elif tag == 'ul' or tag == 'ol':
            self.list_depth += 1
            self.md += "\n"
        elif tag == 'li':
            self.in_list_item = True
            self.md += "  " * (self.list_depth - 1) + "- "
        elif tag == 'table':
            self.in_table = True
            self.table_rows = []
        elif tag == 'tr':
            if self.in_table:
                self.current_row = []
        elif tag == 'td' or tag == 'th':
            if self.in_table:
                self.in_cell = True
                self.cell_content = ""
        elif tag == 'br':
            self.md += "\n"

    def handle_endtag(self, tag):
        if tag == 'p':
            self.md += "\n"
        elif tag == 'strong' or tag == 'b':
            self.md += "**"
        elif tag == 'em' or tag == 'i':
            self.md += "_"
        elif tag == 'a':
            self.md += "]"
            # check the last added link to complete the markdown format
            if self.links:
                 self.md += f"({self.links[-1]})"
        elif tag == 'ul' or tag == 'ol':
            self.list_depth -= 1
            self.md += "\n"
        elif tag == 'li':
            self.in_list_item = False
            self.md += "\n"
        elif tag == 'table':
            self.in_table = False
            self.md += self._render_table()
        elif tag == 'tr':
            if self.in_table:
                self.table_rows.append(self.current_row)
        elif tag == 'td' or tag == 'th':
            if self.in_table:
                self.in_cell = False
                self.current_row.append(self.cell_content.strip())

    def handle_data(self, data):
        if self.in_cell:
            self.cell_content += data
        else:
            self.md += data

    def _render_table(self):
        if not self.table_rows:
            return ""
        
        # Calculate max width for each column
        # Simplified: just join with pipes
        output = "\n"
        
        # Header
        if self.table_rows:
             header = self.table_rows[0]
             output += "| " + " | ".join(header) + " |\n"
             output += "| " + " | ".join(["---"] * len(header)) + " |\n"
             
             for row in self.table_rows[1:]:
                 output += "| " + " | ".join(row) + " |\n"
        
        output += "\n"
        return output

def parse_html(html_content):
    if not html_content:
        return "", []
    parser = HTMLToMarkdownParser()
    parser.feed(html_content)
    return parser.md, parser.links

def main():
    if len(sys.argv) < 2:
        print("Usage: python jira_parser_custom.py <json_file>")
        sys.exit(1)

    json_path = sys.argv[1]
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Extract Basic fields
    key = data.get('key', '')
    fields = data.get('fields', {})
    summary = fields.get('summary', '')
    created = fields.get('created', '')
    
    rendered = data.get('renderedFields', {})
    description_html = rendered.get('description', '')
    
    # Parse Description
    description_md, desc_links = parse_html(description_html)
    
    # Extract Comments
    comments_md = ""
    comment_links = []
    
    # Handle comments structure
    # In renderedFields, comments might be data['renderedFields']['comment']['comments']
    rendered_comments = rendered.get('comment', {}).get('comments', [])
    
    for comment in rendered_comments:
        author = comment.get('author', {}).get('displayName', 'Unknown')
        updated = comment.get('updated', '')
        body_html = comment.get('body', '')
        
        c_md, c_links = parse_html(body_html)
        comment_links.extend(c_links)
        
        comments_md += f"### Comment by {author} ({updated})\n\n{c_md}\n\n"

    # Transaction Limits - Extraction from Description MD
    # Simple regex for now, better to let user refine
    limits_section = ""
    if "Limits per transaction" in description_md:
        try:
             # Basic extraction - grab lines around "Limits per transaction"
             # This is a heuristic.
             # Alternatively, just dumping the whole description covers it.
             pass
        except:
             pass

    # Questions section
    # The table in description is likely the Q&A.
    # We already converted the table to MD in description_md.
    # We can try to extract just the Q&A table if we want a separate section, 
    # but the instructions say "Description... [Full converted description content...]"
    # AND "Integration Details - Q&A ... [The main Q&A table extracted...]"
    # If the Q&A table is part of description, it's redundant to print it twice.
    # However, structuring it as requested:
    
    qa_table_md = ""
    # Try to find the Markdown table starting with | Questions | Answers |
    qa_match = re.search(r'(\| Questions \| Answers \|[\s\S]*?)(?=\n\n|\Z)', description_md)
    if qa_match:
        qa_table_md = qa_match.group(1)
        # We might want to remove it from description if we move it?
        # The prompt says "Full converted description content".
        # I'll leave it in description for completeness and also put it in Q&A section.
    
    # Transaction Limits
    # Extract lines containing "Limits" and subsequent lines with numbers
    t_limits = []
    lines = description_md.split('\n')
    capture_limit = False
    for line in lines:
        if "Limits" in line or "min " in line or "max " in line:
            if re.search(r'\d', line):
                 t_limits.append(line.strip())
    
    limits_md = "\n".join(["- " + l for l in t_limits if l])

    # All Links
    all_links = sorted(list(set(desc_links + comment_links)))
    links_md = "\n".join([f"- {l}" for l in all_links])

    # Final Markdown Construction
    output = f"""# BizDev Integration Request: {summary}

- **Jira Link**: https://4billio.atlassian.net/browse/{key}
- **Issue Key**: {key}
- **Created At**: {created}

## Description

{description_md}

## Transaction Limits

{limits_md}

## Integration Details - Q&A

{qa_table_md}

## Other

## Comments

{comments_md}

## Key Links

{links_md}
"""
    print(output)

if __name__ == "__main__":
    main()
