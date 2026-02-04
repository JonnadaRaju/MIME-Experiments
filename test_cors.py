#!/usr/bin/env python3
"""
Quick test to verify CORS configuration in main.py
"""
import re

def check_cors_config():
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        # Check for expose_headers in CORS configuration
        cors_pattern = r'app\.add_middlewar.*?CORSMiddleware.*?expose_headers'
        if re.search(cors_pattern, content, re.DOTALL | re.IGNORECASE):
            print("✅ CORS Configuration: expose_headers FOUND")
        else:
            print("❌ CORS Configuration: expose_headers MISSING")
            
        # Check for custom headers in endpoints
        if 'X-Custom-Header' in content:
            print("✅ Custom Headers: X-Custom-Header FOUND")
        else:
            print("❌ Custom Headers: X-Custom-Header MISSING")
            
        # Check for headers-demo endpoint
        if '/api/headers-demo' in content:
            print("✅ Headers Demo Endpoint: FOUND")
        else:
            print("❌ Headers Demo Endpoint: MISSING")
            
        # Check frontend header capture improvements
        with open('static/index.html', 'r') as f:
            html_content = f.read()
            
        if 'response.headers.forEach' in html_content and 'response.headers.entries' in html_content:
            print("✅ Frontend Header Capture: Enhanced methods FOUND")
        else:
            print("❌ Frontend Header Capture: Enhanced methods MISSING")
            
        if 'Headers & CORS Testing' in html_content and '/api/headers-demo' in html_content:
            print("✅ Headers Demo Section: FOUND")
        else:
            print("❌ Headers Demo Section: MISSING")
            
        return True
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_sample_cors_config():
    print("\n📋 Sample CORS Configuration:")
    print("""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],  # ← This is the key fix!
)
""")

def show_sample_endpoint():
    print("\n📋 Sample Endpoint with Custom Headers:")
    print("""
@app.get("/api/headers-demo", response_class=JSONResponse)
async def headers_demo():
    response_data = {"message": "Demo"}
    headers = {
        "X-Custom-Demo": "Header-Exposure-Test",
        "X-Endpoint-Name": "/api/headers-demo",
        "X-Server-Time": datetime.now().isoformat(),
    }
    return JSONResponse(content=response_data, headers=headers)
""")

if __name__ == "__main__":
    print("🔍 Testing CORS and Header Configuration...")
    print("=" * 50)
    
    if check_cors_config():
        print("\n✅ Configuration check completed!")
    else:
        print("\n❌ Configuration check failed!")
    
    show_sample_cors_config()
    show_sample_endpoint()
    
    print("\n🚀 Next Steps:")
    print("1. Install dependencies: pip install fastapi uvicorn python-multipart")
    print("2. Run server: python main.py")
    print("3. Test: curl -I http://localhost:8000/api/headers-demo")
    print("4. Open frontend and test headers functionality")