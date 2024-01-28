from __future__ import annotations
from email import message
from flask import Flask, Response, render_template, jsonify, request
import os
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.manager import AsyncCallbackManager
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from flask_socketio import SocketIO
from typing import TYPE_CHECKING, Any, Dict, List
from langchain.callbacks.base import BaseCallbackHandler
if TYPE_CHECKING:
    from langchain_core.agents import AgentAction, AgentFinish
    from langchain_core.messages import BaseMessage
    from langchain_core.outputs import LLMResult

#-----------------------------------------------------------------------------
class StreamingStdOutCallbackHandler_flask(BaseCallbackHandler):
    """Callback handler for streaming. Only works with LLMs that support streaming."""
    def __init__(self):
        self.accumulated_tokens = ""  

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts running."""

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        **kwargs: Any,
    ) -> None:
        """Run when LLM starts running."""

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        socketio.sleep(0.01)
        
        socketio.emit('new_token', {'token': token})
        print(token)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        global global_shared_data
        global_shared_data['ans'] = response.generations[0][0].text
        
        #global_shared_data[key] = value
        """LLM ends"""
        

    def on_llm_error(self, error: BaseException, **kwargs: Any) -> None:
        """Run when LLM errors."""

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Run when chain starts running."""

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""

    def on_chain_error(self, error: BaseException, **kwargs: Any) -> None:
        """Run when chain errors."""

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Run when tool starts running."""

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""
        pass

    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Run when tool ends running."""

    def on_tool_error(self, error: BaseException, **kwargs: Any) -> None:
        """Run when tool errors."""

    def on_text(self, text: str, **kwargs: Any) -> None:
        """Run on arbitrary text."""

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Run on agent end."""

def run_chain(user_input):
    summary_requirements_chain.run({"input":user_input})
    
#-----------------------------------------------------------------------------
os.environ['OPENAI_API_KEY'] = " "#Insert your OpenAI api key
llm = ChatOpenAI(temperature=0.2,
                     model_name="gpt-3.5-turbo-1106",streaming = True,
                     callback_manager=AsyncCallbackManager([StreamingStdOutCallbackHandler_flask()]),
                      )


summary_requirements_template = """You are to read through a customer's dialogue transcript list between >>> <<<, 
answer as long as possible
>>>{input}<<<
Requirements:"""
#formatted_template = template % (vector_history)

prompt=PromptTemplate(input_variables=["input"], template=summary_requirements_template)
summary_requirements_chain=LLMChain(llm=llm, prompt=prompt,verbose=False)


#------------------------------------------------------------------------------------
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
global_shared_data = {}
def update_global_data(key, value):
    global global_shared_data
    global_shared_data[key] = value
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    
    
    socketio.start_background_task(run_chain, user_input=user_input)
      
   

    return jsonify({'reply': None})


if __name__ == '__main__':
    socketio.run(app, debug=True)
