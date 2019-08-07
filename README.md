# ShowOutput
This app is used to display an Image loaded by TCP socket using a specific protocol. Is was made using PyQT5.

## Configuring Environment   
To start, open a Terminal and change to an empty directory. We will use a Python virtual environment to hold your project's dependencies. Create it via the following command:   
   
```python3 -m venv venv```   
   
Then, activate the virtual environment:   
   
```source venv/bin/activate```   
   
You can verify this was successful by the (venv) prefix in your shell:   
   
 ![](https://build-system.fman.io/static/public/img/venv-active-linux.png)   
    
 With the virtual environment still active, install the following Python dependencies:   
    
```pip install fbs PyQt5==5.9.2```   
   
Execute ```fbs startproject```. This asks you a few questions. Pick any values you like:   
   
![](https://build-system.fman.io/static/public/img/fbs-startproject.png)   
   
When you follow the suggestion and enter ```fbs run```, a little window should appear:   
   
![](https://build-system.fman.io/static/public/img/fbs-initial-app.png)   
   
Replace ```src/main/python/main.py```  with your own code   
   
   
## TCP Protocol
