from pyexpat.errors import messages
from django.conf import settings
from openai import OpenAI
from dotenv import load_dotenv
from rest_framework import serializers
from chatbox.models import ChatMessage
import os


load_dotenv()
api_key=os.getenv('OPEN_AI_KEY')
if api_key is None:
    raise ValueError("API key not found in environment variables")


class ChatboxSerializer(serializers.ModelSerializer):
    class Meta :
        model=ChatMessage
        fields=['id','user_message','bot_response','timestamp']
        read_only_fields=['bot_response','timestamp']
    
    def create(self,validated_data):
        user_message=validated_data.get('user_message')
        client=OpenAI(api_key=api_key)
                
        try:
            response=client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[{'role': 'user', 'content': user_message}],
                max_tokens=100
            )
            bot_response=response.choices[0].message.content.strip()
        except Exception as e:
            raise serializers.ValidationError({'error':str(e)})
        
        chat_message=ChatMessage.objects.create(
            user_message=user_message,  
            bot_response=bot_response
        )
        return chat_message
    