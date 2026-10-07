from llama_index.core.node_parser import SentenceSplitter

from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader(
    input_files=["data_folder/ashishmauryab.pdf"] 
).load_data()

splitter = SentenceSplitter(

    chunk_size= 200, 
    chunk_overlap= 50 
)

nodes = splitter.get_nodes_from_documents(documents)

for i ,  tests  in enumerate(nodes):
    print(tests.text)
    print(len(tests.text))



