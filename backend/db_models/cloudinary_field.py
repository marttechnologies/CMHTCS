from cloudinary.models import CloudinaryField
from cloudinary.uploader import upload
from django.db.models import FileField
from django.core.files.uploadedfile import UploadedFile


class CustomCloudinaryField(CloudinaryField):
    def __init__(self, *args, upload_to=None,quality=80, **kwargs):
        self.upload_to = upload_to  # capture upload_to like in FileFields
        self.quality = quality
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        file = getattr(model_instance, self.attname)

        # If it's already uploaded (e.g. public_id string), skip
        if isinstance(file, str):
            return file

        # If it's an uploaded file, upload to Cloudinary
        if isinstance(file, UploadedFile):
            upload_folder = self.upload_to or ''
            result = upload(
                file,
                folder=upload_folder,
                resource_type='auto', # works for image, raw, video
                quality=self.quality,  # set quality if needed
            )

            # Save the public_id or secure_url
            public_id = result.get('public_id')
            setattr(model_instance, self.attname, public_id)
            return public_id

        return file
