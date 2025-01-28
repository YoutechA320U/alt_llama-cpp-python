## alt_llama-cpp-python

[llama.cpp](https://github.com/ggerganov/llama.cpp)のllama-serverを[llama-cpp-python](https://github.com/abetlen/llama-cpp-python)ライクに操作するライブラリ

## 必要なライブラリ
    openai

## 使い方
```python
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
 prompt = system_prompt+"こんにちは。"
 response = alt_llama_cpp.response(prompt,
                                   stream=False)
 #通常出力の処理
 output = response.choices[0].message.content
 print(output)
#<think>
#Alright, the user greeted me with "こんにちは," which is "Hello" in Japanese. I should respond politely in Japanese to match their greeting.
#
#I'll use "おはようございます" for a morning greeting, but since I'm not sure of the time, I'll include a general "こんにちは" as well. Adding "いかがお過ごしですか？" shows I'm interested in their day.
#
#I need to make sure my response is friendly and ready to assist them further.
#</think>
#
#おはようございます！ こんにちは。いかがお過ごしですか？ 何かお手伝いできることがございましたら、お知らせください。

#使用例2(ストリーミング出力)
if model is not None:
 system_prompt="あなたは優秀で誠実なアシスタントです"
 prompt = system_prompt+"東京の魅力を100文字で教えて"
 response = alt_llama_cpp.response(prompt,
                                   max_tokens=512
                                   temperature = 0.6,
                                   top_p=0.95, 
                                   stop=["<|stop|>"] ,
                                   stream=True)
 #ストリーミング出力の処理
 for chunk in response:
     output =  chunk.choices[0].delta.content
     if output:
        print(output,end="",flush=True)
#<think>
#Alright, so the user has asked me to explain the charm of Tokyo in 100 characters. Let me break this down. First, I need to understand the context. The user is probably #looking for a concise yet comprehensive overview of Tokyo's attractions. Since it's limited to 100 characters, I have to be very precise with my words.
#
#I should start by identifying the key aspects that make Tokyo unique. Tokyo is known for its blend of tradition and modernity. So mentioning historical sites like Senso-ji Temple and modern landmarks like the Tokyo Skytree would cover that aspect. Additionally, Tokyo is famous for its vibrant nightlife, shopping districts, and the iconic Shibuya Crossing. These elements highlight the city's dynamic energy.
#
#Cuisine is another important point. Tokyo offers a wide variety of authentic Japanese dishes, from sushi in Tsukiji to ramen in various neighborhoods. Including this would appeal to food enthusiasts. Lastly, Tokyo's efficient public transportation system is a big plus for both tourists and residents, making navigation easy and stress-free.
#
#Now, I need to condense all these points into a coherent sentence that flows well and stays within the character limit. I'll make sure to include the main attractions, cultural mix, culinary delights, and transportation. Let me piece this together: mention the temples, the Skytree, Shibuya Crossing, the diverse food scene, and the convenient transport. That should cover all the essential aspects succinctly.
#</think>
#
#東京は、伝統と現代が融合した魅力あふれる都市です。浅草寺や東京スカイツリーといった観光名所、 Shibuya Crossingや新宿の活気ある街並み、寿司やラーメンなどの多彩な食文化、そして便利な公共交通システムがあります。昼夜問わず楽しめる都市です。
alt_llama_cpp.stop_llama_server()#llama-serverを終了してVRAM/RAMを開放する
```
## 備考

あくまで最低限の機能だけ再現しています。操作方法も完全に同じではありません。

※本ライブラリは[Qwen2.5-Coder-32B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct)によって生成されました。

## 履歴
    [2025/01/25] - 初回リリース
    [2025/01/25] - 分割されていたシステムプロンプトと通常プロンプト単一化。max_token追加