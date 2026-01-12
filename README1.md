// src/app/SecuredFilePage.tsx

        import React, { useState, useEffect } from 'react';
        import { useParams } from 'react-router-dom';
        import { securedFilesAPI } from '../services/api';
        import { OTPMethodSelection } from '../components/OTPMethodSelection';
        import { OTPVerification } from '../components/OTPVerification';
        import { PasskeyInput } from '../components/PasskeyInput';
        import { NotFound } from '../components/NotFound';
        import { FileViewer } from '../components/FileViewer';
        import { maskEmail, maskPhone } from '../utils/mask';
        
        type Stage = 'loading' | 'not-found' | 'otp-method' | 'otp-verify' | 'passkey' | 'success';
        
        export const SecuredFilePage: React.FC = () => {
          const { id } = useParams<{ id: string }>();
          const [stage, setStage] = useState<Stage>('loading');
          const [email, setEmail] = useState('');
          const [phone, setPhone] = useState('');
          const [communicationType, setCommunicationType] = useState<'sms' | 'email'>('email');
          const [expiryTime, setExpiryTime] = useState(75);
          const [token, setToken] = useState('');
          const [loading, setLoading] = useState(false);
          const [files, setFiles] = useState<string[]>([]);
        
          useEffect(() => {
            checkAccess();
          }, [id]);
        
          const checkAccess = async () => {
            if (!id) return;
            
            const data = await securedFilesAPI.checkAccess(id);
            
            if (!data.success) {
              setStage('not-found');
            } else {
              setEmail(maskEmail(data.email!));
              setPhone(maskPhone(data.phone!));
              setCommunicationType(data.communicationType!);
              setStage('otp-method');
            }
          };
        
          const handleSendOTP = async (method: 'sms' | 'email') => {
            if (!id) return;
            
            setLoading(true);
            const data = await securedFilesAPI.sendOTP(id, method);
            setLoading(false);
            
            if (data.success) {
              setExpiryTime(data.expiryTime);
              setStage('otp-verify');
            }
          };
        
          const handleVerifyOTP = async (otp: string) => {
            if (!id) return;
            
            setLoading(true);
            const data = await securedFilesAPI.verifyOTP(id, otp);
            setLoading(false);
            
            if (data.success) {
              setToken(data.token);
              setStage('passkey');
            } else {
              alert(data.message);
            }
          };
        
          const handleResendOTP = async () => {
            await handleSendOTP(communicationType);
          };
        
          const handleVerifyPasskey = async (passkey: string) => {
            if (!id) return;
            
            setLoading(true);
            const data = await securedFilesAPI.verifyPasskey(id, passkey, token);
            setLoading(false);
            
            if (data.success) {
              setFiles(data.files || []);
              setStage('success');
            } else {
              alert(data.message);
            }
          };
        
          if (stage === 'loading') return <div>Loading...</div>;
          if (stage === 'not-found') return <NotFound />;
        
          return (
            <div className="secured-file-page">
              {stage === 'otp-method' && (
                <OTPMethodSelection
                  email={email}
                  phone={phone}
                  defaultMethod={communicationType}
                  onSendOTP={handleSendOTP}
                  loading={loading}
                />
              )}
              {stage === 'otp-verify' && (
                <OTPVerification
                  onVerify={handleVerifyOTP}
                  onResend={handleResendOTP}
                  expiryTime={expiryTime}
                  loading={loading}
                />
              )}
              {stage === 'passkey' && (
                <PasskeyInput
                  onSubmit={handleVerifyPasskey}
                  loading={loading}
                />
              )}
              {stage === 'success' && (
                <FileViewer files={files} userId={id!} token={token} />
              )}
            </div>
          );
        };





