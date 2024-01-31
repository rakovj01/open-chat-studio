import factory
from openai.types.beta import Assistant


class AssistantFactory(factory.Factory):
    class Meta:
        model = Assistant

    id = factory.Faker("uuid4")
    created_at = factory.Faker("pyint")
    name = factory.Faker("name")
    description = factory.Faker("sentence")
    file_ids = []
    metadata = None
    object = "assistant"
    instructions = factory.Faker("sentence")
    model = factory.Faker("random_element", elements=["gpt4", "gpt-3.5-turbo"])
    tools = [
        {"type": "code_interpreter"},
        {"type": "retrieval"},
        {"type": "function", "function": {"name": "test", "parameters": {"test": {"type": "string"}}}},
    ]
