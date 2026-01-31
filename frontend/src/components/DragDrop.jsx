import { useState, useRef } from 'react';
import { UploadCloud, Image as ImageIcon, X } from 'lucide-react';

const DragDrop = ({ onFileSelect }) => {
    const [isDragOver, setIsDragOver] = useState(false);
    const fileInputRef = useRef(null);
    const [preview, setPreview] = useState(null);

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragOver(true);
    };

    const handleDragLeave = () => {
        setIsDragOver(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragOver(false);
        const file = e.dataTransfer.files[0];
        validateAndSet(file);
    };

    const handleFileClick = () => {
        fileInputRef.current.click();
    };

    const handleFileInput = (e) => {
        const file = e.target.files[0];
        validateAndSet(file);
    };

    const validateAndSet = (file) => {
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                setPreview(reader.result);
                onFileSelect(file);
            };
        }
    };

    const clearImage = (e) => {
        e.stopPropagation();
        setPreview(null);
        onFileSelect(null);
        if (fileInputRef.current) fileInputRef.current.value = "";
    };

    return (
        <div
            className={`glass-card ${isDragOver ? 'border-primary' : ''}`}
            style={{
                border: `2px dashed ${isDragOver ? '#48BB78' : '#CBD5E0'}`,
                padding: '40px',
                textAlign: 'center',
                cursor: 'pointer',
                position: 'relative',
                transition: 'all 0.3s'
            }}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={handleFileClick}
        >
            <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileInput}
                style={{ display: 'none' }}
                accept="image/*"
            />

            {preview ? (
                <div style={{ position: 'relative', display: 'inline-block' }}>
                    <img src={preview} alt="Preview" style={{ maxHeight: '300px', borderRadius: '10px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                    <button
                        onClick={clearImage}
                        style={{
                            position: 'absolute',
                            top: '-10px',
                            right: '-10px',
                            background: '#E53E3E',
                            color: 'white',
                            border: 'none',
                            borderRadius: '50%',
                            padding: '5px',
                            cursor: 'pointer'
                        }}
                    >
                        <X size={16} />
                    </button>
                </div>
            ) : (
                <div style={{ color: '#718096' }}>
                    <UploadCloud size={64} style={{ color: '#48BB78', marginBottom: '20px' }} />
                    <h3 style={{ fontSize: '1.2rem', marginBottom: '10px', color: '#2D3748' }}>Drag & Drop Leaf Image Here</h3>
                    <p>or click to browse</p>
                    <p style={{ fontSize: '0.8rem', marginTop: '10px', opacity: 0.7 }}>Supports JPG, PNG</p>
                </div>
            )}
        </div>
    );
};

export default DragDrop;
