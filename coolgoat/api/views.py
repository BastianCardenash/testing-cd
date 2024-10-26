from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Match, Requests, Odds, PastMatch, RequestUserRelation
# from coolgoat.users.models import CoolgoatUser
from .paginations import FixturesPageNumberPagination
from .serializers import MatchSerializer, BatchFixturesCreateSerializer, RequestsSerializer, OddsSerializer, PastMatchesSerializer, BatchPastFixturesCreateSerializer, RequestUserRelationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
""" test """
import os
import json
import paho.mqtt.client as mqtt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import jwt
from jwt import PyJWKClient
from .jwtdecoder import validate_jwt_token

class ProtectedView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtén el token del encabezado Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({"error": "No se proporcionó el token de autorización."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Remueve el prefijo 'Bearer' del token
            token = auth_header.split(' ')[1]
            decoded_token = validate_jwt_token(token)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # Si el token es válido, continúa con la lógica de tu vista
        return Response({"message": "Token válido", "decoded": decoded_token})

# 1. List All Matches
class MatchListView(generics.ListAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    pagination_class = FixturesPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        """
        Apply filtering for home team, away team, and match date, 
        while maintaining the existing pagination.
        """
        queryset = super().get_queryset()  # Use the base queryset
        home_team = self.request.query_params.get('home')
        away_team = self.request.query_params.get('visit')
        match_date = self.request.query_params.get('date')

        if home_team:
            queryset = queryset.filter(home_team__name__icontains=home_team)
        if away_team:
            queryset = queryset.filter(away_team__name__icontains=away_team)
        if match_date:
            queryset = queryset.filter(date__date=match_date)

        # Filter out past matches
        queryset = queryset.filter(status_short__in=["NS", "1H", "2H", "HT", "ET", "P"])

        return queryset

# 2. Get Match Details
class MatchDetailView(generics.RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    renderer_classes = [JSONRenderer]

# 3. Create One Match 
class MatchCreateView(APIView):
    def post(self, request):
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            match = serializer.save()
            return Response({'status': 'success', 
                             'match_id': match.id}, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 4. Create Batch of Matches
class BatchFixturesCreateView(APIView):
    def post(self, request):
        serializer = BatchFixturesCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Matches created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Metimos la logica dentro de la validacion de la request juju
# class PlaceBondView(generics.UpdateAPIView):
#     queryset = Match.objects.all()
#     permission_classes = [IsAuthenticated]
#     renderer_classes = [JSONRenderer]

#     def post(self, request, match_id):
#         try:
#             match = self.get_object()
#         except Match.DoesNotExist:
#             raise ValidationError("Match not found")

#         if match.bonds_available > 0:
#             match.bonds_available -= 1
#             match.save()
#             return Response({"message": "Bond placed successfully", "bonds_remaining": match.bonds_available})
#         else:
#             return Response({"message": "No bonds available for this match"}, status=400)

# 6. List Odds by Match
class OddsByMatchView(generics.ListAPIView):
    serializer_class = OddsSerializer

    def get_queryset(self):
        match_id = self.kwargs['match_id']  # Obtener el ID del partido desde la URL
        return Odds.objects.filter(match__id=match_id)  # Filtrar las odds del partido

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'fixture': self.kwargs['match_id'],  # Incluir el ID del partido en la respuesta
            'odds': serializer.data
        })
        
# 7. MQTT Requests
MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = int(os.getenv('MQTT_PORT'))
MQTT_TOPIC_REQUESTS = 'fixtures/requests'
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')

def publish_bet_request(bet_request_data):
    client = mqtt.Client()
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC_REQUESTS, json.dumps(bet_request_data))
    client.loop_start()
    client.loop_stop()

# 8. Publish Bet Request From User
class PublishBetRequestView(APIView):
    def post(self, request):
        bet_request_data = request.data
        bonds_placed = int(bet_request_data['quantity'])
        serializer = RequestsSerializer(data=request.data)
        # pasarlo como url param??
        # match = Match.objects.get(id=match_id)
        try:
            match = Match.objects.get(id=bet_request_data['fixture_id'])
        except Match.DoesNotExist:
            return Response({"error": "Match not found"}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            if bonds_placed > match.bonds_available:
                print("NO!!")
                return Response({'status': 'error', 'message': 'Not enough bonds available'}, status=status.HTTP_400_BAD_REQUEST)
            request = serializer.save()
            publish_bet_request(bet_request_data)
            match.bonds_available -= bonds_placed
            match.save()
            return Response({'status': 'success', 
                             'request_id': request.request_id}, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 9. Create Request From Another Group
class RequestCreateView(APIView):
    def post(self, request):
        if request.data.get('group_id') != "25":
            serializer = RequestsSerializer(data=request.data)
            if serializer.is_valid():
                request = serializer.save()
                return Response({'status': 'success', 
                                 'request_id': request.request_id}, 
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'error', 'message': 'Group ID not allowed'}, status=status.HTTP_403_FORBIDDEN)
    # Si queremos cambiar el orden del fujo, hay que llamar a la funcion de mqtt para que se envie el mensaje.
    # publish_bet_request(request.data)
    

# 10. Patch Request After Validation
class RequestPatchView(APIView):
    def patch(self, request, request_id):
        try:
            print(request.data)
            # print(Requests.objects)
            betRequest = Requests.objects.get(request_id=request_id)
            matchRequest = Match.objects.get(id=betRequest.fixture_id)
        except Requests.DoesNotExist:
            return Response({"error": "Request not found"}, status=status.HTTP_404_NOT_FOUND)

        valid = request.data.get('valid')
        if valid is None:
            return Response({"error": "Validation status must be provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Chequeamos primero si nosotros hicimos el bet
        if betRequest.group_id == "25":
            # Si es así, y la validación falla, devolvemos los bonds reservados. Sino, se dejan como están.
            if not valid:
                matchRequest.bonds_available += betRequest.quantity; 
                matchRequest.save()
        else:
            #Si es otro grupo y es válido, restamos los bonds disponibles.
            if valid:
                matchRequest.bonds_available -= betRequest.quantity; 
                matchRequest.save()
        
        betRequest.validated = valid
        betRequest.save()

        return Response({"message": "Request updated successfully."}, status=status.HTTP_200_OK)

# 11. Patch Match
class MatchPatchView(APIView):
    def patch(self, request, match_id):
        try:
            match = Match.objects.get(id=match_id)
        except Match.DoesNotExist:
            return Response({"error": "Match not found"}, status=status.HTTP_404_NOT_FOUND)

        # deberiamos hacer un manejo de error de cuando no hay mas bonds disponibles aca?
        if match.bonds_available > 0:
            match.bonds_available -= 1
            match.save()
            return Response({"message": "Bond placed successfully", "bonds_remaining": match.bonds_available})
        # Update the match's status_short field
        else:
            return Response({"message": "No bonds available for this match"}, status=400)

# 12. Create Past Match
class PastMatchCreateView(APIView):
    def post(self, request):
        serializer = PastMatchesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Match history created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 13. Create Batch of Past Matches
class BatchPastFixturesCreateView(APIView):
    def post(self, request):
        serializer = BatchPastFixturesCreateSerializer(data=request.data)
        if serializer.is_valid():
    
            requests = Requests.objects.all()
            for new_past_match in serializer.validated_data['fixtures']:
                new_past_match_id = new_past_match.id
                new_past_match_result = GetResultOfPastMatch(new_past_match)
                requests_of_new_past_match = requests.filter(fixture_id=new_past_match_id)
                for request in requests_of_new_past_match:
                    if request.result == new_past_match_result:
                        user_email = RequestUserRelation.objects.get(request_id=request.request_id)
                        # user = CoolgoatUser.objects.get(email=user_email)
                        # user.funds += request.quantity*1000
            serializer.save()
            return Response({'status': 'success', 'message': 'Past Matches created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def GetResultOfPastMatch(new_past_match):
    match = Match.objects.get(id=new_past_match.id)
    home_team = match.home_team.name
    away_team = match.away_team.name
    goals_home = new_past_match.goals_home
    goals_away = new_past_match.goals_away
    if goals_home > goals_away:
        return home_team
    elif goals_home < goals_away:
        return away_team
    else:
        return "draw"
    
# # DE TEST
# class PastMatchDeleteView(APIView):
#     def delete(self, request, match_id):
#         past_match = PastMatch.objects.get(id=match_id)
#         past_match.delete()
#         return Response({'status': 'success', 'message': 'Past Match deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# 14. Get List Past Matches
class PastMatchListView(generics.ListAPIView):
    queryset = PastMatch.objects.all()
    serializer_class = PastMatchesSerializer

# 15. Creates User - Requests Relation
class RequestUserRelationCreateView(APIView):
    def post(self, request):
        print(request.data)
        serializer = RequestUserRelationSerializer(data=request.data)
        if serializer.is_valid():
            request = serializer.save()
            return Response({'status': 'success', 'request_id': request.request_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 16. Get List User Requests
class UserRequestsList(generics.ListAPIView):
    def get_queryset(self):
        user_email = self.kwargs['user_email']
        userRequestsRelations = RequestUserRelation.objects.filter(email=user_email)
        requests_ids = userRequestsRelations.values_list('request_id', flat=True)
        return Requests.objects.filter(request_id__in=requests_ids)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = RequestsSerializer(queryset, many=True)
        return Response(serializer.data)
    


