import os
import subprocess
import argparse

def process_videos(input_dir, output_dir, start_time, end_time):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            duration = end_time - start_time
            
            # Construct the ffmpeg command
            command = [
                'ffmpeg',
                '-ss', f'{start_time:.2f}',
                '-i', input_path,
                '-t', f'{duration:.2f}',
                '-c:v', 'libx264',
                '-crf', '18',  # 18 is generally considered visually lossless
                '-preset', 'slow',
                output_path
            ]
            
            print(f"Processing {filename}")
            subprocess.run(command, check=True)

def parse_time_range(time_range):
    start, end = time_range.split('-')
    return float(start), float(end)

def main():
    parser = argparse.ArgumentParser(description="Crop and compress videos.")
    parser.add_argument('y', type=str, help="Directory containing the input videos.")
    parser.add_argument('z', type=str, help="Directory to save the processed videos.")
    parser.add_argument('time_range', type=str, help="Time range to crop from the video, formatted as 'start-end' (e.g., '1-11' or '1.5-11.5').")
    
    args = parser.parse_args()
    
    input_dir = args.y
    output_dir = args.z
    start_time, end_time = parse_time_range(args.time_range)
    
    process_videos(input_dir, output_dir, start_time, end_time)

if __name__ == "__main__":
    main()