// src/components/FilePreview.tsx

        import React from 'react';
        import { useFileIcon } from '../hooks/useFileIcon';
        import '../styles/FilePreview.css';
        
        interface FilePreviewProps {
          filename: string;
          userId: string;
          token: string;
          onClose: () => void;
        }
        
        export const FilePreview: React.FC<FilePreviewProps> = ({ filename, userId, token, onClose }) => {
          const { type } = useFileIcon(filename);
          const fileUrl = `/api/files/${userId}/${filename}?token=${token}`;
        
          const handleDownload = () => {
            const link = document.createElement('a');
            link.href = fileUrl;
            link.download = filename;
            link.click();
          };
        
          const renderPreview = () => {
            switch (type) {
              case 'image':
                return <img src={fileUrl} alt={filename} className="preview-content-image" />;
              case 'video':
                return (
                  <video controls className="preview-content-video">
                    <source src={fileUrl} />
                    Your browser does not support the video tag.
                  </video>
                );
              case 'pdf':
                return <iframe src={fileUrl} className="preview-content-iframe" title={filename} />;
              case 'audio':
                return (
                  <div className="preview-audio-container">
                    <audio controls className="preview-content-audio">
                      <source src={fileUrl} />
                      Your browser does not support the audio tag.
                    </audio>
                  </div>
                );
              default:
                return (
                  <div className="preview-unsupported">
                    <p>Preview not available for this file type</p>
                    <button onClick={handleDownload} className="download-btn">
                      Download File
                    </button>
                  </div>
                );
            }
          };
        
          return (
            <div className="file-preview-overlay" onClick={onClose}>
              <div className="file-preview-modal" onClick={(e) => e.stopPropagation()}>
                <div className="file-preview-header">
                  <h3 className="file-preview-title">{filename}</h3>
                  <div className="file-preview-actions">
                    <button onClick={handleDownload} className="action-btn" title="Download">
                      ⬇
                    </button>
                    <button onClick={onClose} className="action-btn close-btn" title="Close">
                      ✕
                    </button>
                  </div>
                </div>
                <div className="file-preview-content">
                  {renderPreview()}
                </div>
              </div>
            </div>
          );
        };


// src/hooks/useFileIcon.ts

        export const useFileIcon = (filename: string) => {
          const extension = filename.split('.').pop()?.toLowerCase() || '';
          
          const imageTypes = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg'];
          const videoTypes = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm'];
          const audioTypes = ['mp3', 'wav', 'ogg', 'flac', 'm4a'];
          const documentTypes = ['doc', 'docx', 'txt', 'rtf'];
          const spreadsheetTypes = ['xls', 'xlsx', 'csv'];
          const presentationTypes = ['ppt', 'pptx'];
          const archiveTypes = ['zip', 'rar', '7z', 'tar', 'gz'];
        
          let icon = '📄';
          let type = 'document';
        
          if (imageTypes.includes(extension)) {
            icon = '🖼️';
            type = 'image';
          } else if (videoTypes.includes(extension)) {
            icon = '🎥';
            type = 'video';
          } else if (audioTypes.includes(extension)) {
            icon = '🎵';
            type = 'audio';
          } else if (extension === 'pdf') {
            icon = '📕';
            type = 'pdf';
          } else if (documentTypes.includes(extension)) {
            icon = '📝';
            type = 'document';
          } else if (spreadsheetTypes.includes(extension)) {
            icon = '📊';
            type = 'spreadsheet';
          } else if (presentationTypes.includes(extension)) {
            icon = '📽️';
            type = 'presentation';
          } else if (archiveTypes.includes(extension)) {
            icon = '🗜️';
            type = 'archive';
          }
        
          return { icon, type, extension };
        };



/* src/styles/FileViewer.css */

        .file-viewer {
          max-width: 1200px;
          margin: 0 auto;
          padding: 2rem;
          background: white;
          min-height: 100vh;
        }
        
        .file-viewer-header {
          margin-bottom: 2rem;
          padding-bottom: 1rem;
          border-bottom: 2px solid #00b3d0;
        }
        
        .file-viewer-header h2 {
          color: #04285b;
          font-size: 2rem;
          margin: 0 0 0.5rem 0;
          font-weight: 600;
        }
        
        .file-count {
          color: #00b3d0;
          font-size: 1rem;
          margin: 0;
          font-weight: 500;
        }

