# Machine Learning Lab: Detecting and Mapping City Elements (Trashbins) using Machine Learning 
This repository contains our code for the ML Lab project WS 24/25. In the following, we give brief explanation of how our application works (More detailed in the report), an explanation of the folder structure, and the necessary steps to run the application. 
## How it works 
We trained a YOLOv11 model on Google Street View images, where the labels are the bounding boxes of trashbins. This model is integrated into a pipeline, where we first fetch images in a radius from google streetview, detect trashbins using the model, and then extract coordinates of the image metadata in order to plot a pin for the trashbin at that location. Using streamlit, we built a frontend where the user can choose to start the pipeline at a specific location and dynamically see the results of our detection pipeline displayed on a map. 

A sample output of our final model:
<img width="812" alt="image" src="https://github.com/user-attachments/assets/24368398-5856-4190-b710-fa527965176f" />


An updated map with trashbin locations mapped: 
<img width="482" alt="image" src="https://github.com/user-attachments/assets/4be135f3-29f7-42e8-b7e4-10272edb756d" />

## Data
We collected and labelled more than 7000 Google Street View screenshots with trashbins.
Due to its size, the data that we collected and labelled during our project is not included in the repository. The data is available on request. 
## Folder Structure
### ml_files folder 
This folder contains code related training the yolov7 and yolov11 models (in the folders ml_files/yolov7 and ml_files/yolov11 respectively). In ml_files/utils, there are some python scripts that were used to move files, create empty labels or plot some of the data. Note that file paths are often hardcoded.
### model_testing 
This folder contains scripts for doing inference with our trained models and evaluating it on a test set. Again, note that file paths are hardcoded
### street_view_approach
This folder contains our streamlit application and backend code. 
### video_approach 
This folder contains code for an approach that was not finished due to time reasons. Here, we wanted to use video data that was collected by our group and map trashbins on frames of the video.
### old_files 
This folder contains some early attempts and explorations of our project. It is not relevant for the final application, but we included it for the sake of documenting our project. 
## How to run the application 
First, clone the repository:
```
git clone https://github.com/yourusername/city-elements-trashbin-mapping.git
```
Create a conda environment 
```
conda create -n city-mapping
```
Install the dependencies
```
pip install -r 'requirements.txt'
```
Then, navigate to the app folder 
```
cd street_view_approach 
```
#### Line 20 in app.py requires an email-address. 
#### Line 5 in fetch_street_view.py requires a Google Street View API Key. 
Run the app and start the detection pipeline
```
streamlit run app.py 
```
