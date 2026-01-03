# File Transfer App - Folder Structure

## Project Structure
```
src/
├── app/
│   └── App.tsx
├── components/
│   ├── FileUploadZone.tsx
│   ├── FileList.tsx
│   ├── ReceiverModal.tsx
│   ├── StoredFilesList.tsx
│   ├── LoadingOverlay.tsx
│   ├── Notification.tsx
│   └── NotificationPanel.tsx
├── hooks/
│   ├── useFileStorage.ts
│   └── useNotification.ts
├── services/
│   └── fileStorage.service.ts
├── types/
│   └── index.ts
├── utils/
│   ├── validation.ts
│   └── formatters.ts
├── styles/
│   └── index.css
└── main.tsx
```

---

## File: `src/types/index.ts`

```typescript
export interface FileData {
  id: string;
  name: string;
  size: number;
  type: string;
  data: string;
  timestamp: number;
  receiverEmail: string;
  receiverPhone: string;
  communicationMethod: 'email' | 'sms';
  isNew?: boolean;
}

export interface ReceiverDetails {
  email: string;
  phone: string;
  communicationMethod: 'email' | 'sms';
}

export interface ValidationErrors {
  email?: string;
  phone?: string;
}
```

---

## File: `src/utils/validation.ts`

```typescript
export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validatePhone = (phone: string): boolean => {
  const phoneRegex = /^[0-9]{10}$/;
  return phoneRegex.test(phone.replace(/[-\s()]/g, ''));
};

export const validateReceiverDetails = (
  email: string,
  phone: string
): { isValid: boolean; errors: { email?: string; phone?: string } } => {
  const errors: { email?: string; phone?: string } = {};

  if (!email.trim()) {
    errors.email = 'Email is required';
  } else if (!validateEmail(email)) {
    errors.email = 'Please enter a valid email address';
  }

  if (!phone.trim()) {
    errors.phone = 'Phone number is required';
  } else if (!validatePhone(phone)) {
    errors.phone = 'Please enter a valid 10-digit phone number';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};
```

---

## File: `src/utils/formatters.ts`

```typescript
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
};

export const formatDate = (timestamp: number): string => {
  return new Date(timestamp).toLocaleString();
};
```

---

## File: `src/services/fileStorage.service.ts`

```typescript
import { FileData } from '../types';

export const fileStorageService = {
  saveFile: (fileData: FileData): void => {
    const dataToSave = { ...fileData, isNew: true };
    localStorage.setItem(fileData.id, JSON.stringify(dataToSave));
  },

  getFile: (id: string): FileData | null => {
    const data = localStorage.getItem(id);
    return data ? JSON.parse(data) : null;
  },

  getAllFiles: (): FileData[] => {
    const files: FileData[] = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key?.startsWith('file_')) {
        try {
          const fileData = JSON.parse(localStorage.getItem(key) || '');
          files.push(fileData);
        } catch (e) {
          console.error('Error loading file:', e);
        }
      }
    }
    return files.sort((a, b) => b.timestamp - a.timestamp);
  },

  getNewFiles: (): FileData[] => {
    return fileStorageService.getAllFiles().filter(file => file.isNew);
  },

  markFileAsRead: (id: string): void => {
    const file = fileStorageService.getFile(id);
    if (file) {
      file.isNew = false;
      localStorage.setItem(id, JSON.stringify(file));
    }
  },

  markAllFilesAsRead: (): void => {
    const files = fileStorageService.getAllFiles();
    files.forEach(file => {
      if (file.isNew) {
        file.isNew = false;
        localStorage.setItem(file.id, JSON.stringify(file));
      }
    });
  },

  deleteFile: (id: string): void => {
    localStorage.removeItem(id);
  },

  readFileAsBase64: (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }
};
```

---

## File: `src/hooks/useNotification.ts`

