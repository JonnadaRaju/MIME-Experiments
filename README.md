# MIME Types Demo

A full-stack application demonstrating all major MIME types with Postman-testable endpoints.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the server:**
   ```bash
   npm start
   # or for development
   npm run dev
   ```

3. **Access the application:**
   - Web Interface: http://localhost:4000
   - API Base URL: http://localhost:4000/api

## 📋 Available MIME Types

### 📝 Text MIME Types
- `GET /api/text/plain` - Plain text content
- `GET /api/text/html` - HTML document
- `GET /api/text/css` - CSS stylesheet
- `GET /api/text/javascript` - JavaScript code
- `GET /api/text/csv` - CSV data (downloads file)

### ⚙️ Application MIME Types
- `GET /api/application/json` - JSON data
- `GET /api/application/xml` - XML document
- `GET /api/application/pdf` - PDF file (downloads)
- `GET /api/application/zip` - ZIP archive (downloads)
- `GET /api/application/octet-stream` - Binary data

### 🖼️ Image MIME Types
- `GET /api/image/jpeg` - JPEG image
- `GET /api/image/png` - PNG image
- `GET /api/image/svg+xml` - SVG vector graphic
- `GET /api/image/gif` - GIF image

### 🎥 Video MIME Types
- `GET /api/video/mp4` - MP4 video
- `GET /api/video/webm` - WebM video

### 📦 Multipart MIME Types
- `POST /api/multipart/form-data` - Single file upload
- `POST /api/multipart/multiple` - Multiple files upload

### ✉️ Message MIME Types
- `GET /api/message/rfc822` - Email message format
- `GET /api/message/http` - HTTP message format

### 📋 Utility
- `GET /api/endpoints` - Lists all available endpoints

## 🧪 Testing with Postman

1. **Import the collection:**
   ```bash
   # Open Postman and import:
   postman-collection.json
   ```

2. **Set environment variable:**
   - Variable: `baseUrl`
   - Initial value: `http://localhost:4000`

3. **Test endpoints:**
   - Click on any request in the collection
   - Send the request and observe the Content-Type header
   - Check response body format

## 🌐 Web Interface

Visit http://localhost:4000 to use the interactive web interface that allows you to:
- Test all MIME type endpoints
- Upload files for multipart testing
- View response headers and content
- Download binary files

## 📁 File Uploads

The application supports file uploads for testing multipart/form-data:
- Single file upload: `POST /api/multipart/form-data`
- Multiple files upload: `POST /api/multipart/multiple`
- Uploaded files are stored in the `uploads/` directory
- Maximum file size: 10MB

## 🔧 API Examples

### Testing Text MIME Types
```bash
# Plain text
curl -H "Accept: text/plain" http://localhost:3000/api/text/plain

# JSON
curl -H "Accept: application/json" http://localhost:3000/api/application/json

# Download CSV
curl -O http://localhost:3000/api/text/csv
```

### File Upload with curl
```bash
# Single file
curl -X POST -F "file=@test.txt" -F "name=John" http://localhost:3000/api/multipart/form-data

# Multiple files
curl -X POST -F "files=@file1.txt" -F "files=@file2.txt" http://localhost:3000/api/multipart/multiple
```

## 📝 What You'll Learn

- How different MIME types are served
- Content-Type headers in action
- File upload handling with multipart
- Binary vs text content delivery
- Browser behavior with different MIME types

## 🛠️ Technologies Used

- **Backend:** Node.js, Express.js
- **File Upload:** Multer
- **Security:** Helmet, CORS
- **Frontend:** Vanilla HTML/CSS/JavaScript
- **Testing:** Postman Collection

## 📂 Project Structure

```
mime/
├── server.js                 # Express server with all endpoints
├── package.json              # Dependencies and scripts
├── postman-collection.json   # Postman collection for testing
├── public/
│   └── index.html           # Interactive web interface
├── uploads/                 # File upload directory (auto-created)
└── README.md                # This file
```

## 🚨 Important Notes

- Binary files (PDF, ZIP, images) will download automatically in browsers
- Video files contain minimal headers for demonstration
- Some endpoints return minimal valid files for testing purposes
- Always check the `Content-Type` header to verify MIME type

## 🎯 Learning Outcomes

After using this demo, you'll understand:
1. How MIME types are declared in HTTP headers
2. Browser behavior with different content types
3. File upload mechanics with multipart/form-data
4. Binary vs text content handling
5. Practical API testing with Postman