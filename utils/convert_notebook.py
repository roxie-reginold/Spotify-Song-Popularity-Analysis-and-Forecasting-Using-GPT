import json

# Function to extract code from Jupyter notebook
def convert_notebook_to_py(notebook_path, output_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Add imports at the top
        f.write("# Generated from Jupyter notebook\n")
        f.write("# Run this script with: python Spotify_Analysis.py\n\n")
        
        # Add import for load_env.py
        f.write("# Load environment variables\n")
        f.write("from load_env import *\n\n")
        
        # Extract and write code cells
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source'])
                # Skip cells that are just comments or empty
                if source.strip() and not source.strip().startswith('#'):
                    # Add a newline after each cell for better readability
                    f.write(source + '\n\n')
        
        print(f"Converted {notebook_path} to {output_path}")

if __name__ == "__main__":
    notebook_path = "Spotify_Analysis.ipynb"
    output_path = "Spotify_Analysis.py"
    convert_notebook_to_py(notebook_path, output_path)
