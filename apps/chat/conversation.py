from datetime import datetime
from typing import Optional, Tuple

import pytz
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.chat_models.anthropic import ChatAnthropic
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.schema import BaseMemory
from langchain.utilities.anthropic import get_num_tokens_anthropic

from apps.chat.agent.agent import AgentExecuter
from apps.experiments.models import ExperimentSession


class Conversation:
    """
    A wrapper class that provides a single way/API to interact with the LLMs, regardless of it being a normal
    conversation or agent implementation
    """

    def __init__(
        self,
        prompt_str: str,
        source_material: str,
        memory: BaseMemory,
        llm,
        experiment_session: Optional[ExperimentSession] = None,
    ):
        UTC = pytz.timezone("UTC")
        current_datetime = datetime.now().astimezone(UTC)
        prompt_to_use = SystemMessagePromptTemplate.from_template(prompt_str)
        if source_material:
            try:
                prompt_to_use = prompt_to_use.format(source_material=source_material)
            except KeyError:
                # no source material found in prompt, just use it "naked"
                pass
        if experiment_session and experiment_session.experiment.tools_enabled:
            self.executer = AgentExecuter(llm=llm, memory=memory, experiment_session=experiment_session)
            # Insert the messages here
            current_date_message = SystemMessagePromptTemplate.from_template("{current_date}")
            self.executer.agent.prompt = OpenAIFunctionsAgent.create_prompt(
                system_message=prompt_to_use,
                extra_prompt_messages=[
                    MessagesPlaceholder(variable_name="history"),
                    current_date_message.format(current_date=str(current_datetime)),
                ],
            )
        else:
            prompt = ChatPromptTemplate.from_messages(
                [
                    prompt_to_use,
                    MessagesPlaceholder(variable_name="history"),
                    HumanMessagePromptTemplate.from_template("{input}"),
                ]
            )
            self.executer = ConversationChain(memory=memory, prompt=prompt, llm=llm)

    def load_memory(self, messages):
        self.executer.memory.chat_memory.messages = messages

    def predict(self, input: str) -> Tuple[str, int, int]:
        if not isinstance(self.executer, AgentExecuter) and isinstance(self.executer.llm, ChatAnthropic):
            # Langchain has no inbuilt functionality to return prompt or
            # completion tokens for Anthropic's models
            # https://python.langchain.com/docs/modules/model_io/llms/token_usage_tracking
            # Instead, we convert the prompt to a string, and count the tokens
            # with Anthropic's token counter.
            # TODO: When we enable the AgentExecuter for Anthropic models, we should revisit this
            response = self.executer.predict(input=input)
            formatted_prompt = self.executer.prompt.format_prompt(
                input=input,
                history=self.memory.buffer_as_messages,
            ).to_string()
            prompt_tokens = get_num_tokens_anthropic(formatted_prompt)
            completion_tokens = get_num_tokens_anthropic(response)
            return response, prompt_tokens, completion_tokens
        else:
            with get_openai_callback() as cb:
                response = self.executer.predict(input=input)
            return response, cb.prompt_tokens, cb.completion_tokens

    @property
    def _is_agent(self) -> bool:
        return isinstance(self.executer, AgentExecuter)
