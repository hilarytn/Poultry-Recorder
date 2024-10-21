# media.py
import cloudinary
import cloudinary.uploader
import cloudinary.api

# # Upload media file to Cloudinary
# def upload_media(file, folder="media"):
#     if file:
#         upload_result = cloudinary.uploader.upload(file, folder=folder)
#         return upload_result.get('url')
#     return None

def upload_media(file, folder):
    if file:
        # Check if the file is an image or a video
        if file.content_type.startswith('image/'):
            upload_result = cloudinary.uploader.upload(file, folder=folder, resource_type='image')
        elif file.content_type.startswith('video/'):
            upload_result = cloudinary.uploader.upload(file, folder=folder, resource_type='video')
        else:
            raise ValueError("Unsupported file type.")
        
        return upload_result.get('secure_url')  # Return the URL of the uploaded file
    return None

# def upload_media(files, folder):
#     if files:
#         # Create a list to hold the URLs of uploaded files
#         uploaded_urls = []
        
#         # Check if the input is a single file or a list of files
#         if isinstance(files, list):
#             for file in files:
#                 if file.content_type.startswith('image/'):
#                     upload_result = cloudinary.uploader.upload(file, folder=folder, resource_type='image')
#                     uploaded_urls.append(upload_result.get('secure_url'))
#                 elif file.content_type.startswith('video/'):
#                     upload_result = cloudinary.uploader.upload(file, folder=folder, resource_type='video')
#                     uploaded_urls.append(upload_result.get('secure_url'))
#                 else:
#                     raise ValueError("Unsupported file type.")
#         else:
#             # Handle single file upload
#             if files.content_type.startswith('image/'):
#                 upload_result = cloudinary.uploader.upload(files, folder=folder, resource_type='image')
#                 uploaded_urls.append(upload_result.get('secure_url'))
#             elif files.content_type.startswith('video/'):
#                 upload_result = cloudinary.uploader.upload(files, folder=folder, resource_type='video')
#                 uploaded_urls.append(upload_result.get('secure_url'))
#             else:
#                 raise ValueError("Unsupported file type.")
        
#         return uploaded_urls  # Return the list of URLs of the uploaded files
#     return None
