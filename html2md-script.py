#pip install markdownify
import os
import argparse
from markdownify import markdownify as md
from concurrent.futures import ThreadPoolExecutor, as_completed

def convert_html_to_md(html_file, output_dir):
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        markdown_content = md(html_content)
        
        base_name = os.path.basename(html_file)
        md_file = os.path.splitext(base_name)[0] + '.md'
        output_path = os.path.join(output_dir, md_file)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Converted {html_file} to {output_path}")
    except Exception as e:
        print(f"Error converting {html_file}: {str(e)}")

def main(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    html_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.html')]
    
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(convert_html_to_md, html_file, output_dir) for html_file in html_files]
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert HTML files to Markdown")
    parser.add_argument("input_dir", help="Directory containing HTML files")
    parser.add_argument("output_dir", help="Directory to save Markdown files")
    args = parser.parse_args()

    main(args.input_dir, args.output_dir)
