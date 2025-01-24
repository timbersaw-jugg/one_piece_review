import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import re

def scrape_reviews():
    url='https://myanimelist.net/anime/21/One_piece/reviews'
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'lxml')
    
    
    
    reviews=[ ]
    

    for review in soup.find_all('div',class_='review-element'):
        
        rating_tag=review.find('div', class_='rating')
        if rating_tag:
            # Extract rating using regex to handle different formats
            match = re.search(r'(\d+(\.\d+)?)', rating_tag.text)  
            if match:
                rating = match.group(1)
            else:
                rating = "N/A"
        else:
            rating="N/A"

        text_tag=review.find('div',class_='text')   
        review_text=text_tag.get_text(separator=' ',strip=True) if text_tag else 'N/A'

        reviews.append({
            'rating':rating,
            'text':review_text
        })

    return pd.DataFrame(reviews)
df=scrape_reviews()
print(df.head())       

def filter_reviews(df,min):
    # Convert 'rating' column to numeric, replacing invalid values with NaN
    df['rating']=pd.to_numeric(df['rating'],errors='coerce') 
    # Filter out rows with ratings less than 'min' and drop rows with NaN ratings
    filtered_df=df[df['rating']>=min].dropna()  
    return filtered_df

high_rated_reviews=filter_reviews(df,8)
print(high_rated_reviews)

def plot_ratings(df):
    # Convert 'rating' column to numeric and remove non-numeric values before plotting
    ratings = pd.to_numeric(df['rating'], errors='coerce').dropna()
    
    # Check if ratings data is empty after cleaning
    if ratings.empty:
        print("No valid ratings to plot.")
        return
    
    plt.figure(figsize=(10,6))
    ratings.value_counts().sort_index().plot(kind='bar',color='skyblue')
    plt.title('Distribution of one piece review ratings')
    plt.xlabel('rating(/10)')
    plt.ylabel('Number of reviews')
    plt.show()

plot_ratings(df)