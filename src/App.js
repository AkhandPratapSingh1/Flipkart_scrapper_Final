// App.js

import React from 'react';
import './App.css';
import UrlForm from './UrlForm';
import ScrapedUrlsByCategory from './ScrapedUrlsByCategory';

function App() {
  return (
    <div className="app-container">
      <div className="url-form-container">
       
        <UrlForm />
      </div>
      <div className="scraped-urls-container">
      
        <ScrapedUrlsByCategory />
      </div>
    </div>
  );
}

export default App;
