"""
Flask S3 Image Manager
A Flask application for managing images in AWS S3
"""
import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from werkzeug.utils import secure_filename
from io import BytesIO
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}

def get_s3_client():
    """Create and return an S3 client"""
    try:
        s3_client = boto3.client('s3', region_name='us-east-1')
        return s3_client
    except NoCredentialsError:
        return None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    """Generate a unique filename to avoid collisions"""
    ext = filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return unique_name

@app.route('/')
def index():
    """Home page - display upload form and list of images"""
    images = []
    error = None
    
    try:
        s3_client = get_s3_client()
        if s3_client:
            bucket_name = app.config['S3_BUCKET_NAME']
            response = s3_client.list_objects_v2(Bucket=bucket_name)
            
            if 'Contents' in response:
                for obj in response['Contents']:
                    # Only show image files
                    key = obj['Key']
                    if any(key.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
                        # Use Flask route to serve images (works with IAM roles)
                        images.append({
                            'key': key,
                            'url': url_for('serve_image', key=key),
                            'size': obj['Size'],
                            'last_modified': obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S'),
                            'size_kb': round(obj['Size'] / 1024, 2)
                        })
        else:
            error = "Failed to connect to AWS S3. Check your credentials."
    except ClientError as e:
        error = f"AWS Error: {str(e)}"
    except Exception as e:
        error = f"Error: {str(e)}"
    
    return render_template('index.html', images=images, error=error)

@app.route('/upload', methods=['POST'])
def upload():
    """Handle file upload to S3"""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if not allowed_file(file.filename):
        flash(f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}', 'error')
        return redirect(url_for('index'))
    
    try:
        s3_client = get_s3_client()
        if not s3_client:
            flash('Failed to connect to S3', 'error')
            return redirect(url_for('index'))
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(original_filename)
        
        # Upload to S3
        bucket_name = app.config['S3_BUCKET_NAME']
        s3_client.upload_fileobj(
            file,
            bucket_name,
            unique_filename,
            ExtraArgs={
                'ContentType': file.content_type,
                'Metadata': {'original_filename': original_filename}
            }
        )
        
        flash(f'Successfully uploaded: {original_filename}', 'success')
    except ClientError as e:
        flash(f'Upload failed: {str(e)}', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete/<path:key>')
def delete(key):
    """Delete an image from S3"""
    try:
        s3_client = get_s3_client()
        if not s3_client:
            flash('Failed to connect to S3', 'error')
            return redirect(url_for('index'))
        
        bucket_name = app.config['S3_BUCKET_NAME']
        s3_client.delete_object(Bucket=bucket_name, Key=key)
        flash(f'Successfully deleted: {key}', 'success')
    except ClientError as e:
        flash(f'Delete failed: {str(e)}', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/image/<path:key>')
def serve_image(key):
    """Serve an image from S3 (for display in browser)"""
    try:
        s3_client = get_s3_client()
        if not s3_client:
            return "S3 connection failed", 500
        
        bucket_name = app.config['S3_BUCKET_NAME']
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        
        file_stream = BytesIO(response['Body'].read())
        content_type = response.get('ContentType', 'image/jpeg')
        
        return send_file(
            file_stream,
            mimetype=content_type
        )
    except Exception as e:
        return f"Error: {str(e)}", 404

@app.route('/download/<path:key>')
def download(key):
    """Download an image from S3"""
    try:
        s3_client = get_s3_client()
        if not s3_client:
            flash('Failed to connect to S3', 'error')
            return redirect(url_for('index'))
        
        bucket_name = app.config['S3_BUCKET_NAME']
        
        # Get the object
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        
        # Create a file-like object
        file_stream = BytesIO(response['Body'].read())
        
        return send_file(
            file_stream,
            as_attachment=True,
            download_name=key,
            mimetype=response['ContentType']
        )
    except ClientError as e:
        flash(f'Download failed: {str(e)}', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/images')
def api_list_images():
    """API endpoint to list all images"""
    try:
        s3_client = get_s3_client()
        if not s3_client:
            return jsonify({'error': 'Failed to connect to S3'}), 500
        
        bucket_name = app.config['S3_BUCKET_NAME']
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        
        images = []
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                if any(key.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
                    images.append({
                        'key': key,
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'].isoformat()
                    })
        
        return jsonify({'images': images, 'count': len(images)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """API endpoint for file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
    
    try:
        s3_client = get_s3_client()
        if not s3_client:
            return jsonify({'error': 'Failed to connect to S3'}), 500
        
        original_filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(original_filename)
        
        bucket_name = app.config['S3_BUCKET_NAME']
        s3_client.upload_fileobj(
            file,
            bucket_name,
            unique_filename,
            ExtraArgs={
                'ContentType': file.content_type,
                'Metadata': {'original_filename': original_filename}
            }
        )
        
        return jsonify({
            'message': 'Upload successful',
            'filename': unique_filename,
            'original_filename': original_filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete/<path:key>', methods=['DELETE'])
def api_delete(key):
    """API endpoint to delete an image"""
    try:
        s3_client = get_s3_client()
        if not s3_client:
            return jsonify({'error': 'Failed to connect to S3'}), 500
        
        bucket_name = app.config['S3_BUCKET_NAME']
        s3_client.delete_object(Bucket=bucket_name, Key=key)
        
        return jsonify({'message': f'Successfully deleted: {key}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'S3 Image Manager'
    })

@app.route('/health/s3')
def health_s3():
    """S3 connectivity health check"""
    try:
        s3_client = get_s3_client()
        if not s3_client:
            return jsonify({'status': 'unhealthy', 'error': 'No credentials'}), 500
        
        bucket_name = app.config['S3_BUCKET_NAME']
        s3_client.head_bucket(Bucket=bucket_name)
        
        return jsonify({
            'status': 'healthy',
            'bucket': bucket_name,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

