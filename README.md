# <p ><img src="Ppda\static\assets\img\lungs.ico" alt="Icon" width="30" height="30"> Pediatric Pnuemonia Diagnostic Aid : Automatic Covid & Pneumonia Detection </p>

**Pediatric Pnuemonia Diagnostic Aid**: Step into the world of cutting-edge technology with our web application. Built upon groundbreaking machine learning research, we've harnessed the power of diverse deep learning classification models. Our application is designed to accurately identify Pneumonia cases from X-ray bringing crucial medical insights to your fingertips.

## Features

- Multiple AI modalities
- Firendly User Interface - Web Application
- Database integration
- Fast prediction time [Strong GPU required]
  - with a stronger GPU the prediction time will be significantly reduced, as all models will be loaded only once.

## installation - Conda

> warning: AI models are not uploaded yet

- clone the repo

- Create a Conda Environment - this will take a while
  ```bash
  conda env create -f environment.yml
  ```
- Activate the environment - name : ppda
  ```bash
  conda activate ppda
  ```
- Follow the Firebase Authentication Guide here
  - [Firebase connection authentication](ppda/readme.md)
- Navigate to the Pulmo-AI directory
  ```bash
  python app.py
  ```

## Main Tools

- `Python` - The primary programming language employed throughout our research endeavors. Python was instrumental in managing backend connections and facilitating database integration.

- `TensorFlow` - Utilized for both research and deployment purposes, TensorFlow played a pivotal role in our projects.

- `Flask` - Our application was constructed using the Flask framework, offering a easy and solid foundation for its development.

- `Firebase` - We established a linkage to Firebase cloud storage, effectively storing our images in a remote environment.

- `PIL` (Python Imaging Library) - PIL was employed to fine-tune images for compatibility with AI models, ensuring seamless integration.

- `Plotly` and `Matplotlib` - These visualization libraries were harnessed to present our research findings, offering clear and visually engaging insights. Moreover, they facilitated model predictions within our application.

- `JavaScript` - This scripting language was strategically employed to manage some backend events, oversee user interface interactions, and provide dynamic animations within the application framework.

- `HTML` , `CSS` and `jinja2` - were utilized to construct the user interface, offering a visually appealing and intuitive experience for users.

## Examples
![Alt text](https://github.com/Praveen10008/Pediatric-Pneumonia-Diagnostic-Aid/blob/master/Examples/Picture6.png)
![Alt text](https://github.com/Praveen10008/Pediatric-Pneumonia-Diagnostic-Aid/blob/master/Examples/Picture7.png)
![Alt text](https://github.com/Praveen10008/Pediatric-Pneumonia-Diagnostic-Aid/blob/master/Examples/Picture8.png)
![Alt text](https://github.com/Praveen10008/Pediatric-Pneumonia-Diagnostic-Aid/blob/master/Examples/Picture9.png)

