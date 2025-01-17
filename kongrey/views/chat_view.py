from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from kongrey.conf import settings
from kongrey.utils.http_client import httpx_common
from kongrey.utils.tools import jsonify
from kongrey.utils import tools
from kongrey.utils.decorators import auth_required, validate_request
from kongrey.models.chat_model import ChatModel
from kongrey.models.message_model import MessageModel
from kongrey.models.content_model import ContentModel
from kongrey.utils.schemas import chat_id_schema, send_message_schema, get_messages_schema
from kongrey.services import chat_service

route = APIRouter()


@route.post('/chat-id')
@auth_required
@validate_request(chat_id_schema)
async def get_chat_id(request: Request):
    body = await request.json()
    title = body.get('title')

    url = f'{settings.ai_url}/v1/oapi/agent/chat/conversation/create'
    headers = {
        'Content-Type': 'application/json',
        'Access-key': settings.ai_api_key,
        'Workspace-Id': settings.ai_workspace_id
    }
    data = {
        'robot_id': settings.ai_robot_id,
        'user': 'wangxun',
        'title': title
    }
    response = await httpx_common.post(url, headers=headers, json=data)
    response = response.json()
    data = response.get('data')
    conversation_id = data.get('conversation_id')

    user = request.state.user
    user_id = user.id
    await ChatModel().add_chat(conversation_id, title, user_id)
    return jsonify(conversation_id)


@route.post('/send-message')
@auth_required
@validate_request(send_message_schema)
async def send_message(request: Request):
    body = await request.json()
    conversation_id = body.get('conversation_id')
    content = body.get('content')

    trace_id = tools.generate_uuid()
    chat_info = await ChatModel().get_chat_by_conversation(conversation_id)
    chat_id = chat_info['ID']

    message_id = await MessageModel().add_message(chat_id, trace_id, 'user')
    await ContentModel().add_content(message_id, content)

    return StreamingResponse(chat_service.stream_data(conversation_id, chat_id, trace_id, content), media_type='text/event-stream')


# 所有会话
@route.post('/chats')
@auth_required
async def get_chats(request: Request):
    user = request.state.user
    user_id = user.id
    chats = await ChatModel().get_chats(user_id)
    return jsonify(chats)


# 所有问答
@route.post('/messages')
@auth_required
@validate_request(get_messages_schema)
async def get_messages(request: Request):
    body = await request.json()
    conversation_id = body.get('conversation_id')

    chats = await MessageModel().get_messages(conversation_id)
    return jsonify(chats)
