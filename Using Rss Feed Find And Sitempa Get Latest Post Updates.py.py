import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Function to parse the sitemap and extract the latest 20 posts
def parse_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        locs = soup.find_all('loc')
        dates = soup.find_all('lastmod')
        posts = []
        for loc, date in zip(locs, dates):
            post_url = loc.text
            post_date = datetime.strptime(date.text, '%Y-%m-%dT%H:%M:%S%z')
            posts.append((post_url, post_date))
        
        # Sort posts by date in descending order
        posts.sort(key=lambda x: x[1], reverse=True)
        
        return posts[:20]
    else:
        st.error(f"Failed to fetch sitemap for URL: {sitemap_url}")

# Function to extract the title of a post from its URL
def extract_post_title(post_url):
    response = requests.get(post_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.text
    return "Title not found"

# Streamlit app
def main():
    st.title("Latest Posts from Sitemap")

    sitemap_urls = st.text_area("Enter sitemap URLs (one URL per line)", height=200).split('\n')
    
    if sitemap_urls:
        for sitemap_url in sitemap_urls:
            # Remove leading and trailing whitespace from the URL
            sitemap_url = sitemap_url.strip()
            
            if not sitemap_url:
                continue  # Skip empty lines
            
            st.write(f"Fetching the latest 20 posts from {sitemap_url}...")
            posts = parse_sitemap(sitemap_url)
            
            if posts:
                st.write(f"Latest 20 Posts from {sitemap_url}:")
                for post_url, post_date in posts:
                    post_title = extract_post_title(post_url)
                    st.write(f"- **{post_title}** - [Link]({post_url}) - {post_date.strftime('%d %B %Y %I:%M %p')}")
            else:
                st.warning(f"No posts found in the sitemap for URL: {sitemap_url}")
    else:
        st.warning("Please enter sitemap URLs.")

if __name__ == "__main__":
    main()
