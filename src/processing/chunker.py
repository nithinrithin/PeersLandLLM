from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import CHUNK_SIZE, CHUNK_OVERLAP
import asyncio

def chunk_code(code_files: list):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    # return splitter.create_documents(code_files)
    def chunk_file(file):
        content = file["content"]
        path = file["path"]
        char_chunks = splitter.create_documents([content])
        return [
            {"path": path, "page_content": doc.page_content}
            for doc in char_chunks
        ]
    all_chunks = [chunk_file(file) for file in code_files]
    return [chunk for file_chunks in all_chunks for chunk in file_chunks]

async def chunk_code_async(files, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """
    Concurrently chunks each file using asyncio.gather and RecursiveCharacterTextSplitter.
    Applies chunk_overlap and returns structured chunks with file path.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    async def chunk_file(file):
        content = file["content"]
        path = file["path"]
        char_chunks = splitter.create_documents([content])
        return [
            {"path": path, "page_content": doc.page_content}
            for doc in char_chunks
        ]

    all_chunks = await asyncio.gather(*(chunk_file(f) for f in files))
    return [chunk for file_chunks in all_chunks for chunk in file_chunks]

# from tree_sitter import Language, Parser
# from langchain.text_splitter import TokenTextSplitter
# from tree_sitter import Language, Parser
# from langchain.text_splitter import TokenTextSplitter
# # Load your precompiled grammar (e.g., Python, Java, etc.)
# GENERIC_LANGUAGE = Language("build/my-languages.so", "generic")

# parser = Parser()
# parser.set_language(GENERIC_LANGUAGE)

# def extract_tree_chunks(code: str, parser: Parser, min_bytes=50, max_depth=3):
#     """
#     Traverse the syntax tree and extract chunks based on node size and depth.
#     Ignores AST types — purely structural.
#     """
#     tree = parser.parse(bytes(code, "utf8"))
#     root = tree.root_node
#     chunks = []

#     def walk(node, depth=0):
#         if node.child_count == 0:
#             return

#         size = node.end_byte - node.start_byte
#         if size >= min_bytes and depth <= max_depth:
#             chunks.append(code[node.start_byte:node.end_byte])
#         else:
#             for child in node.children:
#                 walk(child, depth + 1)

#     walk(root)
#     return chunks if chunks else [code]

# def chunk_code_tree(files, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
#     """
#     Applies tree-based chunking followed by token-safe splitting using TokenTextSplitter.
#     """
#     splitter = TokenTextSplitter(
#         chunk_size=chunk_size,              # Max tokens per chunk
#         chunk_overlap=chunk_overlap,        # Overlap tokens between chunks
#         encoding_name="cl100k_base"         # Tokenizer used by GPT-4 and GPT-3.5
#     )

#     final_chunks = []
#     for file in files:
#         path = file["path"]
#         content = file["content"]

#         # Step 1: Tree-based structural chunking
#         tree_chunks = extract_tree_chunks(content, parser)

#         # Step 2: Token-safe splitting
#         for chunk in tree_chunks:
#             token_chunks = splitter.create_documents([chunk])
#             for doc in token_chunks:
#                 final_chunks.append({
#                     "path": path,
#                     "page_content": doc.page_content
#                 })

#     return final_chunks
