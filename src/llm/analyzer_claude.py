from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import asyncio

from src.utils.logger import setup_logger
logger = setup_logger()

async def analyze_chunks_async(chunks, api_key, llm_model="claude-3-opus-20240229", batch_size=5):
    """
    Asynchronously analyze code chunks using Claude 3 via Anthropic API.
    """
    logger.info(f"Starting Claude analysis with {len(chunks)} chunks using model {llm_model}")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found.")

    # Define the prompt template
    code_analysis_prompt = ChatPromptTemplate.from_template(
        "Analyze the following code chunk and provide insights, improvements, or issues:\n\n{code_chunk}"
    )

    # Initialize Claude LLM
    llm = ChatAnthropic(
        model=llm_model,
        temperature=0,
        api_key=api_key
    )

    # Compose the chain
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