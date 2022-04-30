from bs4 import BeautifulSoup
import sys
from os import listdir
from os.path import isfile, join
import re


def download_image(image_urls):
    reg = "(https:\/\/yt3.ggpht.com\/)(.*)(=s.*)"
    for url in image_urls:
        reg_match = re.search(reg, url)
        filename = reg_match[1] + ".jpg"
        new_url = reg_match[0] + reg_match[1] + "=s0"
        with open(filename, 'wb') as handler:
            img_data = requests.get(new_url).content
            handler.write(img_data)


def find_images(soup):
    image_urls = soup.find_all('img', attrs={'class': 'style-scope yt-img-shadow', 'id': 'img'})

# TODO: Download images by getting the singlefile of community page without replacing crawled url
# Then fix image gallery scrolling
def main():
    # Get directory path
    try:
        if sys.argv[1] is not None:
            path = sys.argv[1]
    except:
        path = input("Path: ")

    # Get the list of files in the directory if directory path is provided and not filename
    if ".html" not in path:
        files = [f for f in listdir(path) if isfile(join(path, f))]
        print(f"Total Files: {len(files)}")
    else:
        files = []
        files.append(path)

    for file in files:
        # Add .html extension if not provided
        # if ".html" not in file:
        #     file = file + ".html"

        # Get file path
        if path not in file:
            file = path+"\\"+file
        print("\n" + file)
        # Open test.html for reading
        with open(file, 'r') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')
            # print(soup)
            # Remove the blue sticky popup
            try:
                popup = soup.find('div', id='contentWrapper')
                popup.decompose()
            except Exception as e:
                print(e, "\nError removing blue popup\n")

            # Make the header static so it doesn't cover half the screen
            try:
                header = soup.find('tp-yt-app-header', attrs={'id': 'header', 'class': "style-scope ytd-c4-tabbed-header-renderer"})
                script_attribute = header['style']
                if ";position:static" not in script_attribute:
                    header['style'] = script_attribute + ";position:static"
                    print(header['style'], "\n")
                else:
                    print("Static Position Appended: True\n")
            except Exception as e:
                print(e, "\nError appending static position to the style's attribute\n")

            # Remove the excess padding from the container
            try:
                padding = soup.find('div', attrs={'id': 'contentContainer', 'class': 'style-scope tp-yt-app-header-layout'})
                padding.decompose()
                print("Remove Container Padding: True")
            except Exception as e:
                print(e, "\nError removing excess padding from contentContainer div\n")

            # Remove collapse to show all text
            ytd_expander = soup.find_all('ytd-expander', attrs={'class': 'style-scope ytd-backstage-post-renderer', 'id': 'expander',
                                                                'collapsed': True})
            changeCounter = 0
            for element in ytd_expander:
                if 'collapsed' in element.attrs:
                    del element.attrs['collapsed']
                    changeCounter+=1
            print(f"Removed Collapsed Attributes: {changeCounter}")

            # Unhide the "Read Less" button if the "Read More" button is not hidden
            # This ensures that "Read Less" is only unhidden on posts with a lot of text
            # Does not work as expected because although hidden attribute is removed it's reintroduced later?
            changeCounter = 0
            read_less_buttons = soup.find_all('tp-yt-paper-button', attrs={'class': 'style-scope', 'id': 'less'})
            try:
                for button in read_less_buttons:
                    # Checks if it's sibling("Read More") has a hidden attribute
                    # So basically the "Read More" tag is visible then unhide "Show Less" button
                    if 'hidden' not in button.parent.contents[7].attrs:
                        del button.attrs['hidden']
                        changeCounter+=1
            except Exception as e:
                print(e, "\nError while handling the read less buttons")
            print(f"Read Less Button Changes: {changeCounter}")

            # Hide the "Read More" button
            changeCounter = 0
            read_more_buttons = soup.find_all('tp-yt-paper-button', attrs={'class': 'style-scope ytd-expander', 'id': 'more'})
            # Create/add the hidden attribute
            try:
                for button in read_more_buttons:
                    button['hidden'] = ''
                    changeCounter += 1
            except Exception as e:
                print(e, "\nError handling the read more buttons")
            print(f"Read More Button Changes: {changeCounter}")

            # # Show membership perks
            # try:
            #     perk_dropdown = soup.find('ytd-sponsorships-expandable-perks-renderer', attrs={'class': 'style-scope ytd-section-list-renderer'})
            #     del perk_dropdown.attrs['is-collapsed']
            # except Exception as e:
            #     print(e, "\nError trying to uncollapse membership perk dropdown")

            # Get the string of soup rather than prettifying it
            edited_html = str(soup)

        # Write changes back to the original file
        with open(file, mode='w') as edited_html_file:
            edited_html_file.write(edited_html)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e, "\nAn unexpected Error has Occurred")