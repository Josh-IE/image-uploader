import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from imageuploader.imageuploader import exceptions

from .serializers import ImageUploadSerializer
from .. import utils


class ImageUpload(views.APIView):
    """
    Process url and return url on storage.
    """

    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        Return uploaded image path
        """
        serializer = ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        error = None

        try:
            uploaded_image_url = utils.upload(serializer.data["image_url"])
        except (
            exceptions.ImagePropertySizeError,
            exceptions.InvalidImageError,
        ) as e:
            error = e.message
            error_code = status.HTTP_400_BAD_REQUEST
        except requests.RequestException as e:
            error = str(e)
            error_code = status.HTTP_424_FAILED_DEPENDENCY
        # except Exception as e:
        #     error = "sorry, service is temporarily unavailable."
        #     error_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if error:
            return Response({"message": error}, error_code)

        response_data = {"image_url": uploaded_image_url}

        return Response(response_data)
