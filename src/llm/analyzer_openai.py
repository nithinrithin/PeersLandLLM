from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from .prompt_template import code_analysis_prompt
from src.utils.logger import setup_logger
logger = setup_logger()

def analyze_chunks(chunks: list, api_key: str) -> list:
    """
    Analyze code chunks using OpenAI GPT model.
    """
    if not api_key:
        raise ValueError("OPEN API not found in environment.")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=api_key)
    chain = code_analysis_prompt | llm | StrOutputParser()

    results = []
    for chunk in chunks:
        try:
            # response = chain.run(code_chunk=chunk.page_content)
            response = chain.invoke({"code_chunk": chunk.page_content})
            results.append(response)
        except Exception as e:
            print(f"Error analyzing chunk: {e}")
    return results

import asyncio

async def analyze_chunks_async(chunks, api_key, llm_model, batch_size=5):
    """
    Asynchronously analyze code chunks using OpenAI GPT model.
    """
    logger.info(f"Starting openAI analysis with {len(chunks)} chunks")
    llm = ChatOpenAI(model_name=llm_model, temperature=0, api_key=api_key)
    chain = code_analysis_prompt | llm | StrOutputParser()

    results = []
    for i in range(0, len(chunks), batch_size):
        logger.info(f"Processing batch {i // batch_size + 1}")
        batch = chunks[i:i+batch_size]
        tasks = [chain.ainvoke({"code_chunk": chunk["page_content"]}) for chunk in batch]
        try:
            batch_results = await asyncio.gather(*tasks)
            logger.info(f"Batch {i // batch_size + 1} completed")
            for result, chunk in zip(batch_results, batch):
                results.append({"path": chunk["path"], "analysis": result})
        except Exception as e:
            logger.error(f"Batch failed: {e}")
            await asyncio.sleep(10)
    return results
