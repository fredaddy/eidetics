from google.cloud import storage

def test_upload():
    client = storage.Client()
    bucket = client.bucket('accumulated-useful-knowledge')  # Replace with your bucket name
    blob = bucket.blob('testfile.txt')
    try:
        blob.upload_from_string('Hello, World!')
        print("Upload successful: {}".format(blob.public_url))
    except Exception as e:
        print("Upload failed: {}".format(e))

if __name__ == "__main__":
    test_upload()
