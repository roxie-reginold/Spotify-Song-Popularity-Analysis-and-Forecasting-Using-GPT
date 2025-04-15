#!/usr/bin/env python3
"""
Convert Spotify recommendation training pairs from input/output format 
to the contents format required for fine-tuning.
"""
import json
import os

# Input and output files
INPUT_TRAINING = "spotify_recommendation_training_pairs.jsonl"
OUTPUT_TRAINING = "spotify_recommendation_training_fixed.jsonl"
INPUT_VALIDATION = "spotify_recommendation_validation.jsonl"
OUTPUT_VALIDATION = "spotify_recommendation_validation_fixed.jsonl"

def convert_file(input_file, output_file):
    """Convert a file from input/output format to contents format."""
    print(f"Converting {input_file} to {output_file}...")
    
    # Check if the file exists
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        return False
    
    converted_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        for line_num, line in enumerate(f_in, 1):
            try:
                # Parse the original JSON
                data = json.loads(line.strip())
                
                # Create the new format
                new_data = {
                    "contents": [
                        {
                            "role": "user",
                            "parts": [{"text": data.get("input", "")}]
                        },
                        {
                            "role": "model",
                            "parts": [{"text": data.get("output", "")}]
                        }
                    ]
                }
                
                # Write to the output file
                f_out.write(json.dumps(new_data) + "\n")
                converted_count += 1
                
            except json.JSONDecodeError:
                print(f"Warning: Line {line_num} in {input_file} is not valid JSON. Skipping.")
            except KeyError as e:
                print(f"Warning: Line {line_num} in {input_file} is missing key {e}. Skipping.")
            except Exception as e:
                print(f"Error processing line {line_num} in {input_file}: {e}")
    
    print(f"Successfully converted {converted_count} training pairs to {output_file}")
    return True

if __name__ == "__main__":
    # Convert training file
    convert_file(INPUT_TRAINING, OUTPUT_TRAINING)
    
    # Convert validation file if it exists
    if os.path.exists(INPUT_VALIDATION):
        convert_file(INPUT_VALIDATION, OUTPUT_VALIDATION)
        
    print("\nConversion complete!")
    print("The converted files are now ready for fine-tuning.")
