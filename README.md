
# Cloud Computing Scaler
This is the project for Cloud Computing 2022, University of Leiden
## Instructions
1. Run the create_images.sh script to create the necessary images. This will create
the images and 2 containers. One wait container and one haproxy container.
``` 
chmod +x create_images.sh
./create_images
```

2. To run the scaler, run the run.py file. This will start the scaler and will output 
the current amount of containers. Please run this when you do have 0 webapp containers
and only have one wait container and one haproxy container to avoid any errors.

```
python3 run.py

```

3. If you want to run any experiments, please check first check the experiment files.
You might have to edit them in order to enter the correct IP address of the haproxy
load balancer. These files are: calibration.py, calibration_multiple.py,
calibration_noerr.py, experiment_static.py, experiment_static_noerrors.py
```
python3 experiment_static.py
```