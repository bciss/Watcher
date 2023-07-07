import requests
import hashlib
import datetime
from bs4 import BeautifulSoup

# Define the list of URLs to monitor
urls = [
    {"name": "Angular", "url": "https://github.com/angular/angular/blob/main/CHANGELOG.md"},
    {"name": "Rust", "url": "https://github.com/rust-lang/rust/blob/master/RELEASES.md"},
    {"name": "Docker", "url": "https://docs.docker.com/compose/release-notes/"},
    {"name": "Ansible", "url": "https://github.com/ansible/ansible/releases"},
    {"name": "Kubernetes", "url": "https://kubernetes.io/releases/"},
    {"name": "Jenkins", "url": "https://www.jenkins.io/changelog/"},
    {"name": "Terraform", "url": "https://github.com/hashicorp/terraform/releases"},
    ]
# Function to get the current date and time
def get_current_datetime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# Function to calculate the hash of a given content
def calculate_hash(content):
    hash_object = hashlib.md5(content.encode())
    return hash_object.hexdigest()

# Function to load the stored data from a file
def load_data():
    try:
        with open("data.txt", "r") as file:
            return eval(file.read())
    except FileNotFoundError:
        return {}

# Function to store the updated data to a file
def store_data(data):
    with open("data.txt", "w") as file:
        file.write(str(data))
      
# Main script logic
def main():
    data = load_data()

    for url_info in urls:
        name = url_info["name"]
        url = url_info["url"]

        # Make a request to the URL
        response = requests.get(url)
        html_content = response.text

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        headings = soup.find_all(["h1", "h2", "h3"])
        extracted_content = " ".join([heading.get_text().strip() for heading in headings])

        # Calculate the hash of the extracted content
        current_hash = calculate_hash(extracted_content)

        # Compare the current hash with the stored hash
        if url in data:
            if data[url]["hash"] == current_hash:
                status = "\033[92mNo Change\033[0m"  # Green color
                time_since_last_change = (datetime.datetime.now() - data[url]["last_changed"]).total_seconds()
            else:
                status = "\033[93mChanged\033[0m"  # Orange color
                time_since_last_change = 0
        else:
            status = "\033[93mChanged\033[0m"  # Orange color
            time_since_last_change = 0

        # Update the stored data
        data[url] = {"hash": current_hash, "last_changed": datetime.datetime.now()}

        # Print the result
        print(f"{name}: {url} [{status}] - Time Since Last Change: {time_since_last_change} seconds")

    # Store the updated data
    store_data(data)

if __name__ == "__main__":
    main()