/* src/styles/FilePreview.css */

        .file-preview-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(4, 40, 91, 0.9);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
          padding: 1rem;
          animation: fadeIn 0.2s ease;
        }
        
        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }
        
        .file-preview-modal {
          background: white;
          border-radius: 16px;
          max-width: 90vw;
          max-height: 90vh;
          width: 100%;
          display: flex;
          flex-direction: column;
          overflow: hidden;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
          animation: slideUp 0.3s ease;
        }
        
        @keyframes slideUp {
          from {
            transform: translateY(20px);
            opacity: 0;
          }
          to {
            transform: translateY(0);
            opacity: 1;
          }
        }
        
        .file-preview-header {
          padding: 1.5rem;
          background: #04285b;
          color: white;
          display: flex;
          justify-content: space-between;
          align-items: center;
          border-bottom: 3px solid #00b3d0;
        }
        
        .file-preview-title {
          margin: 0;
          font-size: 1.25rem;
          font-weight: 600;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          flex: 1;
          margin-right: 1rem;
        }
        
        .file-preview-actions {
          display: flex;
          gap: 0.5rem;
        }
        
        .action-btn {
          background: #00b3d0;
          color: white;
          border: none;
          width: 40px;
          height: 40px;
          border-radius: 8px;
          cursor: pointer;
          font-size: 1.25rem;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.2s ease;
        }
        
        .action-btn:hover {
          background: #008fa8;
          transform: scale(1.1);
        }
        
        .close-btn:hover {
          background: #d32f2f;
        }
        
        .file-preview-content {
          flex: 1;
          overflow: auto;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 2rem;
          background: #f5f5f5;
        }
        
        .preview-content-image {
          max-width: 100%;
          max-height: 100%;
          object-fit: contain;
          border-radius: 8px;
        }
        
        .preview-content-video {
          max-width: 100%;
          max-height: 100%;
          border-radius: 8px;
        }
        
        .preview-content-iframe {
          width: 100%;
          height: 100%;
          border: none;
          border-radius: 8px;
        }
        
        .preview-audio-container {
          width: 100%;
          max-width: 600px;
        }
        
        .preview-content-audio {
          width: 100%;
          border-radius: 8px;
        }
        
        .preview-unsupported {
          text-align: center;
          color: #04285b;
        }
        
        .preview-unsupported p {
          font-size: 1.25rem;
          margin-bottom: 1.5rem;
          color: #666;
        }
        
        .download-btn {
          background: #00b3d0;
          color: white;
          border: none;
          padding: 0.875rem 2rem;
          border-radius: 8px;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
        }
        
        .download-btn:hover {
          background: #04285b;
          transform: scale(1.05);
        }
        
        @media (max-width: 768px) {
          .file-preview-modal {
            max-width: 95vw;
            max-height: 95vh;
          }
          
          .file-preview-header {
            padding: 1rem;
          }
          
          .file-preview-title {
            font-size: 1rem;
          }
          
          .action-btn {
            width: 36px;
            height: 36px;
            font-size: 1rem;
          }
          
          .file-preview-content {
            padding: 1rem;
          }
        }


// FileViewer Component

        import React, { useState } from 'react';
        
        const FileViewer = ({ files, userId, token }) => {
          const [selectedFile, setSelectedFile] = useState(null);
        
          return (
            <div style={styles.fileViewer}>
              <div style={styles.fileViewerHeader}>
                <h2 style={styles.headerTitle}>Your Secured Files</h2>
                <p style={styles.fileCount}>{files.length} file{files.length !== 1 ? 's' : ''} available</p>
              </div>
              
              <FileGrid 
                files={files} 
                userId={userId} 
                token={token}
                onFileClick={setSelectedFile}
              />
        
              {selectedFile && (
                <FilePreview
                  filename={selectedFile}
                  userId={userId}
                  token={token}
                  onClose={() => setSelectedFile(null)}
                />
              )}
            </div>
          );
        };
        
        // FileGrid Component
        const FileGrid = ({ files, userId, token, onFileClick }) => {
          return (
            <div style={styles.fileGrid}>
              {files.map((filename, index) => (
                <FileCard
                  key={index}
                  filename={filename}
                  userId={userId}
                  token={token}
                  onClick={() => onFileClick(filename)}
                />
              ))}
            </div>
          );
        };


