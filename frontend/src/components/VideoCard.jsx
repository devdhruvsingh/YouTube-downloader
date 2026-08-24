import React, { useState, useEffect } from 'react';

export default function VideoCard({ videoInfo, selectedFormat, setSelectedFormat, onDownload, taskStatus }) {
  const [activeTab, setActiveTab] = useState('mp4');

  const formats = videoInfo?.formats || [];

  // Filter options based on selected Tab
  const filteredFormats = formats.filter(f => {
    if (activeTab === 'mp4') return f.type === 'mp4' || (!f.type && f.label?.includes('MP4'));
    if (activeTab === 'webm') return f.type === 'webm' || f.label?.includes('WebM');
    if (activeTab === 'audio') return f.type === 'audio' || f.label?.toLowerCase().includes('audio');
    return true;
  });

  // Auto select default format when tab changes or video loads
  useEffect(() => {
    if (filteredFormats.length > 0 && !filteredFormats.some(f => f.format_id === selectedFormat)) {
      setSelectedFormat(filteredFormats[0].format_id);
    }
  }, [activeTab, videoInfo]);

  if (!videoInfo) return null;

  const isProcessing = taskStatus?.status === 'processing';
  const isCompleted = taskStatus?.status === 'completed';
  const progress = taskStatus?.progress_percentage || 0;

  return (
    <div style={{
      maxWidth: '680px',
      margin: '32px auto',
      padding: '28px',
      background: '#ffffff',
      borderRadius: '28px',
      boxShadow: '0 24px 48px -12px rgba(139, 92, 246, 0.15)',
      border: '1px solid #e2e8f0',
    }}>
      {/* Video Details Header */}
      <div style={{ display: 'flex', gap: '20px', alignItems: 'center', flexWrap: 'wrap' }}>
        <img 
          src={videoInfo.thumbnail} 
          alt={videoInfo.title} 
          style={{ width: '180px', height: '102px', objectFit: 'cover', borderRadius: '16px' }} 
        />
        <div style={{ flex: 1, minWidth: '240px' }}>
          <h3 style={{ margin: '0 0 6px 0', fontSize: '17px', fontWeight: '700', color: '#0f172a' }}>
            {videoInfo.title}
          </h3>
          <p style={{ margin: 0, fontSize: '13px', color: '#64748b' }}>
            Channel: <span style={{ color: '#8b5cf6', fontWeight: '600' }}>{videoInfo.uploader || 'YouTube'}</span>
          </p>
        </div>
      </div>

      <hr style={{ border: 'none', borderTop: '1px solid #f1f5f9', margin: '24px 0' }} />

      {/* Category Selection Tabs */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '20px', borderBottom: '2px solid #f1f5f9', paddingBottom: '12px' }}>
        {[
          { id: 'mp4', label: '🎬 MP4 Video' },
          { id: 'webm', label: '🌐 WebM Video' },
          { id: 'audio', label: '🎵 Audio Only' },
        ].map(tab => (
          <button
            key={tab.id}
            type="button"
            onClick={() => setActiveTab(tab.id)}
            style={{
              padding: '10px 18px',
              borderRadius: '12px',
              border: 'none',
              background: activeTab === tab.id ? '#8b5cf6' : '#f1f5f9',
              color: activeTab === tab.id ? '#ffffff' : '#475569',
              fontWeight: '700',
              fontSize: '13px',
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Resolutions Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '10px' }}>
        {filteredFormats.map((fmt, idx) => {
          const isSelected = selectedFormat === fmt.format_id;
          return (
            <button
              key={idx}
              type="button"
              onClick={() => setSelectedFormat(fmt.format_id)}
              disabled={isProcessing}
              style={{
                padding: '12px 14px',
                borderRadius: '14px',
                border: isSelected ? '2px solid #8b5cf6' : '1px solid #cbd5e1',
                background: isSelected ? '#f3e8ff' : '#f8fafc',
                color: isSelected ? '#6b21a8' : '#0f172a',
                fontWeight: '700',
                fontSize: '13px',
                cursor: isProcessing ? 'not-allowed' : 'pointer',
                textAlign: 'left',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}
            >
              <span>{fmt.label}</span>
              {isSelected && <span style={{ color: '#6b21a8' }}>✓</span>}
            </button>
          );
        })}
      </div>

      {/* Progress Status */}
      {taskStatus && (
        <div style={{ marginTop: '24px', background: '#f8fafc', padding: '16px 20px', borderRadius: '16px', border: '1px solid #e2e8f0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
            <span style={{ fontSize: '13px', fontWeight: '700', color: taskStatus.status === 'failed' ? '#e11d48' : isCompleted ? '#059669' : '#7c3aed' }}>
              {taskStatus.status === 'processing' ? 'Downloading & Converting...' : taskStatus.status}
            </span>
            <span style={{ fontSize: '14px', fontWeight: '800', color: '#0f172a' }}>{progress}%</span>
          </div>

          <div style={{ width: '100%', height: '10px', background: '#e2e8f0', borderRadius: '20px', overflow: 'hidden' }}>
            <div style={{ width: `${progress}%`, height: '100%', background: isCompleted ? '#10b981' : '#8b5cf6', transition: 'width 0.3s ease' }} />
          </div>
        </div>
      )}

      {/* Action Button */}
      <button
        onClick={onDownload}
        disabled={isProcessing}
        style={{
          width: '100%',
          marginTop: '24px',
          padding: '16px',
          borderRadius: '16px',
          border: 'none',
          background: isProcessing ? '#cbd5e1' : '#8b5cf6',
          color: '#ffffff',
          fontWeight: '700',
          fontSize: '16px',
          cursor: isProcessing ? 'not-allowed' : 'pointer'
        }}
      >
        {isProcessing ? 'Processing Download...' : isCompleted ? 'Redownload File' : 'Start Download'}
      </button>
    </div>
  );
}