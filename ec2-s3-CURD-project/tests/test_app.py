"""
Unit tests for the Flask S3 Image Manager application
"""
import pytest
import json
import os
from io import BytesIO
from unittest.mock import patch, MagicMock
import boto3
from moto import mock_aws

# Set test environment variables before importing app
os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
os.environ['AWS_REGION'] = 'us-east-1'
os.environ['S3_BUCKET_NAME'] = 'test-bucket'
os.environ['SECRET_KEY'] = 'test-secret-key'

from app import app, allowed_file, generate_unique_filename, ALLOWED_EXTENSIONS


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_s3():
    """Create a mock S3 bucket for testing"""
    with mock_aws():
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        yield s3


class TestAllowedFile:
    """Tests for the allowed_file function"""
    
    def test_allowed_extensions(self):
        """Test that allowed extensions return True"""
        for ext in ALLOWED_EXTENSIONS:
            assert allowed_file(f'test.{ext}') is True
            assert allowed_file(f'test.{ext.upper()}') is True
    
    def test_disallowed_extensions(self):
        """Test that disallowed extensions return False"""
        disallowed = ['txt', 'pdf', 'exe', 'js', 'py', 'html']
        for ext in disallowed:
            assert allowed_file(f'test.{ext}') is False
    
    def test_no_extension(self):
        """Test that files without extension return False"""
        assert allowed_file('testfile') is False
    
    def test_empty_filename(self):
        """Test that empty filename returns False"""
        assert allowed_file('') is False


class TestGenerateUniqueFilename:
    """Tests for the generate_unique_filename function"""
    
    def test_generates_unique_names(self):
        """Test that function generates unique filenames"""
        name1 = generate_unique_filename('test.jpg')
        name2 = generate_unique_filename('test.jpg')
        assert name1 != name2
    
    def test_preserves_extension(self):
        """Test that original extension is preserved"""
        result = generate_unique_filename('photo.png')
        assert result.endswith('.png')
        
        result = generate_unique_filename('image.JPEG')
        assert result.endswith('.jpeg')
    
    def test_contains_timestamp(self):
        """Test that filename contains timestamp pattern"""
        result = generate_unique_filename('test.jpg')
        # Should contain underscore separating uuid and timestamp
        assert '_' in result


class TestHealthEndpoints:
    """Tests for health check endpoints"""
    
    def test_health_endpoint(self, client):
        """Test the /health endpoint returns healthy status"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'S3 Image Manager'
        assert 'timestamp' in data
    
    @mock_aws
    def test_health_s3_endpoint_healthy(self, client):
        """Test the /health/s3 endpoint when S3 is accessible"""
        # Create mock bucket
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        
        response = client.get('/health/s3')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'


class TestIndexRoute:
    """Tests for the index route"""
    
    def test_index_returns_200(self, client):
        """Test that index page returns 200"""
        with patch('app.get_s3_client') as mock_client:
            mock_s3 = MagicMock()
            mock_s3.list_objects_v2.return_value = {'Contents': []}
            mock_client.return_value = mock_s3
            
            response = client.get('/')
            assert response.status_code == 200
    
    def test_index_contains_upload_form(self, client):
        """Test that index page contains upload form"""
        with patch('app.get_s3_client') as mock_client:
            mock_s3 = MagicMock()
            mock_s3.list_objects_v2.return_value = {}
            mock_client.return_value = mock_s3
            
            response = client.get('/')
            assert b'Upload Image' in response.data
            assert b'enctype="multipart/form-data"' in response.data


class TestUploadRoute:
    """Tests for the upload route"""
    
    def test_upload_no_file(self, client):
        """Test upload with no file selected"""
        response = client.post('/upload', data={}, follow_redirects=True)
        assert response.status_code == 200
        assert b'No file selected' in response.data
    
    def test_upload_empty_filename(self, client):
        """Test upload with empty filename"""
        data = {'file': (BytesIO(b''), '')}
        response = client.post('/upload', data=data, follow_redirects=True)
        assert response.status_code == 200
    
    def test_upload_invalid_file_type(self, client):
        """Test upload with invalid file type"""
        data = {'file': (BytesIO(b'test content'), 'test.txt')}
        response = client.post('/upload', data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Invalid file type' in response.data
    
    @mock_aws
    def test_upload_valid_file(self, client):
        """Test successful file upload"""
        # Create mock bucket
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        
        # Create a small test image (1x1 pixel PNG)
        png_data = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
            b'\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00'
            b'\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00'
            b'\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        
        data = {
            'file': (BytesIO(png_data), 'test.png', 'image/png')
        }
        response = client.post('/upload', data=data, 
                               content_type='multipart/form-data',
                               follow_redirects=True)
        assert response.status_code == 200


class TestAPIEndpoints:
    """Tests for API endpoints"""
    
    @mock_aws
    def test_api_images_empty(self, client):
        """Test API images endpoint with empty bucket"""
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        
        response = client.get('/api/images')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 0
        assert data['images'] == []
    
    @mock_aws
    def test_api_images_with_files(self, client):
        """Test API images endpoint with files in bucket"""
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        
        # Upload a test file
        s3.put_object(Bucket='test-bucket', Key='test.jpg', Body=b'test')
        
        response = client.get('/api/images')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 1
        assert data['images'][0]['key'] == 'test.jpg'
    
    def test_api_upload_no_file(self, client):
        """Test API upload with no file"""
        response = client.post('/api/upload', data={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_api_upload_invalid_type(self, client):
        """Test API upload with invalid file type"""
        data = {'file': (BytesIO(b'test'), 'test.txt')}
        response = client.post('/api/upload', data=data,
                               content_type='multipart/form-data')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Invalid file type' in data['error']


class TestDeleteRoute:
    """Tests for delete functionality"""
    
    @mock_aws
    def test_delete_file(self, client):
        """Test deleting a file from S3"""
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        s3.put_object(Bucket='test-bucket', Key='test.jpg', Body=b'test')
        
        response = client.get('/delete/test.jpg', follow_redirects=True)
        assert response.status_code == 200
        
        # Verify file is deleted
        objects = s3.list_objects_v2(Bucket='test-bucket')
        assert 'Contents' not in objects or len(objects['Contents']) == 0
    
    @mock_aws
    def test_api_delete_file(self, client):
        """Test API delete endpoint"""
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        s3.put_object(Bucket='test-bucket', Key='test.jpg', Body=b'test')
        
        response = client.delete('/api/delete/test.jpg')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'Successfully deleted' in data['message']


class TestDownloadRoute:
    """Tests for download functionality"""
    
    @mock_aws
    def test_download_file(self, client):
        """Test downloading a file from S3"""
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        s3.put_object(
            Bucket='test-bucket', 
            Key='test.jpg', 
            Body=b'test image content',
            ContentType='image/jpeg'
        )
        
        response = client.get('/download/test.jpg')
        assert response.status_code == 200
        assert response.data == b'test image content'


if __name__ == '__main__':
    pytest.main(['-v', '--cov=app', '--cov-report=html'])

