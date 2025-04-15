#!/usr/bin/env python3
"""
Convert Spotify recommendation training pairs to the Vertex AI Gemini format.
This follows the official Vertex AI documentation for supervised fine-tuning.
"""
import json
import os

# Input and output files
INPUT_TRAINING = "spotify_recommendation_training_pairs.jsonl"
OUTPUT_TRAINING = "spotify_recommendation_vertex_ai.jsonl"
INPUT_VALIDATION = "spotify_recommendation_validation.jsonl"
OUTPUT_VALIDATION = "spotify_recommendation_vertex_ai_validation.jsonl"

def convert_to_vertex_ai_format(input_file, output_file):
    """Convert a file from input/output format to Vertex AI Gemini format."""
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
                
                # Create the new format according to Vertex AI documentation
                # Basic structure is:
                # {
                #   "contents": [
                #     {"role": "user", "parts": [{"text": "input text"}]},
                #     {"role": "model", "parts": [{"text": "output text"}]}
                #   ]
                # }
                
                input_text = data.get("input", "")
                output_text = data.get("output", "")
                
                # Optional: Add system instruction for better guidance
                system_instruction = {
                    "systemInstruction": {
                        "role": "system",
                        "parts": [
                            {
                                "text": "You are a music recommendation assistant specialized in Spotify songs. Provide personalized song recommendations based on user preferences, including detailed explanations that reference track popularity, playlist metrics, and chart rankings."
                            }
                        ]
                    }
                }
                
                # The core training data
                new_data = {
                    "contents": [
                        {
                            "role": "user",
                            "parts": [{"text": input_text}]
                        },
                        {
                            "role": "model",
                            "parts": [{"text": output_text}]
                        }
                    ]
                }
                
                # Combine system instruction with contents
                # Note: Only include system instruction for models that support it
                # For gemini-1.5-flash, include the systemInstruction
                combined_data = {**system_instruction, **new_data}
                
                # Write to the output file
                f_out.write(json.dumps(combined_data) + "\n")
                converted_count += 1
                
            except json.JSONDecodeError:
                print(f"Warning: Line {line_num} in {input_file} is not valid JSON. Skipping.")
            except KeyError as e:
                print(f"Warning: Line {line_num} in {input_file} is missing key {e}. Skipping.")
            except Exception as e:
                print(f"Error processing line {line_num} in {input_file}: {e}")
    
    print(f"Successfully converted {converted_count} examples to {output_file}")
    return True

# Alternate version without system instructions (for models that don't support it)
def convert_to_vertex_ai_format_basic(input_file, output_file):
    """Convert to Vertex AI format without system instructions."""
    print(f"Converting {input_file} to basic format (no system instructions) at {output_file}...")
    
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found.")
        return False
    
    converted_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        for line_num, line in enumerate(f_in, 1):
            try:
                data = json.loads(line.strip())
                
                input_text = data.get("input", "")
                output_text = data.get("output", "")
                
                # Only include contents without system instruction
                new_data = {
                    "contents": [
                        {
                            "role": "user",
                            "parts": [{"text": input_text}]
                        },
                        {
                            "role": "model",
                            "parts": [{"text": output_text}]
                        }
                    ]
                }
                
                f_out.write(json.dumps(new_data) + "\n")
                converted_count += 1
                
            except Exception as e:
                print(f"Error processing line {line_num} in {input_file}: {e}")
    
    print(f"Successfully converted {converted_count} examples to {output_file} (basic format)")
    return True

if __name__ == "__main__":
    # Convert training file with system instructions
    convert_to_vertex_ai_format(INPUT_TRAINING, OUTPUT_TRAINING)
    
    # Also create a version without system instructions for compatibility
    basic_output = OUTPUT_TRAINING.replace('.jsonl', '_basic.jsonl')
    convert_to_vertex_ai_format_basic(INPUT_TRAINING, basic_output)
    
    # Convert validation file if it exists
    if os.path.exists(INPUT_VALIDATION):
        convert_to_vertex_ai_format(INPUT_VALIDATION, OUTPUT_VALIDATION)
        
        # Also create a validation version without system instructions
        basic_validation = OUTPUT_VALIDATION.replace('.jsonl', '_basic.jsonl')
        convert_to_vertex_ai_format_basic(INPUT_VALIDATION, basic_validation)
        
    print("\nConversion complete!")
    print("The converted files are now ready for Vertex AI Gemini supervised fine-tuning.")
