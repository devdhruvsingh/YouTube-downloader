import React, { useState, useEffect } from 'react';
import { analyzeVideo, startDownload, getDownloadStatus, getFileDownloadUrl } from '../services/api';
import VideoCard from '../components/VideoCard';

export default function Home() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [videoInfo, setVideoInfo] = useState(null);
  const [selectedFormat, setSelectedFormat] = useState('best');
  const [taskId, setTaskId] = useState(null);
  const [taskStatus, setTaskStatus] = useState(null);
  const [error, setError] = useState(null);

  // Handle Video Analysis
  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!url.trim()) return;

    setLoading(true);
    setError(null);
    setVideoInfo(null);
    setTaskId(null);
    setTaskStatus(null);

    try {
      const res = await analyzeVideo(url);
      const actualData = res?.data || res;
      setVideoInfo(actualData);

      if (actualData?.formats && actualData.formats.length > 0) {
        setSelectedFormat(actualData.formats[0].format_id);
      }
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to analyze video. Please check the URL.');
    } finally {
      setLoading(false);
    }
  };

  // Handle Download Trigger
  const handleDownload = async () => {
    if (!videoInfo) return;

    try {
      setError(null);
      const res = await startDownload(url, selectedFormat);
      const newTaskId = res?.task_id || res?.data?.task_id;
      
      if (newTaskId) {
        setTaskId(newTaskId);
        setTaskStatus({ status: 'processing', progress_percentage: 0 });
      } else {
        setError('Failed to start download task.');
      }
    } catch (err) {
      setError(err?.response?.data?.detail || 'Download initiation failed.');
    }
  };

  // Poll Task Status & Trigger Browser Download on Completion
  useEffect(() => {
    if (!taskId) return;

    const interval = setInterval(async () => {
      try {
        const res = await getDownloadStatus(taskId);
        const statusData = res?.data || res;
        setTaskStatus(statusData);

        if (statusData.status === 'completed' || statusData.status === 'failed') {
          clearInterval(interval);
          
          if (statusData.status === 'completed') {
            // Automatically trigger download into system's Downloads folder
            const downloadUrl = getFileDownloadUrl(taskId);
            const link = document.createElement('a');
            link.href = downloadUrl;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          }
        }
      } catch (err) {
        console.error('Error fetching task status:', err);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [taskId]);

  return (
    <div style={{ minHeight: '100vh', padding: '0 16px 48px', background: '#f8fafc', fontFamily: 'Inter, sans-serif' }}>
      {/* Header */}
      <header style={{ textAlign: 'center', paddingTop: '48px', paddingBottom: '20px' }}>
        <h1 style={{ fontSize: '32px', fontWeight: '800', color: '#7c3aed', margin: 0 }}>
          MediaMorph
        </h1>
        <p style={{ color: '#64748b', fontSize: '14px', marginTop: '6px' }}>
          Download YouTube Videos in Any Resolution & Format
        </p>
      </header>

      {/* URL Input Form */}
      <form 
        onSubmit={handleAnalyze}
        style={{
          maxWidth: '650px',
          margin: '0 auto 24px auto',
          display: 'flex',
          background: '#ffffff',
          borderRadius: '24px',
          padding: '8px',
          boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.05)',
          border: '1px solid #e2e8f0'
        }}
      >
        <input 
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Paste YouTube video link here..." 
          required
          style={{
            flex: 1,
            border: 'none',
            background: 'transparent',
            padding: '12px 16px',
            fontSize: '15px',
            outline: 'none',
            color: '#0f172a'
          }}
        />
        <button 
          type="submit"
          disabled={loading}
          style={{
            background: '#8b5cf6',
            color: '#ffffff',
            border: 'none',
            padding: '12px 24px',
            borderRadius: '16px',
            fontWeight: '700',
            cursor: loading ? 'not-allowed' : 'pointer',
            transition: 'background 0.2s'
          }}
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>

      {/* Error Message */}
      {error && (
        <div style={{ maxWidth: '650px', margin: '0 auto 16px auto', padding: '14px', background: '#fee2e2', color: '#dc2626', borderRadius: '12px', textAlign: 'center', fontWeight: '600', fontSize: '13px' }}>
          {error}
        </div>
      )}

      {/* Video Card Component */}
      {videoInfo && (
        <VideoCard 
          videoInfo={videoInfo}
          selectedFormat={selectedFormat}
          setSelectedFormat={setSelectedFormat}
          onDownload={handleDownload}
          taskStatus={taskStatus}
        />
      )}
    </div>
  );
}