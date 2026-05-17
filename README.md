# SafeDrive - License Plate Detection and Traffic Violation Detection System

An AI-powered automated traffic violation detection backend system using Computer Vision. SafeDrive processes traffic footage to detect traffic light violations, extract license plate information, and log infractions automatically.

## Features

- **Traffic Light State Detection**: Monitors the current state of traffic lights (Red, Green, Yellow) to determine valid vehicle movement.
- **Vehicle & Helmet Detection**: Uses YOLOv8 object detection (`yolov8s.pt`, `helmet.pt`) to detect vehicles and whether two-wheeler riders are wearing helmets.
- **License Plate Recognition (ANPR)**: Employs custom YOLO models (`plate.pt`) to detect license plates, and **EasyOCR** to extract text from the license plates of violating vehicles.
- **Violation Logging**: Automatically generates CSV records (`violations.csv`) containing details of the infraction, including the vehicle plate number and timestamp.
- **Cropped Evidence**: Automatically crops and saves images of the detected violation (`violation_crops`) and the vehicle's license plate (`plate_crops`) as evidence.
- **Cloud Integration**: Uses a backend script (`process_violations.py`) to process violations, potentially integrating with Firebase or other cloud services for database storage (via `serviceAccountKey.json`).

## Project Structure

- `red_light_project/`: Contains the core computer vision pipeline.
  - `red_light_pipeline.py`: The main script that runs the traffic light and vehicle detection logic.
  - `*.pt`: PyTorch YOLO model weights for general objects, plates, and helmets.
- `backend/`: Handles data processing and syncing.
  - `process_violations.py`: Backend script for handling logged violations.
- `input videos/`: Directory for placing raw video footage for processing.
- `traffic_light.html`: A frontend interface for visualizing data or status.

## Technologies Used

- **Python**
- **OpenCV**: For video processing and frame manipulation.
- **Ultralytics YOLOv8**: For real-time object detection (vehicles, plates, helmets).
- **EasyOCR**: For Optical Character Recognition to extract license plate text.
- **Pandas**: For managing and exporting violation data.
- **Firebase (Optional)**: For cloud syncing and storage.

## Setup and Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/SidharthMN/LICENSEPLATEDETECTION
   cd safedrive_backend/corepart
   ```

2. **Set up the Conda Environment:**

   ```bash
   conda create --name rl_env python=3.12
   conda activate rl_env
   ```

3. **Install Dependencies:**
   Navigate to the respective directories and install requirements:

   ```bash
   cd red_light_project
   pip install -r requirements.txt

   cd ../backend
   pip install -r requirements.txt
   ```

4. **Add Model Weights:**
   Ensure the `.pt` files (`yolov8s.pt`, `plate.pt`, `helmet.pt`) are present in the `red_light_project/` directory.

5. **Run Code:**
   For red_light_project : python red_light_pipeline.py --source "input video source location" --out output_video.mp4 --show

   For backend to integrate data from red_light_project :
   python process_violations.py

## Usage

To run the main detection pipeline, navigate to the `red_light_project` directory and execute the pipeline script on your input video.

Also apply in case of Backend

## License

[MIT License](LICENSE) (Update as appropriate)