```typescript
import { useState, useCallback } from 'react';

export const useNotification = () => {
  const [notification, setNotification] = useState<string>('');

  const showNotification = useCallback((message: string) => {
    setNotification(message);
    setTimeout(() => setNotification(''), 3000);
  }, []);

  return { notification, showNotification };
};
```

---

## File: `src/hooks/useFileStorage.ts`

```typescript
import { useState, useEffect, useCallback } from 'react';
import { FileData, ReceiverDetails } from '../types';
import { fileStorageService } from '../services/fileStorage.service';

export const useFileStorage = () => {
  const [storedFiles, setStoredFiles] = useState<FileData[]>([]);
  const [newFilesCount, setNewFilesCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  const loadFiles = useCallback(() => {
    const files = fileStorageService.getAllFiles();
    setStoredFiles(files);
    setNewFilesCount(files.filter(f => f.isNew).length);
  }, []);

  useEffect(() => {
    loadFiles();
  }, [loadFiles]);

  const uploadFiles = async (
    files: File[],
    receiverDetails: ReceiverDetails
  ): Promise<void> => {
    setIsLoading(true);

    try {
      for (const file of files) {
        const data = await fileStorageService.readFileAsBase64(file);
        const fileData: FileData = {
          id: `file_${Date.now()}_${Math.random()}`,
          name: file.name,
          size: file.size,
          type: file.type,
          data,
          timestamp: Date.now(),
          receiverEmail: receiverDetails.email,
          receiverPhone: receiverDetails.phone,
          communicationMethod: receiverDetails.communicationMethod,
          isNew: true
        };
        fileStorageService.saveFile(fileData);
      }
      loadFiles();
    } finally {
      setIsLoading(false);
    }
  };

  const deleteFile = useCallback((id: string) => {
    fileStorageService.deleteFile(id);
    loadFiles();
  }, [loadFiles]);

  const downloadFile = useCallback((fileData: FileData) => {
    const link = document.createElement('a');
    link.href = fileData.data;
    link.download = fileData.name;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }, []);

  const markAsRead = useCallback((id: string) => {
    fileStorageService.markFileAsRead(id);
    loadFiles();
  }, [loadFiles]);

  const markAllAsRead = useCallback(() => {
    fileStorageService.markAllFilesAsRead();
    loadFiles();
  }, [loadFiles]);

  return {
    storedFiles,
    newFilesCount,
    isLoading,
    uploadFiles,
    deleteFile,
    downloadFile,
    markAsRead,
    markAllAsRead
  };
};
```

---

## File: `src/components/NotificationPanel.tsx`

