# Minimal_Website_Stalker

- Minimal implementation of a script to track parts of pages from multiple websites to see if they changed. Useful to stalk job boards and many others
- So far this is only tested with Safari on MacOS, to use it with other browsers you need to change the driver in the code

## How to use

- Clone the repo
- Install the requirements
- Create a file called 'websites.csv' in the data folder
- Add the websites you want to track in the following format:

```
website url,xpath to the element you want to track
website url,xpath to the element you want to track
website url,xpath to the element you want to track
```

- Run the script with `python3 main.py`
- To choose how often the script checks the websites use the `--t` argument. Enter value in _minutes_
- Control/Command + C to stop the script
  `python main.py --t 15`

## How to find the xpath

- Open the website in your browser
- Right click on the element you want to track
- Click on inspect
- Right click on the highlighted line in the inspector
- Click on copy -> copy xpath
