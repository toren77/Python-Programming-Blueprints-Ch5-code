from nameko.rpc import rpc, RpcProxy
from nameko.web.handlers import http
from .dependencies.redis import MessageStore
from .dependencies.jinja2 import Jinja2


class WebServer:

    name = 'web_server'
    message_service = RpcProxy('message_service')
    jinja = Jinja2()

    @http('GET', '/')
    def home(self, request):
        messages = self.message_service.get_all_messages()
        rendered_template = self.jinja.render_home(messages)

        return rendered_template


class MessageService:
    name = 'message_service'

    message_store = MessageStore()

    @rpc
    def get_message(self, message_id):
        return self.message_store.get_message(message_id)

    @rpc
    def save_message(self, message):
        message_id = self.message_store.save_message(message)
        return message_id

    @rpc
    def get_all_messages(self):
        messages = self.message_store.get_all_messages()
        return messages