// FileCard Component

        const FileCard = ({ filename, userId, token, onClick }) => {
          const { icon, type, extension } = useFileIcon(filename);
          const fileUrl = `/api/files/${userId}/${filename}?token=${token}`;
          
          const [imageError, setImageError] = useState(false);
        
          const handleDownload = (e) => {
            e.stopPropagation();
            const link = document.createElement('a');
            link.href = fileUrl;
            link.download = filename;
            link.click();
          };
        
          const renderThumbnail = () => {
            if (type === 'image' && !imageError) {
              return (
                <img 
                  src={fileUrl} 
                  alt={filename}
                  style={styles.thumbnailImage}
                  onError={() => setImageError(true)}
                />
              );
            }
            return (
              <div style={styles.iconContainer}>
                <span style={styles.fileIcon}>{icon}</span>
              </div>
            );
          };
        
          return (
            <div style={styles.fileCard} onClick={onClick}>
              <div style={styles.thumbnailContainer}>
                {renderThumbnail()}
                <div style={styles.fileCardOverlay}>
                  <button style={styles.previewButton}>
                    👁️ Preview
                  </button>
                </div>
              </div>
              <div style={styles.fileCardContent}>
                <div style={styles.fileInfo}>
                  <p style={styles.fileName} title={filename}>{filename}</p>
                  <span style={styles.fileExtension}>{extension.toUpperCase()}</span>
                </div>
                <button 
                  style={styles.downloadButton}
                  onClick={handleDownload}
                  title="Download"
                >
                  ⬇️
                </button>
              </div>
            </div>
          );
        };


// FilePreview Component

        const FilePreview = ({ filename, userId, token, onClose }) => {
          const { type } = useFileIcon(filename);
          const fileUrl = `/api/files/${userId}/${filename}?token=${token}`;
        
          const handleDownload = () => {
            const link = document.createElement('a');
            link.href = fileUrl;
            link.download = filename;
            link.click();
          };
        
          const renderPreview = () => {
            switch (type) {
              case 'image':
                return <img src={fileUrl} alt={filename} style={styles.previewImage} />;
              case 'video':
                return (
                  <video controls style={styles.previewVideo}>
                    <source src={fileUrl} />
                    Your browser does not support the video tag.
                  </video>
                );
              case 'pdf':
                return <iframe src={fileUrl} style={styles.previewIframe} title={filename} />;
              case 'audio':
                return (
                  <div style={styles.audioContainer}>
                    <audio controls style={styles.previewAudio}>
                      <source src={fileUrl} />
                      Your browser does not support the audio tag.
                    </audio>
                  </div>
                );
              default:
                return (
                  <div style={styles.unsupportedPreview}>
                    <p style={styles.unsupportedText}>Preview not available for this file type</p>
                    <button onClick={handleDownload} style={styles.unsupportedDownloadBtn}>
                      Download File
                    </button>
                  </div>
                );
            }
          };
        
          return (
            <div style={styles.previewOverlay} onClick={onClose}>
              <div style={styles.previewModal} onClick={(e) => e.stopPropagation()}>
                <div style={styles.previewHeader}>
                  <h3 style={styles.previewTitle}>{filename}</h3>
                  <div style={styles.previewActions}>
                    <button onClick={handleDownload} style={styles.actionBtn} title="Download">
                      ⬇
                    </button>
                    <button onClick={onClose} style={{...styles.actionBtn, ...styles.closeBtn}} title="Close">
                      ✕
                    </button>
                  </div>
                </div>
                <div style={styles.previewContent}>
                  {renderPreview()}
                </div>
              </div>
            </div>
          );
        };


// useFileIcon Hook

        const useFileIcon = (filename) => {
          const extension = filename.split('.').pop()?.toLowerCase() || '';
          
          const imageTypes = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg'];
          const videoTypes = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm'];
          const audioTypes = ['mp3', 'wav', 'ogg', 'flac', 'm4a'];
          const documentTypes = ['doc', 'docx', 'txt', 'rtf'];
          const spreadsheetTypes = ['xls', 'xlsx', 'csv'];
          const presentationTypes = ['ppt', 'pptx'];
          const archiveTypes = ['zip', 'rar', '7z', 'tar', 'gz'];
        
          let icon = '📄';
          let type = 'document';
        
          if (imageTypes.includes(extension)) {
            icon = '🖼️';
            type = 'image';
          } else if (videoTypes.includes(extension)) {
            icon = '🎥';
            type = 'video';
          } else if (audioTypes.includes(extension)) {
            icon = '🎵';
            type = 'audio';
          } else if (extension === 'pdf') {
            icon = '📕';
            type = 'pdf';
          } else if (documentTypes.includes(extension)) {
            icon = '📝';
            type = 'document';
          } else if (spreadsheetTypes.includes(extension)) {
            icon = '📊';
            type = 'spreadsheet';
          } else if (presentationTypes.includes(extension)) {
            icon = '📽️';
            type = 'presentation';
          } else if (archiveTypes.includes(extension)) {
            icon = '🗜️';
            type = 'archive';
          }
        
          return { icon, type, extension };
        };


