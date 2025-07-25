from cloudinary.models import CloudinaryField
from cloudinary.uploader import upload,destroy

from django.db.models import FileField
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError

from cloudinary import CloudinaryResource

class CustomCloudinaryField(CloudinaryField):
    def __init__(self, *args, 
                 upload_func=None,
                 category=None,
                 user_type='student',
                 prefix='',
                 allowed_file_types=None,
                 quality=80, **kwargs):
        self.upload_func = upload_func  # capture upload_func like in FileFields
        self.quality = quality
        self.category = category
        self.user_type = user_type
        self.prefix = prefix
        self.allowed_file_types = allowed_file_types
        super().__init__(*args, **kwargs)

    
    
    def pre_save(self, model_instance, add):
        file = getattr(model_instance, self.attname)

        # If it's already uploaded (e.g. public_id string), skip
        if isinstance(file, str):
            return file
    

        # If it's an uploaded file, upload to Cloudinary
        if isinstance(file, UploadedFile):
            # Validate the file type
            self.validate_the_file_type(file)
            
            # Check if the process os add or update
            if not add:
                # If updating, delete the old file if it exists
                old_file_instance = model_instance.__class__.objects.get(pk=model_instance.pk)
                old_file = getattr(old_file_instance, self.attname)
             
                format =  old_file.format or old_file.url.split('/')[-1]
                resource_type = old_file.resource_type or self.determine_resource_type(format)
                
                destroy_result = destroy(
                    old_file.public_id + "." + format if resource_type == 'raw' else old_file.public_id,
                    resource_type=resource_type,
                )

            function = self.upload_func
            instance = model_instance
            upload_folder = function(
                                     instance=instance,
                                     category=self.category,
                                     user_type=self.user_type,
                                     prefix=self.prefix
                )
                
            result = upload(
                file,
                folder=upload_folder,
                resource_type='auto', # works for image, raw, video
                quality=self.quality,  # set quality if needed
            )
            
            # Construct a CloudinaryResource from the upload result
            cloudinary_resource = CloudinaryResource(
                        public_id=result.get("public_id"),
                        format=result.get("format"),
                        version=result.get("version"),
                        signature=result.get("signature"),
                        metadata=result.get("metadata"),
                        type=result.get("type"),
                        resource_type=result.get("resource_type"),
                    )

            # Store the resource object directly on the instance
            setattr(model_instance, self.attname, cloudinary_resource)

            return cloudinary_resource

        return file
    def validate_the_file_type(self, file):
        """
        Validate the file type against allowed types.
        """
        if self.allowed_file_types and isinstance(file, UploadedFile):
            file_extension = file.name.split('.')[-1].lower()
            
            # Check if the file extension is in the allowed types
            if file_extension not in self.allowed_file_types:
                raise ValidationError(f"Invalid file type: {file_extension}. Allowed types are: {', '.join(self.allowed_file_types)}.")
        return True
    def determine_resource_type(self,filename):
        ext = filename.split('.')[-1].lower().strip()

        image_exts = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'tiff', 'svg'}
        video_exts = {'mp4', 'mov', 'avi', 'mkv', 'flv', 'webm', 'wmv', '3gp', 'mpeg'}
        audio_exts = {'mp3', 'wav', 'ogg', 'aac', 'flac', 'm4a'}

        if ext in image_exts:
            return 'image'
        elif ext in video_exts or ext in audio_exts:
            return 'video'  # Cloudinary uses 'video' for both video and audio
        else:
            return 'raw'
    def remove_file_extension(self, filename):
        """
        Remove the file extension from the filename.
        """
        if '.' in filename:
            return '.'.join(filename.split('.')[:-1])
        return filename
    