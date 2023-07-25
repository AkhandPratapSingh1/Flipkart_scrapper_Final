// UrlForm.js
import React, { useState } from 'react';
import axios from 'axios';
import './UrlForm.css'; // Import the CSS file

function UrlForm() {
  const [url, setUrl] = useState('');
  const [scrapedData, setScrapedData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchUrlData = async () => {
    try {
      setLoading(true);
      const response = await axios.post('http://1012.pythonanywhere.com/scrape', { url });
      setScrapedData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  return (
    <div className="url-form">
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter URL"
        className="input-field"
      />
      <button
        onClick={fetchUrlData}
        disabled={loading}
        className={loading ? 'fetch-btn disabled' : 'fetch-btn'}
      >
        {loading ? 'Fetching...' : 'Fetch Data'}
      </button>

      {loading && <div className="loading-text">Loading...</div>}

      {scrapedData && (
        <div className="fetched-data">
          <h2>Fetched Data:</h2>
          <p><strong>Title:</strong> {scrapedData.title}</p>
          <p><strong>Description:</strong> {scrapedData.description}</p>
          <p><strong>Price:</strong> {scrapedData.price}</p>
          <p><strong>Rating:</strong> {scrapedData.mobile_number}</p>
          {scrapedData.size && <p><strong>Size:</strong> {scrapedData.size}</p>}
          {scrapedData.category && <p><strong>Category:</strong> {scrapedData.category}</p>}
          {scrapedData.product_image && (
            <img
              src={scrapedData.product_image}
              alt="Product"
              className="product-image"
            />
          )}
        </div>
      )}
    </div>
  );
}

export default UrlForm;
