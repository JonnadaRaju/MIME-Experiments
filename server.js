const express = require('express');
const multer = require('multer');
const cors = require('cors');
const helmet = require('helmet');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 4000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Ensure uploads directory exists
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir);
}

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, uploadsDir);
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + '-' + file.originalname);
    }
});

const upload = multer({ 
    storage: storage,
    limits: { fileSize: 10 * 1024 * 1024 } // 10MB limit
});

// TEXT MIME TYPES
app.get('/api/text/plain', (req, res) => {
    res.set('Content-Type', 'text/plain');
    res.send('This is plain text content');
});

app.get('/api/text/html', (req, res) => {
    res.set('Content-Type', 'text/html');
    res.send(`
        <!DOCTYPE html>
        <html>
        <head><title>HTML MIME Demo</title></head>
        <body><h1>This is HTML content</h1><p>Served with text/html MIME type</p></body>
        </html>
    `);
});

app.get('/api/text/css', (req, res) => {
    res.set('Content-Type', 'text/css');
    res.send(`
        body { 
            font-family: Arial, sans-serif; 
            background-color: #f0f0f0; 
            padding: 20px; 
        }
        .demo { 
            color: #333; 
            border: 2px solid #007bff; 
            padding: 10px; 
        }
    `);
});

app.get('/api/text/javascript', (req, res) => {
    res.set('Content-Type', 'text/javascript');
    res.send(`
        function showMimeDemo() {
            console.log('This is JavaScript content served as text/javascript');
            document.body.innerHTML += '<p>JavaScript executed successfully!</p>';
        }
        showMimeDemo();
    `);
});

app.get('/api/text/csv', (req, res) => {
    res.set('Content-Type', 'text/csv');
    res.set('Content-Disposition', 'attachment; filename="demo.csv"');
    res.send('Name,Age,City\nJohn,30,New York\nJane,25,London\nBob,35,Paris');
});

// APPLICATION MIME TYPES
app.get('/api/application/json', (req, res) => {
    res.set('Content-Type', 'application/json');
    res.json({
        message: "This is JSON content",
        timestamp: new Date().toISOString(),
        data: {
            users: ["Alice", "Bob", "Charlie"],
            count: 3,
            active: true
        }
    });
});

app.get('/api/application/xml', (req, res) => {
    res.set('Content-Type', 'application/xml');
    res.send(`
        <?xml version="1.0" encoding="UTF-8"?>
        <message>
            <title>XML MIME Demo</title>
            <content>This is XML content served with application/xml</content>
            <timestamp>${new Date().toISOString()}</timestamp>
        </message>
    `);
});

app.get('/api/application/pdf', (req, res) => {
    // Simple PDF creation
    const pdfContent = `%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT /F1 12 Tf 100 700 Td (Hello PDF World!) Tj ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000010 00000 n 
0000000079 00000 n 
0000000173 00000 n 
0000000301 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
398
%%EOF`;
    
    res.set('Content-Type', 'application/pdf');
    res.set('Content-Disposition', 'attachment; filename="demo.pdf"');
    res.send(pdfContent);
});

app.get('/api/application/zip', (req, res) => {
    // Note: This is a minimal ZIP file structure
    const zipContent = Buffer.from([
        0x50, 0x4B, 0x05, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]);
    
    res.set('Content-Type', 'application/zip');
    res.set('Content-Disposition', 'attachment; filename="demo.zip"');
    res.send(zipContent);
});

app.get('/api/application/octet-stream', (req, res) => {
    const binaryData = Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]);
    res.set('Content-Type', 'application/octet-stream');
    res.set('Content-Disposition', 'attachment; filename="binary.bin"');
    res.send(binaryData);
});

// IMAGE MIME TYPES
app.get('/api/image/jpeg', (req, res) => {
    // Minimal JPEG header
    const jpegData = Buffer.from([
        0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01,
        0x01, 0x01, 0x00, 0x48, 0x00, 0x48, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43
    ]);
    res.set('Content-Type', 'image/jpeg');
    res.send(jpegData);
});

app.get('/api/image/png', (req, res) => {
    // Minimal PNG header
    const pngData = Buffer.from([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D,
        0x49, 0x48, 0x44, 0x52, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01
    ]);
    res.set('Content-Type', 'image/png');
    res.send(pngData);
});

app.get('/api/image/svg+xml', (req, res) => {
    res.set('Content-Type', 'image/svg+xml');
    res.send(`
        <svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
            <text x="50" y="55" font-family="Arial" font-size="14" fill="white" text-anchor="middle">SVG</text>
        </svg>
    `);
});

