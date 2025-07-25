from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile, InMemoryUploadedFile

def validate_file_type_and_size(file, allowed_types=None, max_size=None):
    """
    Validate the file type and size.
    
    :param file: The file to validate.
    :param allowed_types: List of allowed MIME types.
    :param max_size: Maximum allowed file size in bytes.
    :raises ValidationError: If the file type or size is invalid.
    """
    if isinstance(file, InMemoryUploadedFile):
        if allowed_types and file.content_type not in allowed_types:
            raise ValidationError(f"Invalid file type: {file.content_type}. Allowed types are: {', '.join(allowed_types)}.")
        
        if max_size and file.size > max_size:
            raise ValidationError(f"File size exceeds the maximum limit of {max_size} bytes. Current size: {file.size} bytes.")
    return True


