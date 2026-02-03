from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Response
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import io
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import magic
from PIL import Image
import zipfile
import csv
from typing import Optional, List
import mimetypes

app = FastAPI(title="MIME Types Demo API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("static/images", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# TEXT MIME TYPES
@app.get("/api/text/plain", response_class=Response)
async def get_plain_text():
    """Serve plain text content"""
    content = "This is plain text content served with text/plain MIME type"
    return Response(content=content, media_type="text/plain")

@app.get("/api/text/html", response_class=HTMLResponse)
async def get_html():
    """Serve HTML content"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HTML MIME Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { border: 2px solid #007bff; padding: 20px; border-radius: 10px; }
            h1 { color: #007bff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>This is HTML content</h1>
            <p>Served with text/html MIME type</p>
            <p>Timestamp: {}</p>
        </div>
    </body>
    </html>
    """.format(datetime.now().isoformat())
    return HTMLResponse(content=html_content)

@app.get("/api/text/css", response_class=Response)
async def get_css():
    """Serve CSS content"""
    css_content = """
    body { 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: 0; 
        padding: 20px; 
        min-height: 100vh;
    }
    .demo-container { 
        background: white; 
        color: #333; 
        border-radius: 15px; 
        padding: 30px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        max-width: 800px;
        margin: 50px auto;
    }
    h1 { 
        color: #4a5568; 
        border-bottom: 3px solid #667eea;
        padding-bottom: 10px;
    }
    """
    return Response(content=css_content, media_type="text/css")

@app.get("/api/text/javascript", response_class=Response)
async def get_javascript():
    """Serve JavaScript content"""
    js_content = f"""
    // MIME Demo JavaScript
    console.log('This is JavaScript content served as text/javascript');
    
    function showMimeDemo() {{
        const demo = document.createElement('div');
        demo.innerHTML = `
            <div style="position: fixed; top: 20px; right: 20px; background: #4CAF50; color: white; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3>✅ JavaScript Executed Successfully!</h3>
                <p>Timestamp: {datetime.now().isoformat()}</p>
                <p>MIME Type: text/javascript</p>
            </div>
        `;
        document.body.appendChild(demo);
        
        setTimeout(() => {{
            demo.remove();
        }}, 5000);
    }}
    
    showMimeDemo();
    """
    return Response(content=js_content, media_type="text/javascript")

@app.get("/api/text/csv", response_class=Response)
async def get_csv():
    """Serve CSV content"""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Name', 'Age', 'City', 'Country', 'Email'])
    writer.writerow(['John Doe', 30, 'New York', 'USA', 'john@example.com'])
    writer.writerow(['Jane Smith', 25, 'London', 'UK', 'jane@example.com'])
    writer.writerow(['Bob Johnson', 35, 'Paris', 'France', 'bob@example.com'])
    writer.writerow(['Alice Brown', 28, 'Tokyo', 'Japan', 'alice@example.com'])
    
    content = output.getvalue()
    output.close()
    
    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=demo.csv"}
    )

# APPLICATION MIME TYPES
@app.get("/api/application/json", response_class=JSONResponse)
async def get_json():
    """Serve JSON content"""
    return {
        "message": "This is JSON content",
        "timestamp": datetime.now().isoformat(),
        "server": "FastAPI MIME Demo",
        "version": "1.0.0",
        "data": {
            "users": [
                {"name": "Alice", "age": 30, "active": True},
                {"name": "Bob", "age": 25, "active": False},
                {"name": "Charlie", "age": 35, "active": True}
            ],
            "statistics": {
                "total_users": 3,
                "active_users": 2,
                "completion_rate": 66.67
            }
        },
        "mime_type": "application/json"
    }

@app.get("/api/application/xml", response_class=Response)
async def get_xml():
    """Serve XML content"""
    root = ET.Element("message")
    title = ET.SubElement(root, "title")
    title.text = "XML MIME Demo"
    content = ET.SubElement(root, "content")
    content.text = "This is XML content served with application/xml"
    
    # Add metadata
    metadata = ET.SubElement(root, "metadata")
    timestamp = ET.SubElement(metadata, "timestamp")
    timestamp.text = datetime.now().isoformat()
    server = ET.SubElement(metadata, "server")
    server.text = "FastAPI"
    
    xml_str = ET.tostring(root, encoding='unicode', xml_declaration=True)
    return Response(content=xml_str, media_type="application/xml")

@app.get("/api/application/pdf", response_class=Response)
async def get_pdf():
    """Serve a simple PDF"""
    # Create a simple text-based PDF
    pdf_content = b"""%PDF-1.4
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
/Resources <<
/Font <<
/F1 5 0 R
>>
>>
>>
endobj
4 0 obj
<<
/Length 107
>>
stream
BT
/F1 16 Tf
72 720 Td
(FastAPI PDF Demo) Tj
0 -20 Td
(This is a PDF file served with application/pdf MIME type.) Tj
0 -20 Td
(Timestamp: """ + datetime.now().isoformat().encode() + b""") Tj
ET
endstream
endobj
5 0 obj
<<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000274 00000 n 
0000000465 00000 n 
trailer
<<
/Size 6
/Root 1 0 R
>>
startxref
534
%%EOF"""
    
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=demo.pdf"}
    )