```typescript
import React from 'react';
import { X, Download, Mail, Phone, FileIcon, ExternalLink } from 'lucide-react';
import { FileData } from '../types';
import { formatFileSize, formatDate } from '../utils/formatters';

interface NotificationPanelProps {
  isOpen: boolean;
  newFiles: FileData[];
  onClose: () => void;
  onDownload: (file: FileData) => void;
  onMarkAsRead: (id: string) => void;
  onMarkAllAsRead: () => void;
}

export const NotificationPanel: React.FC<NotificationPanelProps> = ({
  isOpen,
  newFiles,
  onClose,
  onDownload,
  onMarkAsRead,
  onMarkAllAsRead
}) => {
  if (!isOpen) return null;

  const handleDownload = (file: FileData) => {
    onDownload(file);
    onMarkAsRead(file.id);
  };

  return (
    <>
      <div 
        className="fixed inset-0 bg-black bg-opacity-30 z-40"
        onClick={onClose}
      />
      <div className="fixed right-0 top-0 h-full w-full max-w-md bg-white shadow-2xl z-50 flex flex-col">
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-4 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-white">Notifications</h2>
            <p className="text-blue-100 text-sm">{newFiles.length} new file{newFiles.length !== 1 ? 's' : ''}</p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-white hover:bg-opacity-20 p-2 rounded-lg transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        {newFiles.length > 0 && (
          <div className="p-4 border-b bg-gray-50">
            <button
              onClick={onMarkAllAsRead}
              className="text-blue-600 hover:text-blue-800 font-semibold text-sm"
            >
              Mark all as read
            </button>
          </div>
        )}

        <div className="flex-1 overflow-y-auto p-4">
          {newFiles.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <FileIcon size={48} className="mx-auto mb-4 opacity-50" />
              <p>No new notifications</p>
            </div>
          ) : (
            <div className="space-y-3">
              {newFiles.map((file) => (
                <div
                  key={file.id}
                  className="bg-blue-50 border border-blue-200 rounded-lg p-4 hover:bg-blue-100 transition-colors"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-start flex-1 min-w-0">
                      <FileIcon className="text-blue-600 mr-3 flex-shrink-0 mt-1" size={20} />
                      <div className="min-w-0 flex-1">
                        <p className="font-semibold text-gray-900 truncate">{file.name}</p>
                        <p className="text-sm text-gray-600 mt-1">
                          {formatFileSize(file.size)}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">
                          {formatDate(file.timestamp)}
                        </p>
                      </div>
                    </div>
                    <span className="ml-2 w-2 h-2 bg-blue-600 rounded-full flex-shrink-0 mt-2"></span>
                  </div>

                  <div className="mt-3 pt-3 border-t border-blue-200">
                    <div className="space-y-1 mb-3">
                      <div className="flex items-center text-sm text-gray-700">
                        <Mail size={14} className="mr-2 text-blue-600" />
                        <span className="truncate">{file.receiverEmail}</span>
                      </div>
                      <div className="flex items-center text-sm text-gray-700">
                        <Phone size={14} className="mr-2 text-blue-600" />
                        <span>{file.receiverPhone}</span>
                      </div>
                      <div className="flex items-center text-sm">
                        <span className="px-2 py-1 bg-blue-600 text-white rounded text-xs font-semibold">
                          {file.communicationMethod.toUpperCase()}
                        </span>
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <button
                        onClick={() => handleDownload(file)}
                        className="flex-1 bg-blue-600 text-white px-3 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm font-semibold flex items-center justify-center"
                      >
                        <Download size={16} className="mr-2" />
                        Download
                      </button>
                      <button
                        onClick={() => onMarkAsRead(file.id)}
                        className="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors text-sm"
                      >
                        <X size={16} />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
};
```

---

## File: `src/components/Notification.tsx`

```typescript
import React from 'react';

interface NotificationProps {
  message: string;
}

export const Notification: React.FC<NotificationProps> = ({ message }) => {
  if (!message) return null;

  return (
    <div className="bg-green-500 text-white px-6 py-3 text-center font-medium">
      {message}
    </div>
  );
};
```

---

## File: `src/components/LoadingOverlay.tsx`

```typescript
import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingOverlayProps {
  isLoading: boolean;
}

export const LoadingOverlay: React.FC<LoadingOverlayProps> = ({ isLoading }) => {
  if (!isLoading) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 flex flex-col items-center">
        <Loader2 className="animate-spin text-blue-600 mb-4" size={48} />
        <p className="text-xl font-semibold">Please wait...</p>
        <p className="text-gray-600 mt-2">Processing your files</p>
      </div>
    </div>
  );
};
```

---

## File: `src/components/FileUploadZone.tsx`

```typescript
import React, { useRef, useState } from 'react';
import { Upload } from 'lucide-react';

interface FileUploadZoneProps {
  onFilesSelected: (files: File[]) => void;
}

export const FileUploadZone: React.FC<FileUploadZoneProps> = ({ onFilesSelected }) => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    onFilesSelected(droppedFiles);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      onFilesSelected(selectedFiles);
    }
  };

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors cursor-pointer ${
        isDragging
          ? 'border-blue-600 bg-blue-50'
          : 'border-gray-300 hover:border-blue-400'
      }`}
      onClick={() => fileInputRef.current?.click()}
    >
      <Upload className="mx-auto mb-4 text-gray-400" size={48} />
      <p className="text-lg font-semibold text-gray-700 mb-2">
        Drag & drop files here
      </p>
      <p className="text-gray-500 mb-4">or click to browse</p>
      <input
        ref={fileInputRef}
        type="file"
        multiple
        onChange={handleFileSelect}
        className="hidden"
      />
    </div>
  );
};
```

---

## File: `src/components/FileList.tsx`

```typescript
import React from 'react';
import { File, X } from 'lucide-react';
import { formatFileSize } from '../utils/formatters';

