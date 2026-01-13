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


// src/components/FileViewer.tsx

        import React, { useState } from 'react';
        import { FileGrid } from './FileGrid';
        import { FilePreview } from './FilePreview';
        import '../styles/FileViewer.css';
        
        interface FileViewerProps {
          files: string[];
          userId: string;
          token: string;
        }
        
        export const FileViewer: React.FC<FileViewerProps> = ({ files, userId, token }) => {
          const [selectedFile, setSelectedFile] = useState<string | null>(null);
        
          const handleFileClick = (filename: string) => {
            setSelectedFile(filename);
          };
        
          const handleClose = () => {
            setSelectedFile(null);
          };
        
          return (
            <div className="file-viewer">
              <div className="file-viewer-header">
                <h2>Secured Files</h2>
                <p className="file-count">{files.length} file{files.length !== 1 ? 's' : ''}</p>
              </div>
        
              <FileGrid 
                files={files} 
                userId={userId} 
                token={token}
                onFileClick={handleFileClick}
              />
        
              {selectedFile && (
                <FilePreview
                  filename={selectedFile}
                  userId={userId}
                  token={token}
                  onClose={handleClose}
                />
              )}
            </div>
          );
        };



// src/components/FileGrid.tsx

        import React from 'react';
        import { FileCard } from './FileCard';
        import { useFileIcon } from '../hooks/useFileIcon';
        import '../styles/FileGrid.css';
        
        interface FileGridProps {
          files: string[];
          userId: string;
          token: string;
          onFileClick: (filename: string) => void;
        }
        
        export const FileGrid: React.FC<FileGridProps> = ({ files, userId, token, onFileClick }) => {
          return (
            <div className="file-grid">
              {files.map((filename) => (
                <FileCard
                  key={filename}
                  filename={filename}
                  userId={userId}
                  token={token}
                  onClick={() => onFileClick(filename)}
                />
              ))}
            </div>
          );
        };


// src/components/FileCard.tsx

        import React from 'react';
        import { useFileIcon } from '../hooks/useFileIcon';
        import '../styles/FileCard.css';
        
        interface FileCardProps {
          filename: string;
          userId: string;
          token: string;
          onClick: () => void;
        }
        
        export const FileCard: React.FC<FileCardProps> = ({ filename, userId, token, onClick }) => {
          const { icon, type } = useFileIcon(filename);
          const fileUrl = `/api/files/${userId}/${filename}?token=${token}`;
        
          return (
            <div className="file-card" onClick={onClick}>
              <div className="file-card-preview">
                {type === 'image' ? (
                  <img src={fileUrl} alt={filename} className="file-thumbnail" />
                ) : (
                  <div className="file-icon">{icon}</div>
                )}
              </div>
              <div className="file-card-name" title={filename}>
                {filename}
              </div>
            </div>
          );
        };

