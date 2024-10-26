from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class BatchFixturesCreateViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('fixtures-create-batch')
        self.sample_data = {
            "fixtures": [
                {
                    "fixture": {
                        "id": 1208043,
                        "referee": "J. Gillett",
                        "timezone": "UTC",
                        "date": "2024-09-01T12:30:00+00:00",
                        "timestamp": 1725193800,
                        "status": {"long": "Not Started", "short": "NS", "elapsed": None}
                    },
                    "league": {
                        "id": 39,
                        "name": "Premier League",
                        "country": "England",
                        "logo": "https://media.api-sports.io/football/leagues/39.png",
                        "flag": "https://media.api-sports.io/flags/gb.svg",
                        "season": 2024,
                        "round": "Regular Season - 3"
                    },
                    "teams": {
                        "home": {"id": 49, "name": "Chelsea", 
                                 "logo": "https://media.api-sports.io/football/teams/49.png", "winner": None},
                        "away": {"id": 52, "name": "Crystal Palace", 
                                 "logo": "https://media.api-sports.io/football/teams/52.png", "winner": None}
                    },
                    "goals": {"home": None, "away": None},
                    "odds": [
                        {"id": 1, "name": "Match Winner", "values": [
                            {"value": "Home", "odd": "1.62"},
                            {"value": "Draw", "odd": "4.55"},
                            {"value": "Away", "odd": "5.10"}
                        ]}
                    ]
                },
                {
                    "fixture": {
                        "id": 1208041,
                        "referee": "Chris Kavanagh, England",
                        "timezone": "UTC",
                        "date": "2024-08-31T11:30:00+00:00",
                        "timestamp": 1725103800,
                        "status": {"long": "First Half", "short": "1H", "elapsed": 36}
                    },
                    "league": {
                        "id": 39,
                        "name": "Premier League",
                        "country": "England",
                        "logo": "https://media.api-sports.io/football/leagues/39.png",
                        "flag": "https://media.api-sports.io/flags/gb.svg",
                        "season": 2024,
                        "round": "Regular Season - 3"
                    },
                    "teams": {
                        "home": {"id": 42, "name": "Arsenal", 
                                 "logo": "https://media.api-sports.io/football/teams/42.png", "winner": None},
                        "away": {"id": 51, "name": "Brighton", 
                                 "logo": "https://media.api-sports.io/football/teams/51.png", "winner": None}
                    },
                    "goals": {"home": 0, "away": 0},
                    "odds": [
                        {"id": 1, "name": "Match Winner", "values": [
                            {"value": "Home", "odd": "1.39"},
                            {"value": "Draw", "odd": "5.60"},
                            {"value": "Away", "odd": "7.60"}
                        ]}
                    ]
                }
            ]
        }

    def test_batch_fixtures_create(self):
        response = self.client.post(self.url, self.sample_data, format='json')
        print(response.content)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