interface FileListProps {
  files: File[];
  onRemove: (index: number) => void;
  onUpload: () => void;
}

export const FileList: React.FC<FileListProps> = ({ files, onRemove, onUpload }) => {
  if (files.length === 0) return null;

  return (
    <div className="mt-6">
      <h3 className="font-semibold text-lg mb-3">Selected Files ({files.length})</h3>
      <div className="space-y-2 max-h-64 overflow-y-auto">
        {files.map((file, index) => (
          <div
            key={index}
            className="flex items-center justify-between bg-gray-50 p-3 rounded-lg"
          >
            <div className="flex items-center flex-1 min-w-0">
              <File className="text-blue-600 mr-3 flex-shrink-0" size={24} />
              <div className="min-w-0 flex-1">
                <p className="font-medium truncate">{file.name}</p>
                <p className="text-sm text-gray-500">{formatFileSize(file.size)}</p>
              </div>
            </div>
            <button
              onClick={() => onRemove(index)}
              className="ml-3 text-red-500 hover:text-red-700 flex-shrink-0"
            >
              <X size={20} />
            </button>
          </div>
        ))}
      </div>

      <button
        onClick={onUpload}
        className="w-full mt-6 bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
      >
        Upload Files
      </button>
    </div>
  );
};
```

---

## File: `src/components/ReceiverModal.tsx`

```typescript
import React, { useState } from 'react';
import { Mail, Phone } from 'lucide-react';
import { ReceiverDetails, ValidationErrors } from '../types';
import { validateReceiverDetails } from '../utils/validation';

interface ReceiverModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (details: ReceiverDetails) => void;
}

