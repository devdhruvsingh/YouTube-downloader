import React from 'react';
import { Search } from 'lucide-react';

export default function UrlInput({ url, setUrl, onAnalyze, loading }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim()) onAnalyze(url);
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '650px', margin: '20px auto' }}>
      <div className="clay-input-box">
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Paste YouTube video link here..."
          className="clay-input"
          required
        />
        <button type="submit" disabled={loading} className="clay-btn-primary">
          <Search size={18} />
          <span>{loading ? 'Analyzing...' : 'Analyze'}</span>
        </button>
      </div>
    </form>
  );
}