// Styles

        const styles = {
          fileViewer: {
            maxWidth: '1200px',
            margin: '0 auto',
            padding: '2rem',
            background: 'white',
            minHeight: '100vh',
          },
          fileViewerHeader: {
            marginBottom: '2rem',
            paddingBottom: '1rem',
            borderBottom: '2px solid #00b3d0',
          },
          headerTitle: {
            color: '#04285b',
            fontSize: '2rem',
            margin: '0 0 0.5rem 0',
            fontWeight: '600',
          },
          fileCount: {
            color: '#00b3d0',
            fontSize: '1rem',
            margin: '0',
            fontWeight: '500',
          },
          fileGrid: {
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
            gap: '1.5rem',
            padding: '1rem 0',
          },
          fileCard: {
            background: 'white',
            borderRadius: '12px',
            overflow: 'hidden',
            boxShadow: '0 2px 8px rgba(4, 40, 91, 0.1)',
            transition: 'all 0.3s ease',
            cursor: 'pointer',
            border: '2px solid transparent',
          },
          thumbnailContainer: {
            position: 'relative',
            width: '100%',
            height: '200px',
            background: '#f5f5f5',
            overflow: 'hidden',
          },
          thumbnailImage: {
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          },
          iconContainer: {
            width: '100%',
            height: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'linear-gradient(135deg, #04285b 0%, #00b3d0 100%)',
          },
          fileIcon: {
            fontSize: '4rem',
          },
          fileCardOverlay: {
            position: 'absolute',
            top: '0',
            left: '0',
            right: '0',
            bottom: '0',
            background: 'rgba(4, 40, 91, 0.9)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            opacity: '0',
            transition: 'opacity 0.3s ease',
          },
          previewButton: {
            background: '#00b3d0',
            color: 'white',
            border: 'none',
            padding: '0.75rem 1.5rem',
            borderRadius: '8px',
            fontSize: '1rem',
            fontWeight: '600',
            cursor: 'pointer',
            transition: 'transform 0.2s ease',
          },
          fileCardContent: {
            padding: '1rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '0.5rem',
            background: 'white',
          },
          fileInfo: {
            flex: '1',
            minWidth: '0',
          },
          fileName: {
            margin: '0 0 0.25rem 0',
            fontSize: '0.95rem',
            fontWeight: '600',
            color: '#04285b',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
          },
          fileExtension: {
            fontSize: '0.75rem',
            color: '#00b3d0',
            fontWeight: '600',
            textTransform: 'uppercase',
          },
          downloadButton: {
            background: '#00b3d0',
            color: 'white',
            border: 'none',
            width: '36px',
            height: '36px',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '1.25rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'all 0.2s ease',
            flexShrink: '0',
          },
          previewOverlay: {
            position: 'fixed',
            top: '0',
            left: '0',
            right: '0',
            bottom: '0',
            background: 'rgba(4, 40, 91, 0.9)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: '1000',
            padding: '1rem',
            animation: 'fadeIn 0.2s ease',
          },
          previewModal: {
            background: 'white',
            borderRadius: '16px',
            maxWidth: '90vw',
            maxHeight: '90vh',
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
            animation: 'slideUp 0.3s ease',
          },
          previewHeader: {
            padding: '1.5rem',
            background: '#04285b',
            color: 'white',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            borderBottom: '3px solid #00b3d0',
          },
          previewTitle: {
            margin: '0',
            fontSize: '1.25rem',
            fontWeight: '600',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
            flex: '1',
            marginRight: '1rem',
          },
          previewActions: {
            display: 'flex',
            gap: '0.5rem',
          },
          actionBtn: {
            background: '#00b3d0',
            color: 'white',
            border: 'none',
            width: '40px',
            height: '40px',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '1.25rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'all 0.2s ease',
          },
          closeBtn: {
            background: '#d32f2f',
          },
          previewContent: {
            flex: '1',
            overflow: 'auto',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '2rem',
            background: '#f5f5f5',
          },
          previewImage: {
            maxWidth: '100%',
            maxHeight: '100%',
            objectFit: 'contain',
            borderRadius: '8px',
          },
          previewVideo: {
            maxWidth: '100%',
            maxHeight: '100%',
            borderRadius: '8px',
          },
          previewIframe: {
            width: '100%',
            height: '100%',
            border: 'none',
            borderRadius: '8px',
          },
          audioContainer: {
            width: '100%',
            maxWidth: '600px',
          },
          previewAudio: {
            width: '100%',
            borderRadius: '8px',
          },
          unsupportedPreview: {
            textAlign: 'center',
            color: '#04285b',
          },
          unsupportedText: {
            fontSize: '1.25rem',
            marginBottom: '1.5rem',
            color: '#666',
          },
          unsupportedDownloadBtn: {
            background: '#00b3d0',
            color: 'white',
            border: 'none',
            padding: '0.875rem 2rem',
            borderRadius: '8px',
            fontSize: '1rem',
            fontWeight: '600',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
          },
        };



