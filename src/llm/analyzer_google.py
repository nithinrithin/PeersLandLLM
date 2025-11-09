import time
from src.utils.logger import setup_logger
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from .prompt_template import code_analysis_prompt

logger = setup_logger()

import asyncio

async def analyze_chunks_async(chunks, api_key, llm_model, batch_size=5):
    """
    Asynchronously analyze code chunks using Google Gemini model.
    """

    logger.info(f"Starting gemini analysis with {len(chunks)} chunks with model {llm_model}")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment.")
    llm = ChatGoogleGenerativeAI(
        model=llm_model,
        temperature=0,
        google_api_key=api_key
    )
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
                results.append({
                    "path": chunk["path"],
                    "analysis": result
                })
        except Exception as e:
            logger.error(f"Batch failed: {e}")
            await asyncio.sleep(10)  # backoff
    return results

def analyze_chunks(chunks: list, api_key: str) -> list:
    """
    Analyze code chunks using Google Gemini model."""
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment.")

    llm = ChatGoogleGenerativeAI(
        # model="models/gemini-2.5-pro",
        model="models/gemini-embedding-001",
        google_api_key=api_key,
        temperature=0
    )

    chain = code_analysis_prompt | llm | StrOutputParser()

    results = []
    for chunk in chunks:
        try:
            response = chain.invoke({"code_chunk": chunk.page_content})
            results.append(response)
            time.sleep(60) #To respect rate limits
        except Exception as e:
            print(f"Error analyzing chunk: {e}")
    return results