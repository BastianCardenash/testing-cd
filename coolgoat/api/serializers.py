from rest_framework import serializers

from .models import League, Team, Match, Odds, Requests, PastMatch, RequestUserRelation

class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['id', 'name', 'country', 'logo', 'flag', 'season', 'round']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'logo', 'winner']

class OddsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Odds
        fields = ['id_in_match', 'name', 'values', 'match']

class RequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = ['request_id', 'group_id', 'fixture_id', 'league_name', 'round' ,'date', 'result' , 'deposit_token', 'datetime', 'quantity', 'wallet', 'seller', 'validated']

class MatchSerializer(serializers.ModelSerializer):
    league = LeagueSerializer()
    home_team = TeamSerializer()
    away_team = TeamSerializer()
    odds = OddsSerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'referee', 'timezone', 'date', 'timestamp', 
                  'status_long', 'status_short', 'elapsed', 
                  'league', 'home_team', 'away_team', 
                  'goals_home', 'goals_away', 'odds', 'bonds_available']

class PastMatchesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PastMatch
        fields = ['id', 'referee', 'timezone', 'date', 'timestamp', 
                  'status_long', 'status_short', 'elapsed',
                  'goals_home', 'goals_away']

class BatchFixturesCreateSerializer(serializers.Serializer):
    fixtures = serializers.ListField(child=serializers.DictField())

    def validate(self, data):
        # Extract fixtures data from the incoming payload
        fixtures = data.get('fixtures')

        if not fixtures:
            raise serializers.ValidationError("No fixtures provided.")

        validated_fixtures = []

        # Iterate over each fixture and perform validation and transformations
        for fixture in fixtures:
            fixture_data = fixture.get('fixture')
            league_data = fixture.get('league')
            teams_data = fixture.get('teams')
            odds_data = fixture.get('odds', [])
            for odd in odds_data:
                odd['id_in_match'] = odd.pop('id')

            if not fixture_data or not league_data or not teams_data:
                raise serializers.ValidationError("Fixture, league, or team data is missing or incorrectly formatted.")

            # Handle League creation or retrieval
            league, _ = League.objects.get_or_create(id=league_data['id'], defaults=league_data)

            # Handle Team creation or retrieval
            home_team, _ = Team.objects.get_or_create(id=teams_data['home']['id'], defaults=teams_data['home'])
            away_team, _ = Team.objects.get_or_create(id=teams_data['away']['id'], defaults=teams_data['away'])

            # Prepare the match data structure
            match_data = {
                'id': fixture_data.get('id'),
                'referee': fixture_data.get('referee'),
                'timezone': fixture_data.get('timezone'),
                'date': fixture_data.get('date'),
                'timestamp': fixture_data.get('timestamp'),
                'status_long': fixture_data['status'].get('long'),
                'status_short': fixture_data['status'].get('short'),
                'elapsed': fixture_data['status'].get('elapsed'),
                'league': league,
                'home_team': home_team,
                'away_team': away_team,
                'goals_home': fixture.get('goals').get('home'),
                'goals_away': fixture.get('goals').get('away'),
            }

            # Create the match object
            match, create = Match.objects.get_or_create(id=match_data['id'], defaults=match_data)

            # Handle Odds creation
            for odd in odds_data:
                Odds.objects.get_or_create(match=match, **odd)

            validated_fixtures.append(match)

        # Replace the original fixtures data with the fully validated and created matches
        data['fixtures'] = validated_fixtures

        return data

    def create(self, validated_data):
        # Since all objects are already created in the validate method, we just return them
        return validated_data['fixtures']

class BatchPastFixturesCreateSerializer(serializers.Serializer):
    fixtures = serializers.ListField(child=serializers.DictField())

    def validate(self, data):
        # Extract fixtures data from the incoming payload
        past_fixtures = data.get('fixtures')

        if not past_fixtures:
            raise serializers.ValidationError("No fixtures provided.")

        validated_past_matches = []

        # Iterate over each fixture and perform validation and transformations
        for fixture in past_fixtures:
            fixture_data = fixture.get('fixture')

            if not fixture_data:
                raise serializers.ValidationError("Fixture data is missing or incorrectly formatted.")

            # Prepare the past match data structure
            past_match_data = {
                'id': fixture_data.get('id'),
                'referee': fixture_data.get('referee'),
                'timezone': fixture_data.get('timezone'),
                'date': fixture_data.get('date'),
                'timestamp': fixture_data.get('timestamp'),
                'status_long': fixture_data['status'].get('long'),
                'status_short': fixture_data['status'].get('short'),
                'elapsed': fixture_data['status'].get('elapsed'),
                'goals_home': fixture.get('goals').get('home'),
                'goals_away': fixture.get('goals').get('away'),
            }

            # Create the match object
            past_match, create = PastMatch.objects.get_or_create(id=past_match_data['id'], defaults=past_match_data)

            validated_past_matches.append(past_match)

        # Replace the original fixtures data with the fully validated and created matches
        data['fixtures'] = validated_past_matches

        return data

    def create(self, validated_data):
        # Since all objects are already created in the validate method, we just return them
        return validated_data['fixtures']


class RequestUserRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestUserRelation
        fields = ['email','request_id']