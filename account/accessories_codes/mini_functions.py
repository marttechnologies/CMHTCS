def get_file_upload_directory_path(
                        user_type='student',
                        instance=None,
                        category="registration",
                        prefix=""):
        """
        Custom method to define the directory path for the uploaded file for student.
        """
        if category == "registration":
                return prefix + f'student/{instance.fullname}/registration/{instance.info_type}'
        if category == "qualification":
                return prefix + f'staff/{instance.fullname}/qualification/{instance.qualification_type}'
        return prefix + f"{user_type}/{instance.fullname}/{category}"