# One Piece Review Analysis

This project analyzes reviews of the popular anime series "One Piece" from MyAnimeList, performing sentiment analysis and creating visualizations to understand viewer opinions and ratings.

## Features

- Web scraping of One Piece reviews from MyAnimeList
- Sentiment analysis using TextBlob
- Rating distribution analysis
- Sentiment distribution visualization
- Correlation analysis between ratings and sentiments
- High-rated review filtering and analysis

## Project Structure

```
one_piece_review/
├── one_piece_sentiment_analysis.ipynb  # Main analysis notebook
├── requirements.txt                    # Project dependencies
└── README.md                          # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/one_piece_review.git
cd one_piece_review
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Open the Jupyter notebook:
```bash
jupyter notebook one_piece_sentiment_analysis.ipynb
```

2. Run the cells in sequence to:
   - Scrape reviews from MyAnimeList
   - Perform sentiment analysis
   - Generate visualizations
   - Analyze correlations between ratings and sentiments

## Dependencies

- requests: For web scraping
- beautifulsoup4: For HTML parsing
- pandas: For data manipulation
- matplotlib: For basic plotting
- seaborn: For advanced visualizations
- textblob: For sentiment analysis
- jupyter: For running the notebook
- notebook: For notebook interface

## Future Improvements

- Add more advanced sentiment analysis techniques
- Implement machine learning models for review classification
- Add support for analyzing reviews in different languages
- Create a web interface for interactive analysis
- Add support for analyzing other anime series
- Implement review summarization
- Add time-series analysis of reviews
- Create an API for accessing the analysis results

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MyAnimeList for providing the review data
- TextBlob for sentiment analysis capabilities
- The Python community for the amazing libraries used in this project 