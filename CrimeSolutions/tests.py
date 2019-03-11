from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Activities
from .serializers import ActivitiesSerializer


# Create your tests here.
class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_act(act_name="", location="", loc_lat=0, loc_long=0, time="", description=""):
        if act_name != "" and location != "" and loc_lat != "" and loc_long != ""  and description != "":
            Activities.objects.create(act_name=act_name, location=location, loc_lat=loc_lat, loc_long=loc_long,
                                      time=time, description=description)

    def setUp(self):
        # add test data
        self.create_act("like glue", "sean paul", 76, 78, 0, "dead man")
        self.create_act("simple song", "konshens", 76, 78, 0,"dead man")
        self.create_act("love is wicked", "brick and lace", 76, 78, 0,"dead man")
        self.create_act("jam rock", "damien marley", 76, 78, 0,"dead man")


class GetAllSongsTest(BaseViewTest):

    def test_get_all_songs(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("songs-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Activities.objects.all()
        serialized = ActivitiesSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