@app.get("/api/application/zip", response_class=Response)
async def get_zip():
    """Serve a ZIP file"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add a text file
        zip_file.writestr('demo.txt', f'This is a text file inside ZIP\nCreated: {datetime.now().isoformat()}')
        
        # Add a JSON file
        json_data = {
            "message": "JSON file inside ZIP",
            "created": datetime.now().isoformat(),
            "mime_type": "application/zip"
        }
        zip_file.writestr('data.json', json.dumps(json_data, indent=2))
        
        # Add a simple HTML file
        html_content = '<html><body><h1>HTML file in ZIP</h1><p>Created with FastAPI</p></body></html>'
        zip_file.writestr('page.html', html_content)
    
    zip_buffer.seek(0)
    
    return StreamingResponse(
        io.BytesIO(zip_buffer.read()),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=demo.zip"}
    )

@app.get("/api/application/octet-stream", response_class=Response)
async def get_octet_stream():
    """Serve binary data"""
    # Create some binary data (PNG header + some data)
    binary_data = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
    binary_data += b'FastAPI Binary Data' + datetime.now().isoformat().encode()
    
    return Response(
        content=binary_data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=binary.bin"}
    )

# IMAGE MIME TYPES
@app.get("/api/image/jpeg", response_class=Response)
async def get_jpeg():
    """Generate and serve a JPEG image"""
    # Create a simple image with PIL
    img = Image.new('RGB', (400, 300), color='#FF6B6B')
    
    # Add some text
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)
    
    # Add title
    draw.text((50, 50), "JPEG Image", fill='white')
    draw.text((50, 80), "MIME Type: image/jpeg", fill='white')
    draw.text((50, 110), f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fill='white')
    
    # Convert to JPEG
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='JPEG', quality=95)
    img_buffer.seek(0)
    
    return StreamingResponse(
        io.BytesIO(img_buffer.read()),
        media_type="image/jpeg",
        headers={"Content-Disposition": "attachment; filename=demo.jpg"}
    )

@app.get("/api/image/png", response_class=Response)
async def get_png():
    """Generate and serve a PNG image"""
    # Create a gradient PNG image
    img = Image.new('RGB', (400, 300), color='#4ECDC4')
    
    # Add text
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    
    # Add title and info
    draw.text((50, 50), "PNG Image", fill='white')
    draw.text((50, 80), "MIME Type: image/png", fill='white')
    draw.text((50, 110), f"FastAPI Demo", fill='white')
    draw.text((50, 140), f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fill='white')
    
    # Convert to PNG
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return StreamingResponse(
        io.BytesIO(img_buffer.read()),
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=demo.png"}
    )

@app.get("/api/image/svg+xml", response_class=Response)
async def get_svg():
    """Serve SVG content"""
    svg_content = f"""
    <svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#FF6B6B;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#4ECDC4;stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect width="400" height="300" fill="url(#grad1)" />
        <text x="200" y="80" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="white" text-anchor="middle">
            SVG Image
        </text>
        <text x="200" y="120" font-family="Arial, sans-serif" font-size="16" fill="white" text-anchor="middle">
            MIME Type: image/svg+xml
        </text>
        <text x="200" y="150" font-family="Arial, sans-serif" font-size="14" fill="white" text-anchor="middle">
            FastAPI Demo
        </text>
        <text x="200" y="180" font-family="Arial, sans-serif" font-size="12" fill="white" text-anchor="middle">
            {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </text>
        <circle cx="100" cy="220" r="20" fill="white" opacity="0.8"/>
        <circle cx="200" cy="220" r="20" fill="white" opacity="0.8"/>
        <circle cx="300" cy="220" r="20" fill="white" opacity="0.8"/>
    </svg>
    """
    return Response(content=svg_content, media_type="image/svg+xml")

@app.get("/api/image/gif", response_class=Response)
async def get_gif():
    """Generate and serve a GIF image"""
    # Create a simple animated GIF
    frames = []
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    for i, color in enumerate(colors):
        img = Image.new('RGB', (200, 200), color=color)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.text((50, 80), f"Frame {i+1}", fill='white')
        draw.text((50, 110), "GIF Demo", fill='white')
        frames.append(img)
    
    # Save as GIF
    gif_buffer = io.BytesIO()
    frames[0].save(
        gif_buffer, 
        format='GIF', 
        save_all=True, 
        append_images=frames[1:], 
        duration=500, 
        loop=0
    )
    gif_buffer.seek(0)
    
    return StreamingResponse(
        io.BytesIO(gif_buffer.read()),
        media_type="image/gif",
        headers={"Content-Disposition": "attachment; filename=demo.gif"}
    )

# VIDEO MIME TYPES
@app.get("/api/video/mp4", response_class=Response)
async def get_mp4():
    """Serve MP4 video placeholder"""
    # This would normally contain actual video data
    # For demo purposes, we'll return a placeholder
    mp4_header = bytes([0x00, 0x00, 0x00, 0x20, 0x66, 0x74, 0x79, 0x70, 
                       0x69, 0x73, 0x6F, 0x6D, 0x00, 0x00, 0x02, 0x00])
    
    return Response(
        content=mp4_header + b"MP4 placeholder - FastAPI Demo",
        media_type="video/mp4",
        headers={"Content-Disposition": "attachment; filename=demo.mp4"}
    )

@app.get("/api/video/webm", response_class=Response)
async def get_webm():
    """Serve WebM video placeholder"""
    webm_header = bytes([0x1A, 0x45, 0xDF, 0xA3, 0x00, 0x00, 0x00, 0x00])
    
    return Response(
        content=webm_header + b"WebM placeholder - FastAPI Demo",
        media_type="video/webm",
        headers={"Content-Disposition": "attachment; filename=demo.webm"}
    )

# FILE UPLOAD ENDPOINTS
@app.post("/api/upload/single", response_class=JSONResponse)
async def upload_single_file(file: UploadFile = File(...)):
    """Upload a single file and return MIME type information"""
    try:
        # Read file content
        content = await file.read()
        
        # Detect MIME type
        mime_type = magic.from_buffer(content, mime=True)
        
        # Save file
        file_path = f"uploads/{datetime.now().timestamp()}_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(content)
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "mime_type": mime_type,
            "file_size": len(content),
            "saved_path": file_path,
            "timestamp": datetime.now().isoformat(),
            "headers": dict(file.headers)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Upload failed: {str(e)}")

@app.post("/api/upload/multiple", response_class=JSONResponse)
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """Upload multiple files and return MIME type information"""
    results = []
    
    for file in files:
        try:
            content = await file.read()
            mime_type = magic.from_buffer(content, mime=True)
            
            file_path = f"uploads/{datetime.now().timestamp()}_{file.filename}"
            with open(file_path, "wb") as f:
                f.write(content)
            
            results.append({
                "filename": file.filename,
                "mime_type": mime_type,
                "file_size": len(content),
                "saved_path": file_path
            })
            
            # Reset file position for next operation
            await file.seek(0)
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {
        "message": f"Processed {len(files)} files",
        "successful_uploads": len([r for r in results if "error" not in r]),
        "failed_uploads": len([r for r in results if "error" in r]),
        "results": results,
        "timestamp": datetime.now().isoformat()
    }

# UTILITY ENDPOINTS
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main demo page"""
    return FileResponse("static/index.html")

@app.get("/api/endpoints", response_class=JSONResponse)
async def get_endpoints():
    """Get all available endpoints"""
    return {
        "title": "FastAPI MIME Types Demo",
        "version": "1.0.0",
        "server": "FastAPI",
        "endpoints": {
            "text": [
                {"method": "GET", "path": "/api/text/plain", "description": "Plain text content"},
                {"method": "GET", "path": "/api/text/html", "description": "HTML content"},
                {"method": "GET", "path": "/api/text/css", "description": "CSS stylesheet"},
                {"method": "GET", "path": "/api/text/javascript", "description": "JavaScript code"},
                {"method": "GET", "path": "/api/text/csv", "description": "CSV data download"}
            ],
            "application": [
                {"method": "GET", "path": "/api/application/json", "description": "JSON data"},
                {"method": "GET", "path": "/api/application/xml", "description": "XML data"},
                {"method": "GET", "path": "/api/application/pdf", "description": "PDF document download"},
                {"method": "GET", "path": "/api/application/zip", "description": "ZIP archive download"},
                {"method": "GET", "path": "/api/application/octet-stream", "description": "Binary data download"}
            ],
            "image": [
                {"method": "GET", "path": "/api/image/jpeg", "description": "JPEG image download"},
                {"method": "GET", "path": "/api/image/png", "description": "PNG image download"},
                {"method": "GET", "path": "/api/image/svg+xml", "description": "SVG vector image"},
                {"method": "GET", "path": "/api/image/gif", "description": "Animated GIF download"}
            ],
            "video": [
                {"method": "GET", "path": "/api/video/mp4", "description": "MP4 video placeholder"},
                {"method": "GET", "path": "/api/video/webm", "description": "WebM video placeholder"}
            ],
            "upload": [
                {"method": "POST", "path": "/api/upload/single", "description": "Upload single file"},
                {"method": "POST", "path": "/api/upload/multiple", "description": "Upload multiple files"}
            ],
            "utility": [
                {"method": "GET", "path": "/", "description": "Main demo page"},
                {"method": "GET", "path": "/api/endpoints", "description": "List all endpoints"}
            ]
        },
        "usage": {
            "browser": "Open any GET endpoint directly in your browser",
            "postman": "Use Postman collection to test all endpoints including file uploads",
            "curl": "Use curl commands for command-line testing"
        },
        "features": [
            "Automatic MIME type detection",
            "File upload with type validation",
            "Dynamic image generation",
            "Archive creation",
            "CSV export",
            "Interactive documentation at /docs"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)