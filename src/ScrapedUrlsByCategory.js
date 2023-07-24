// ScrapedUrlsByCategory.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ScrapedUrlsByCategory.css'; // Import the CSS file

function ScrapedUrlsByCategory() {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [scrapedData, setScrapedData] = useState([]);

  useEffect(() => {
    // Fetch categories from the Flask server
    axios
      .get('http://localhost:5000/categories')
      .then((response) => {
        setCategories(response.data);
      })
      .catch((error) => {
        console.error('Error fetching categories:', error);
      });
  }, []);

  const handleCategoryChange = (e) => {
    setSelectedCategory(e.target.value);
  };

  useEffect(() => {
    // Fetch scraped data for the selected category
    if (selectedCategory) {
      axios
        .get(`http://localhost:5000/scraped-urls?category=${selectedCategory}`)
        .then((response) => {
          setScrapedData(response.data);
        })
        .catch((error) => {
          console.error('Error fetching scraped data:', error);
        });
    }
  }, [selectedCategory]);

  return (
    <div className="scraped-container">
      <h2>Scraped URLs by Category</h2>
      <div className="select-container">
        <select
          value={selectedCategory}
          onChange={handleCategoryChange}
          className="select-dropdown"
        >
          <option value="">Select a category</option>
          {categories.map((category, index) => (
            <option key={index} value={category}>
              {category}
            </option>
          ))}
        </select>
      </div>
      {selectedCategory && (
        <div>
          <h3>Category: {selectedCategory}</h3>
          <ul className="url-list">
            {scrapedData.map((data, index) => (
              <li key={index} className="url-item">
                <a
                  href={data.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="url-link"
                >
                  {truncateUrl(data.url)}
                </a>
                <p className="scraped-date">
                  Scraped Date: {new Date(data.scraped_at).toLocaleString()}
                </p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default ScrapedUrlsByCategory;

// Helper function to truncate URL
function truncateUrl(url) {
  const maxLength = 130;
  return url.length > maxLength ? url.substring(0, maxLength) + '...' : url;
}