app.get('/api/image/gif', (req, res) => {
    // Minimal GIF header
    const gifData = Buffer.from([
        0x47, 0x49, 0x46, 0x38, 0x39, 0x61, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00,
        0x00, 0x21, 0xF9, 0x04, 0x01, 0x00, 0x00, 0x00, 0x00, 0x2C, 0x00, 0x00
    ]);
    res.set('Content-Type', 'image/gif');
    res.send(gifData);
});

// VIDEO MIME TYPES
app.get('/api/video/mp4', (req, res) => {
    // Minimal MP4 header
    const mp4Data = Buffer.from([
        0x00, 0x00, 0x00, 0x20, 0x66, 0x74, 0x79, 0x70, 0x69, 0x73, 0x6F, 0x6D,
        0x00, 0x00, 0x02, 0x00, 0x69, 0x73, 0x6F, 0x6D, 0x69, 0x73, 0x6F, 0x32
    ]);
    res.set('Content-Type', 'video/mp4');
    res.send(mp4Data);
});

app.get('/api/video/webm', (req, res) => {
    // Minimal WebM header
    const webmData = Buffer.from([
        0x1A, 0x45, 0xDF, 0xA3, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x22,
        0x42, 0x82, 0x88, 0x6D, 0x61, 0x74, 0x72, 0x6F, 0x73, 0x6B, 0x61, 0x00
    ]);
    res.set('Content-Type', 'video/webm');
    res.send(webmData);
});

// MULTIPART MIME TYPES
app.post('/api/multipart/form-data', upload.single('file'), (req, res) => {
    res.set('Content-Type', 'application/json');
    res.json({
        message: "Multipart form-data received successfully",
        file: req.file ? {
            originalname: req.file.originalname,
            mimetype: req.file.mimetype,
            size: req.file.size,
            filename: req.file.filename
        } : null,
        fields: req.body,
        timestamp: new Date().toISOString()
    });
});

app.post('/api/multipart/multiple', upload.array('files', 5), (req, res) => {
    res.set('Content-Type', 'application/json');
    res.json({
        message: "Multiple files received via multipart",
        files: req.files ? req.files.map(file => ({
            originalname: file.originalname,
            mimetype: file.mimetype,
            size: file.size,
            filename: file.filename
        })) : [],
        fields: req.body,
        timestamp: new Date().toISOString()
    });
});

// MESSAGE MIME TYPES
app.get('/api/message/rfc822', (req, res) => {
    res.set('Content-Type', 'message/rfc822');
    res.send(`
        From: sender@example.com
        To: receiver@example.com
        Subject: MIME Demo Email
        Date: ${new Date().toUTCString()}
        Content-Type: text/plain; charset=UTF-8

        This is a sample email message served with message/rfc822 MIME type.
        It demonstrates the email message format.
    `);
});

app.get('/api/message/http', (req, res) => {
    res.set('Content-Type', 'message/http');
    res.send(`
        HTTP/1.1 200 OK
        Content-Type: text/html
        Date: ${new Date().toUTCString()}
        Server: MIME-Demo/1.0
        
        <html><body><h1>This is an HTTP message</h1></body></html>
    `);
});

// Utility endpoint to list all available endpoints
app.get('/api/endpoints', (req, res) => {
    res.set('Content-Type', 'application/json');
    res.json({
        title: "MIME Types Demo API",
        version: "1.0.0",
        endpoints: {
            text: [
                "GET /api/text/plain",
                "GET /api/text/html", 
                "GET /api/text/css",
                "GET /api/text/javascript",
                "GET /api/text/csv"
            ],
            application: [
                "GET /api/application/json",
                "GET /api/application/xml",
                "GET /api/application/pdf",
                "GET /api/application/zip", 
                "GET /api/application/octet-stream"
            ],
            image: [
                "GET /api/image/jpeg",
                "GET /api/image/png",
                "GET /api/image/svg+xml",
                "GET /api/image/gif"
            ],
            video: [
                "GET /api/video/mp4",
                "GET /api/video/webm"
            ],
            multipart: [
                "POST /api/multipart/form-data",
                "POST /api/multipart/multiple"
            ],
            message: [
                "GET /api/message/rfc822",
                "GET /api/message/http"
            ],
            utility: [
                "GET /api/endpoints"
            ]
        },
        usage: "Use Postman to test these endpoints. For POST endpoints, upload files or send form data."
    });
});

// Serve static files from uploads directory
app.use('/uploads', express.static(uploadsDir));

// Serve frontend
app.use(express.static(path.join(__dirname, 'public')));

// Root route redirects to frontend
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 MIME Types Demo Server running on port ${PORT}`);
    console.log(`📋 Available endpoints: http://localhost:${PORT}/api/endpoints`);
    console.log(`📁 Uploads directory: ${uploadsDir}`);
});

module.exports = app;