// src/components/FilePreview.tsx

        import React from 'react';
        import { Download, X, FileText, Image, Film, Music, File } from 'lucide-react';
        
        interface FilePreviewProps {
          filename: string;
          userId: string;
          token: string;
          onClose: () => void;
        }
        
        const useFileIcon = (filename: string) => {
          const ext = filename.split('.').pop()?.toLowerCase() || '';
          
          const imageExts = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp'];
          const videoExts = ['mp4', 'webm', 'ogg', 'mov', 'avi'];
          const audioExts = ['mp3', 'wav', 'ogg', 'flac', 'm4a'];
          const pdfExts = ['pdf'];
          
          if (imageExts.includes(ext)) return { type: 'image', Icon: Image };
          if (videoExts.includes(ext)) return { type: 'video', Icon: Film };
          if (audioExts.includes(ext)) return { type: 'audio', Icon: Music };
          if (pdfExts.includes(ext)) return { type: 'pdf', Icon: FileText };
          
          return { type: 'other', Icon: File };
        };
        
        export const FilePreview: React.FC<FilePreviewProps> = ({ filename, userId, token, onClose }) => {
          const { type, Icon } = useFileIcon(filename);
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
                return (
                  <div className="flex items-center justify-center h-full p-8">
                    <img 
                      src={fileUrl} 
                      alt={filename} 
                      className="max-w-full max-h-full object-contain rounded-lg shadow-2xl"
                    />
                  </div>
                );
              case 'video':
                return (
                  <div className="flex items-center justify-center h-full p-8">
                    <video 
                      controls 
                      className="max-w-full max-h-full rounded-lg shadow-2xl"
                    >
                      <source src={fileUrl} />
                      Your browser does not support the video tag.
                    </video>
                  </div>
                );
              case 'pdf':
                return (
                  <iframe 
                    src={fileUrl} 
                    className="w-full h-full border-0"
                    title={filename} 
                  />
                );
              case 'audio':
                return (
                  <div className="flex flex-col items-center justify-center h-full gap-8 p-8">
                    <div className="w-32 h-32 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center shadow-2xl">
                      <Music className="w-16 h-16 text-white" />
                    </div>
                    <div className="w-full max-w-md">
                      <audio controls className="w-full">
                        <source src={fileUrl} />
                        Your browser does not support the audio tag.
                      </audio>
                    </div>
                  </div>
                );
              default:
                return (
                  <div className="flex flex-col items-center justify-center h-full gap-6 p-8">
                    <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center">
                      <Icon className="w-12 h-12 text-gray-400" />
                    </div>
                    <div className="text-center">
                      <p className="text-gray-600 text-lg mb-4">Preview not available for this file type</p>
                      <button 
                        onClick={handleDownload} 
                        className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 mx-auto shadow-lg hover:shadow-xl"
                      >
                        <Download className="w-5 h-5" />
                        Download File
                      </button>
                    </div>
                  </div>
                );
            }
          };
        
          return (
            <div 
              className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in duration-200"
              onClick={onClose}
            >
              <div 
                className="bg-white rounded-2xl shadow-2xl w-full max-w-6xl h-[90vh] flex flex-col animate-in zoom-in-95 duration-200"
                onClick={(e) => e.stopPropagation()}
              >
                {/* Header */}
                <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-white rounded-t-2xl">
                  <div className="flex items-center gap-3 flex-1 min-w-0">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center flex-shrink-0 shadow-md">
                      <Icon className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-800 truncate" title={filename}>
                      {filename}
                    </h3>
                  </div>
                  
                  <div className="flex items-center gap-2 ml-4">
                    <button 
                      onClick={handleDownload} 
                      className="p-2.5 hover:bg-gray-100 rounded-lg transition-colors group"
                      title="Download"
                    >
                      <Download className="w-5 h-5 text-gray-600 group-hover:text-blue-600 transition-colors" />
                    </button>
                    <button 
                      onClick={onClose} 
                      className="p-2.5 hover:bg-red-50 rounded-lg transition-colors group"
                      title="Close"
                    >
                      <X className="w-5 h-5 text-gray-600 group-hover:text-red-600 transition-colors" />
                    </button>
                  </div>
                </div>
        
                {/* Content */}
                <div className="flex-1 overflow-hidden bg-gray-50">
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

/* src/styles/FileGrid.css */

        .file-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
          gap: 1.5rem;
          padding: 1rem 0;
        }
        
        @media (max-width: 768px) {
          .file-grid {
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 1rem;
          }
        }
        
        @media (max-width: 480px) {
          .file-grid {
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 0.75rem;
          }
        }


/* src/styles/FileCard.css */

        .file-card {
          background: white;
          border: 2px solid #e0e0e0;
          border-radius: 12px;
          overflow: hidden;
          cursor: pointer;
          transition: all 0.3s ease;
          display: flex;
          flex-direction: column;
        }
        
        .file-card:hover {
          border-color: #00b3d0;
          transform: translateY(-4px);
          box-shadow: 0 8px 16px rgba(0, 179, 208, 0.2);
        }
        
        .file-card-preview {
          width: 100%;
          height: 180px;
          background: #f5f5f5;
          display: flex;
          align-items: center;
          justify-content: center;
          overflow: hidden;
          position: relative;
        }
        
        .file-thumbnail {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
        
        .file-icon {
          font-size: 4rem;
          color: #04285b;
        }
        
        .file-card-name {
          padding: 0.75rem;
          font-size: 0.875rem;
          color: #04285b;
          text-align: center;
          word-break: break-word;
          line-height: 1.4;
          background: white;
          border-top: 1px solid #e0e0e0;
          font-weight: 500;
        }
        
        @media (max-width: 480px) {
          .file-card-preview {
            height: 140px;
          }
          
          .file-icon {
            font-size: 3rem;
          }
          
          .file-card-name {
            font-size: 0.75rem;
            padding: 0.5rem;
          }
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









        
