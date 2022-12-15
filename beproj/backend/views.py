from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from .serializers import PolicySerializer, ElementSerializer, ElementFlagSerializer 
from .algo import *
from .models import *
from django.utils.text import slugify

class PolicyViewSet(ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        policy_data = request.data

        new_policy = Policy.objects.create(name = policy_data['name'], fullText = policy_data['fullText'], link = policy_data['link'], category = policy_data['category'], date=policy_data['date'], slug=slugify(policy_data['name']))
        new_policy.save()

        serializer = PolicySerializer(new_policy)
        sp = spacyClass(new_policy.fullText)
        sp.clean_lemmatize()
        sp.phrase_match()
        i = 0
        for index, phrases in sp.matchedDict.items():
            for phrase in phrases:
                matchedElement = Element.objects.get(pk = index + 1)
                elementFlag = ElementFlag(element = matchedElement, policy = new_policy, associatedText = phrase, fullSentence = sp.sentence[i])
                elementFlag.save()
                i = i + 1
        sp.matchedDict.clear()
        return Response(serializer.data)


class ElementViewSet(ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer

class ElementFlagViewSet(ModelViewSet):
    queryset = ElementFlag.objects.all()
    serializer_class = ElementFlagSerializer
    
        
