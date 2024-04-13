from llama_index.legacy.embeddings import HuggingFaceEmbedding
from llama_index.legacy.llms import LlamaCPP
from llama_index.llms.llama_cpp.llama_utils import (
    messages_to_prompt,
    completion_to_prompt,
)

llm = LlamaCPP(
    model_url="https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q4_0"
              ".bin",
    temperature=0.1,
    max_new_tokens=256,
    context_window=3900,
    generate_kwargs={},
    model_kwargs={"n_gpu_layers": 1},
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=True,
)


def get_embed_model():
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    return embed_model


async def get_answer(query, context):
    prompt = f"""Given the context below answer the question.
            Context: {context}
            Question: {query}
            Answer:
            """
    return await llm.acomplete(prompt=prompt)
