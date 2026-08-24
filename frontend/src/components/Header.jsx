import React from 'react';
import { Video } from 'lucide-react';

export default function Header() {
  return (
    <header style={{ textAlign: 'center', paddingTop: '40px', paddingBottom: '20px' }}>
      <div style={{ display: 'inline-flex', alignItems: 'center', gap: '12px' }}>
        <div 
          className="clay-card" 
          style={{ 
            padding: '12px', 
            background: 'var(--primary)', 
            color: 'white', 
            borderRadius: '18px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <Video size={32} />
        </div>
        <h1 style={{ fontSize: '2rem', fontWeight: '800', margin: 0 }}>
          Media<span style={{ color: 'var(--primary)' }}>Morph</span>
        </h1>
      </div>
    </header>
  );
}