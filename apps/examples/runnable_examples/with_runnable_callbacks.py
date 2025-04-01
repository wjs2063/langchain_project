from langchain.callbacks.tracers import ConsoleCallbackHandler, FunctionCallbackHandler
from langchain_core.runnables import RunnablePassthrough, RunnableLambda


def _print(x):
    return x


# console 출력은 Sequence first -> first ... last -> Sequence last
runnable = (
    RunnablePassthrough()
    | RunnableLambda(lambda x: {"text": x})
    | RunnableLambda(lambda x: {"text": x})
)

# runnable.invoke("안녕", config={"callbacks": [ConsoleCallbackHandler()]})
