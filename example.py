#Qwen2.5-Coder-32B製。llama-cpp-python代替関数のテスト
import alt_llama_cpp

# 使用例
model=alt_llama_cpp.start_llama_server(
    model_path="DeepSeek-R1-Distill-Qwen-32B-Q5_K_M.gguf",
    n_gpu_layers=-1,
    n_ctx=512,
    n_batch=512,
    #flash_attn=True,
    #tensor_split=[100, 0],
    #last_n_tokens_size=64
)

#使用例1(通常出力)
if model is not None:
 system_prompt="あなたは優秀で誠実なアシスタントです"
 prompt = system_prompt+"こんにちは"
 response = alt_llama_cpp.response(prompt,
                                   stream=False)
 #通常出力の処理
 output = response.choices[0].message.content
 print(output)

#使用例2(ストリーミング出力)
if model is not None:
 system_prompt="あなたは優秀で誠実なアシスタントです"
 prompt = system_prompt+"東京の魅力を100文字で教えて"
 response = alt_llama_cpp.response(prompt,
                                   max_tokens=512,
                                   temperature = 0.6,
                                   top_p=0.95, 
                                   stop=["<|stop|>"] ,
                                   stream=True)
 #ストリーミング出力の処理
 for chunk in response:
     output =  chunk.choices[0].delta.content
     if output:
        print(output,end="",flush=True)
alt_llama_cpp.stop_llama_server()#llama-serverを終了してVRAM/RAMを開放する