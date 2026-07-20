from langchain_aws import ChatBedrock

llm = ChatBedrock(
    model_id="amazon.nova-pro-v1:0",
    region_name="us-west-2"
)

response = llm.invoke("Explain LangGraph.")

print(response.content)