import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# One Piece Review Analysis with Sentiment Analysis\n",
                "\n",
                "This notebook combines:\n",
                "1. Scraping One Piece reviews from MyAnimeList\n",
                "2. Sentiment analysis using TextBlob\n",
                "3. Visualization of both ratings and sentiments"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Import required libraries\n",
                "import requests\n",
                "from bs4 import BeautifulSoup\n",
                "import pandas as pd\n",
                "import matplotlib.pyplot as plt\n",
                "import re\n",
                "from textblob import TextBlob\n",
                "import seaborn as sns"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Scrape Reviews from MyAnimeList"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "def scrape_reviews():\n",
                "    url = 'https://myanimelist.net/anime/21/One_piece/reviews'\n",
                "    response = requests.get(url)\n",
                "    soup = BeautifulSoup(response.text, 'lxml')\n",
                "    \n",
                "    reviews = []\n",
                "    \n",
                "    for review in soup.find_all('div', class_='review-element'):\n",
                "        rating_tag = review.find('div', class_='rating')\n",
                "        if rating_tag:\n",
                "            # Extract rating using regex to handle different formats\n",
                "            match = re.search(r'(\\d+(\\.\\d+)?)', rating_tag.text)  \n",
                "            if match:\n",
                "                rating = match.group(1)\n",
                "            else:\n",
                "                rating = \"N/A\"\n",
                "        else:\n",
                "            rating = \"N/A\"\n",
                "\n",
                "        text_tag = review.find('div', class_='text')   \n",
                "        review_text = text_tag.get_text(separator=' ', strip=True) if text_tag else 'N/A'\n",
                "\n",
                "        reviews.append({\n",
                "            'rating': rating,\n",
                "            'text': review_text\n",
                "        })\n",
                "\n",
                "    return pd.DataFrame(reviews)\n",
                "\n",
                "# Scrape reviews\n",
                "df = scrape_reviews()\n",
                "print(\"First few reviews:\")\n",
                "print(df.head())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Perform Sentiment Analysis"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "def sentiment_analysis(df):\n",
                "    sentiments = []\n",
                "    polarity_scores = []\n",
                "\n",
                "    for text in df['text']:\n",
                "        blob = TextBlob(text)\n",
                "        polarity = blob.sentiment.polarity\n",
                "\n",
                "        polarity_scores.append(polarity)\n",
                "\n",
                "        if polarity > 0.1:\n",
                "            sentiment = \"Positive\"\n",
                "        elif polarity < -0.1:\n",
                "            sentiment = \"Negative\"\n",
                "        else:\n",
                "            sentiment = \"Neutral\"\n",
                "\n",
                "        sentiments.append(sentiment)\n",
                "\n",
                "    df['polarity'] = polarity_scores\n",
                "    df['sentiment'] = sentiments\n",
                "    return df\n",
                "\n",
                "# Perform sentiment analysis\n",
                "df = sentiment_analysis(df)\n",
                "print(\"\\nReviews with sentiment analysis:\")\n",
                "print(df.head())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Filter and Analyze High-Rated Reviews"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "def filter_reviews(df, min_rating):\n",
                "    # Convert 'rating' column to numeric, replacing invalid values with NaN\n",
                "    df['rating'] = pd.to_numeric(df['rating'], errors='coerce') \n",
                "    # Filter out rows with ratings less than 'min_rating' and drop rows with NaN ratings\n",
                "    filtered_df = df[df['rating'] >= min_rating].dropna()  \n",
                "    return filtered_df\n",
                "\n",
                "# Filter high-rated reviews\n",
                "high_rated_reviews = filter_reviews(df, 8)\n",
                "print(\"\\nHigh-rated reviews (rating >= 8):\")\n",
                "print(high_rated_reviews.head())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Visualizations"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "def plot_ratings_and_sentiment(df):\n",
                "    # Create a figure with two subplots\n",
                "    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))\n",
                "    \n",
                "    # Plot 1: Rating Distribution\n",
                "    ratings = pd.to_numeric(df['rating'], errors='coerce').dropna()\n",
                "    if not ratings.empty:\n",
                "        ratings.value_counts().sort_index().plot(kind='bar', color='skyblue', ax=ax1)\n",
                "        ax1.set_title('Distribution of One Piece Review Ratings')\n",
                "        ax1.set_xlabel('Rating (/10)')\n",
                "        ax1.set_ylabel('Number of Reviews')\n",
                "    \n",
                "    # Plot 2: Sentiment Distribution\n",
                "    sentiment_counts = df['sentiment'].value_counts()\n",
                "    sentiment_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax2)\n",
                "    ax2.set_title('Distribution of Review Sentiments')\n",
                "    \n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "\n",
                "# Create visualizations\n",
                "plot_ratings_and_sentiment(df)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Additional Analysis: Correlation between Ratings and Sentiment"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "def analyze_rating_sentiment_correlation(df):\n",
                "    # Convert ratings to numeric\n",
                "    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')\n",
                "    \n",
                "    # Create a cross-tabulation of ratings and sentiments\n",
                "    rating_sentiment = pd.crosstab(df['rating'], df['sentiment'])\n",
                "    \n",
                "    # Plot heatmap\n",
                "    plt.figure(figsize=(12, 6))\n",
                "    sns.heatmap(rating_sentiment, annot=True, fmt='d', cmap='YlOrRd')\n",
                "    plt.title('Correlation between Ratings and Sentiments')\n",
                "    plt.xlabel('Sentiment')\n",
                "    plt.ylabel('Rating')\n",
                "    plt.show()\n",
                "    \n",
                "    # Print summary statistics\n",
                "    print(\"\\nSummary Statistics:\")\n",
                "    print(f\"Average polarity score: {df['polarity'].mean():.3f}\")\n",
                "    print(f\"Average rating: {df['rating'].mean():.2f}\")\n",
                "    print(\"\\nSentiment distribution:\")\n",
                "    print(df['sentiment'].value_counts(normalize=True).round(3) * 100)\n",
                "\n",
                "# Analyze correlation\n",
                "analyze_rating_sentiment_correlation(df)"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Write the notebook to a file
with open('one_piece_sentiment_analysis.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1) 