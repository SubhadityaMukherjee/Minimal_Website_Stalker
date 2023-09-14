import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
from joblib import Parallel, delayed
import pickle
from desktop_notifier import DesktopNotifier

def get_element_text(driver, website_url, element_xpath):
    try:
        driver.get(website_url)
        # Find the element using its XPath
        element = driver.find_element(By.XPATH, element_xpath)

        # Get the text value of the element
        element_text = element.text

        # Print the text value
        # print('Element Text:', element_text)
        return element_text

    except Exception as e:
        print("An error occurred:", str(e))
        return None


def create_list_to_scrape():
    dict_sites = {}
    # Check if data/websites.csv exists or return error
    if not os.path.exists("data/websites.csv"):
        print("Error: data/websites.csv not found")
        return None

    # Load csv file with sites,xpath from data/websites.csv
    with open("data/websites.csv", "r") as f:
        for line in f.readlines():
            try:
                line = line.strip().split(",")
                if len(line) == 2:
                    site, xpath = line
                    dict_sites[site] = [xpath, None, None]  # [xpath,new_text,old_text]
                elif len(line) == 3:
                    site, xpath, xpath2 = line
                    dict_sites[site] = [
                        (xpath, xpath2),
                        None,
                        None,
                    ]  # [xpath,new_text,old_text]
            except ValueError:
                pass
    return dict_sites


def pickle_current_text(dict_sites):
    # Save the text value to a pickle file
    with open("data/websites.pkl", "wb") as f:
        pickle.dump(dict_sites, f)


def load_pickle_text_or_create():
    # Load the text value from the pickle file if it exists
    try:
        if os.path.exists("data/websites.pkl"):
            load_file = input("Load pickle file? (y/n): ")
            if load_file in ["y", "Y", None]:
                with open("data/websites.pkl", "rb") as f:
                    dict_sites = pickle.load(f)
            else:
                dict_sites = create_list_to_scrape()
    except:
        dict_sites = create_list_to_scrape()
    return dict_sites


def get_current_text_and_compare(driver, dict_sites):
    # Get the current text value of the element
    for site in tqdm(dict_sites.keys()):
        old_text = dict_sites[site][2] if dict_sites[site][2] is not None else ''
        # if xpath is a tuple, then get the text value of the first xpath
        if isinstance(dict_sites[site][0], tuple):
            xpath_check = dict_sites[site][0][0]
        else:
            xpath_check = dict_sites[site][0]

        new_text = get_element_text(driver, site, xpath_check)
        # Compare the current text value to the previous value
        if new_text is not None and new_text != old_text:
            # print('Text has changed!')
            # replace save new_text as old_text and replace new_text with new_text
            dict_sites[site][1] = new_text
            dict_sites[site][2] = dict_sites[site][1]
        else:
            # print('Text has not changed')
            pass
    return dict_sites


def summarize_changes(dict_sites):
    # Print a summary of the changes as website name, old text -> new text (if changed)
    site_changed = []
    for site in dict_sites.keys():
        if dict_sites[site][1] != dict_sites[site][2]:
            site_changed.append(site)
            print(site, dict_sites[site][2], "->", dict_sites[site][1])

    # open all sites in a new tabs in Safari
    if len(site_changed) > 0:
        notifier = DesktopNotifier()
        notifier.send_sync(title="Website Stalker", message="Website changes detected!")
        # open_sites = input("Open all sites in Safari? (y/n): ")
        # if open_sites in ["y", "Y"]:
            # site_open(site_changed)
    else:
        print("No sites changed")


def site_open(sites):
    # open all sites in a new tabs in Safari
    for site in sites:
        os.system("open -a Safari " + site)


def main():
    options = webdriver.SafariOptions()
    options.add_argument("-b")

    # driver = webdriver.Safari(options=options)

    dict_sites = load_pickle_text_or_create()
    driver = webdriver.Safari(options=options)
    # Get the current text value of the elements and compare to previous value and then save
    dict_sites = get_current_text_and_compare(driver, dict_sites)
    # print(dict_sites)
    pickle_current_text(dict_sites)

    # Print a summary of the changes
    summarize_changes(dict_sites)

    driver.quit()