export const ReceiverModal: React.FC<ReceiverModalProps> = ({
  isOpen,
  onClose,
  onSubmit
}) => {
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [communicationMethod, setCommunicationMethod] = useState<'email' | 'sms'>('email');
  const [errors, setErrors] = useState<ValidationErrors>({});

  if (!isOpen) return null;

  const handleSubmit = () => {
    const validation = validateReceiverDetails(email, phone);
    
    if (!validation.isValid) {
      setErrors(validation.errors);
      return;
    }

    onSubmit({ email, phone, communicationMethod });
    setEmail('');
    setPhone('');
    setCommunicationMethod('email');
    setErrors({});
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg p-6 max-w-md w-full">
        <h2 className="text-2xl font-bold mb-4">Receiver Details</h2>
        
        <div className="mb-4">
          <label className="block text-sm font-semibold mb-2">
            Receiver Email <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <Mail className="absolute left-3 top-3 text-gray-400" size={20} />
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={`w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.email ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="example@email.com"
            />
          </div>
          {errors.email && (
            <p className="text-red-500 text-sm mt-1">{errors.email}</p>
          )}
        </div>

        <div className="mb-4">
          <label className="block text-sm font-semibold mb-2">
            Receiver Phone <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <Phone className="absolute left-3 top-3 text-gray-400" size={20} />
            <input
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className={`w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.phone ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="1234567890"
            />
          </div>
          {errors.phone && (
            <p className="text-red-500 text-sm mt-1">{errors.phone}</p>
          )}
        </div>

        <div className="mb-6">
          <label className="block text-sm font-semibold mb-3">
            Communication Method <span className="text-red-500">*</span>
          </label>
          <div className="space-y-2">
            <label className="flex items-center cursor-pointer">
              <input
                type="radio"
                name="communicationMethod"
                value="email"
                checked={communicationMethod === 'email'}
                onChange={() => setCommunicationMethod('email')}
                className="w-4 h-4 text-blue-600 focus:ring-blue-500"
              />
              <Mail className="ml-3 mr-2 text-blue-600" size={18} />
              <span className="text-gray-700">Email</span>
            </label>
            <label className="flex items-center cursor-pointer">
              <input
                type="radio"
                name="communicationMethod"
                value="sms"
                checked={communicationMethod === 'sms'}
                onChange={() => setCommunicationMethod('sms')}
                className="w-4 h-4 text-blue-600 focus:ring-blue-500"
              />
              <Phone className="ml-3 mr-2 text-blue-600" size={18} />
              <span className="text-gray-700">Phone SMS</span>
            </label>
          </div>
        </div>

        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 bg-gray-300 text-gray-700 py-2 rounded-lg font-semibold hover:bg-gray-400 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            className="flex-1 bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Submit
          </button>
        </div>
      </div>
    </div>
  );
};
```

---

## File: `src/components/StoredFilesList.tsx`

```typescript
import React from 'react';
import { File, Download, X, Mail, Phone } from 'lucide-react';
import { FileData } from '../types';
import { formatFileSize, formatDate } from '../utils/formatters';

interface StoredFilesListProps {
  files: FileData[];
  onDownload: (file: FileData) => void;
  onDelete: (id: string) => void;
}

export const StoredFilesList: React.FC<StoredFilesListProps> = ({
  files,
  onDownload,
  onDelete
}) => {
  if (files.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <Download size={48} className="mx-auto mb-4 opacity-50" />
        <p>No files available</p>
      </div>
    );
  }

  return (
    <div className="space-y-2 max-h-96 overflow-y-auto">
      {files.map((file) => (
        <div
          key={file.id}
          className="bg-gray-50 p-4 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center flex-1 min-w-0">
              <File className="text-blue-600 mr-3 flex-shrink-0" size={24} />
              <div className="min-w-0 flex-1">
                <p className="font-medium truncate">{file.name}</p>
                <p className="text-sm text-gray-500">
                  {formatFileSize(file.size)} • {formatDate(file.timestamp)}
                </p>
              </div>
            </div>
            <div className="flex gap-2 ml-3">
              <button
                onClick={() => onDownload(file)}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex-shrink-0"
              >
                <Download size={18} />
              </button>
              <button
                onClick={() => onDelete(file.id)}
                className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors flex-shrink-0"
              >
                <X size={18} />
              </button>
            </div>
          </div>
          <div className="flex gap-4 text-sm text-gray-600 mt-2 pt-2 border-t border-gray-200">
            <span className="flex items-center">
              <Mail size={14} className="mr-1" />
              {file.receiverEmail}
            </span>
            <span className="flex items-center">
              <Phone size={14} className="mr-1" />
              {file.receiverPhone}
            </span>
            <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-semibold">
              {file.communicationMethod.toUpperCase()}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
};
```

---

## File: `src/app/App.tsx`

```typescript
import React, { useState } from 'react';
import { Upload, Download, Bell } from 'lucide-react';
import { FileUploadZone } from '../components/FileUploadZone';
import { FileList } from '../components/FileList';
import { ReceiverModal } from '../components/ReceiverModal';
import { StoredFilesList } from '../components/StoredFilesList';
import { LoadingOverlay } from '../components/LoadingOverlay';
import { Notification } from '../components/Notification';
import { NotificationPanel } from '../components/NotificationPanel';
import { useFileStorage } from '../hooks/useFileStorage';
import { useNotification } from '../hooks/useNotification';
import { ReceiverDetails } from '../types';

const App: React.FC = () => {
  const [mode, setMode] = useState<'send' | 'receive'>('send');
  const [files, setFiles] = useState<File[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [showNotificationPanel, setShowNotificationPanel] = useState(false);

  const { 
    storedFiles, 
    newFilesCount, 
    isLoading, 
    uploadFiles, 
    deleteFile, 
    downloadFile,
    markAsRead,
    markAllAsRead
  } = useFileStorage();
  const { notification, showNotification } = useNotification();

  const newFiles = storedFiles.filter(file => file.isNew);

  const handleFilesSelected = (newFiles: File[]) => {
    setFiles(prev => [...prev, ...newFiles]);
  };

  const handleRemoveFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleUploadClick = () => {
    if (files.length === 0) {
      showNotification('Please select files to upload');
      return;
    }
    setShowModal(true);
  };

  const handleSubmitReceiverDetails = async (details: ReceiverDetails) => {
    setShowModal(false);
    await uploadFiles(files, details);
    showNotification(`${files.length} file(s) uploaded successfully via ${details.communicationMethod}!`);
    setFiles([]);
  };

  const handleDownload = (file: any) => {
    downloadFile(file);
    showNotification(`Downloading ${file.name}`);
  };

  const handleDelete = (id: string) => {
    deleteFile(id);
    showNotification('File deleted');
  };

  const handleNotificationDownload = (file: any) => {
    downloadFile(file);
    showNotification(`Downloading ${file.name}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-xl overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-6 relative">
            <h1 className="text-3xl font-bold text-white text-center">File Transfer</h1>
            
            <button
              onClick={() => setShowNotificationPanel(true)}
              className="absolute right-6 top-1/2 -translate-y-1/2 text-white hover:bg-white hover:bg-opacity-20 p-2 rounded-lg transition-colors relative"
            >
              <Bell size={24} />
              {newFilesCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                  {newFilesCount > 9 ? '9+' : newFilesCount}
                </span>
              )}
            </button>
          </div>

          <Notification message={notification} />

          <div className="flex border-b">
            <button
              onClick={() => setMode('send')}
              className={`flex-1 py-4 font-semibold transition-colors ${
                mode === 'send'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              <Upload className="inline mr-2" size={20} />
              Send Files
            </button>
            <button
              onClick={() => setMode('receive')}
              className={`flex-1 py-4 font-semibold transition-colors ${
                mode === 'receive'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              <Download className="inline mr-2" size={20} />
              Receive Files
            </button>
          </div>

          <div className="p-6">
            <LoadingOverlay isLoading={isLoading} />

            <ReceiverModal
              isOpen={showModal}
              onClose={() => setShowModal(false)}
              onSubmit={handleSubmitReceiverDetails}
            />

            <NotificationPanel
              isOpen={showNotificationPanel}
              newFiles={newFiles}
              onClose={() => setShowNotificationPanel(false)}
              onDownload={handleNotificationDownload}
              onMarkAsRead={markAsRead}
              onMarkAllAsRead={markAllAsRead}
            />

            {mode === 'send' ? (
              <div>
                <FileUploadZone onFilesSelected={handleFilesSelected} />
                <FileList
                  files={files}
                  onRemove={handleRemoveFile}
                  onUpload={handleUploadClick}
                />
              </div>
            ) : (
              <div>
                <h3 className="font-semibold text-lg mb-4">
                  Stored Files ({storedFiles.length})
                </h3>
                <StoredFilesList
                  files={storedFiles}
                  onDownload={handleDownload}
                  onDelete={handleDelete}
                />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
```

---

## File: `src/main.tsx`

```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './app/App';
import './styles/index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

---

## File: `src/styles/index.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
```

---

## Additional Configuration Files

### `vite.config.ts`

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': '/src'
    }
  }
});
```

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### `package.json`

```json
{
  "name": "file-transfer-app",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "lucide-react": "^0.263.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.2.2",
    "vite": "^5.0.8"
  }
}
```

---

## Installation & Running

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

This structure follows React best practices with clear separation of concerns, making the codebase maintainable and scalable!