BACKEND


// src/controllers/securedFilesController.ts

        import { Request, Response } from 'express';
        import fs from 'fs';
        import path from 'path';
        
        export const verifyPasskey = async (req: Request, res: Response) => {
          try {
            const { id } = req.params;
            const { passkey, token } = req.body;
        
            // Verify token first
            // ... your token verification logic here ...
        
            // Verify passkey
            // ... your passkey verification logic here ...
        
            // If verification successful, get files list
            const uploadsPath = path.join(__dirname, '../../uploads', id);
            
            if (!fs.existsSync(uploadsPath)) {
              return res.status(404).json({
                success: false,
                message: 'User folder not found'
              });
            }
        
            // Read files from the user's folder
            const files = fs.readdirSync(uploadsPath).filter(file => {
              const filePath = path.join(uploadsPath, file);
              return fs.statSync(filePath).isFile();
            });
        
            return res.json({
              success: true,
              message: 'Passkey verified successfully',
              files: files
            });
        
          } catch (error) {
            console.error('Error verifying passkey:', error);
            return res.status(500).json({
              success: false,
              message: 'Server error'
            });
          }
        };
        
        // Add this new endpoint to serve files
        export const getFile = async (req: Request, res: Response) => {
          try {
            const { userId, filename } = req.params;
            const { token } = req.query;
        
            // Verify token
            // ... your token verification logic here ...
        
            const filePath = path.join(__dirname, '../../uploads', userId, filename);
            
            if (!fs.existsSync(filePath)) {
              return res.status(404).json({
                success: false,
                message: 'File not found'
              });
            }
        
            // Send the file
            res.sendFile(filePath);
        
          } catch (error) {
            console.error('Error getting file:', error);
            return res.status(500).json({
              success: false,
              message: 'Server error'
            });
          }
        };



// src/routes/securedFilesRoutes.ts

        import express from 'express';
        import { verifyPasskey, getFile } from '../controllers/securedFilesController';
        
        const router = express.Router();
        
        // Your existing routes...
        // router.post('/check-access/:id', checkAccess);
        // router.post('/send-otp/:id', sendOTP);
        // router.post('/verify-otp/:id', verifyOTP);
        router.post('/verify-passkey/:id', verifyPasskey);
        
        // Add this new route for serving files
        router.get('/files/:userId/:filename', getFile);
        
        export default router;



// src/services/api.ts
        
        const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';
        
        interface CheckAccessResponse {
          success: boolean;
          email?: string;
          phone?: string;
          communicationType?: 'sms' | 'email';
        }
        
        interface SendOTPResponse {
          success: boolean;
          expiryTime: number;
        }
        
        interface VerifyOTPResponse {
          success: boolean;
          token: string;
          message?: string;
        }
        
        interface VerifyPasskeyResponse {
          success: boolean;
          message: string;
          files?: string[];
        }
        
        export const securedFilesAPI = {
          checkAccess: async (id: string): Promise<CheckAccessResponse> => {
            const response = await fetch(`${API_BASE_URL}/check-access/${id}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
            });
            return response.json();
          },
        
          sendOTP: async (id: string, method: 'sms' | 'email'): Promise<SendOTPResponse> => {
            const response = await fetch(`${API_BASE_URL}/send-otp/${id}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({ method }),
            });
            return response.json();
          },
        
          verifyOTP: async (id: string, otp: string): Promise<VerifyOTPResponse> => {
            const response = await fetch(`${API_BASE_URL}/verify-otp/${id}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({ otp }),
            });
            return response.json();
          },
        
          verifyPasskey: async (id: string, passkey: string, token: string): Promise<VerifyPasskeyResponse> => {
            const response = await fetch(`${API_BASE_URL}/verify-passkey/${id}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({ passkey, token }),
            });
            return response.json();
          },
        };









        
