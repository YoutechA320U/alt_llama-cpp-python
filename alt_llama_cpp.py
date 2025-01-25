#Qwen2.5-Coder-32B製。llama.cppのllama-serverをllama-cpp-pythonライクに操作するライブラリ
from openai import OpenAI
import subprocess
from typing import List, Optional

llama_server_path = "llama_cpp"#llama-server 実行ファイルのパスを指定
llama_server_process = None  # グローバル変数としてプロセスオブジェクトを保持

def start_llama_server(model_path: str, 
                       n_gpu_layers: Optional[int] = None, 
                       n_ctx: Optional[int] = 512, 
                       n_batch: Optional[int] = 512, 
                       flash_attn: Optional[bool] = None, 
                       tensor_split: Optional[List[int]] = None, 
                       last_n_tokens_size: Optional[int] = 64) -> None:
    """
    llama-server.exe を起動する関数

    Args:
        model_path (str): モデルのファイルパス
        n_gpu_layers (Optional[int]): GPUレイヤーの数 (デフォルト: None)
        n_ctx (Optional[int]): コンテキストサイズ (デフォルト: 512)
        n_batch (Optional[int]): バッチサイズ (デフォルト: 512)
        flash_attn (Optional[bool]): Flash Attention を使用するかどうか (デフォルト: None)
        tensor_split (Optional[List[int]]): テンソルの分割比率 (デフォルト: None)
        last_n_tokens_size (Optional[int]): 最後のnトークンのサイズ (デフォルト: 64)
    """
    global llama_server_process  # グローバル変数を使用
    
    command = [
        f"{llama_server_path}\\llama-server.exe",
        "-m", model_path
    ]
    
    if n_gpu_layers is not None:
        if n_gpu_layers == -1:
            command.extend(["-ngl", "9999"])
        else:
            command.extend(["-ngl", str(n_gpu_layers)])
    
    if n_ctx is not None:
        command.extend(["-c", str(n_ctx)])
    
    if n_batch is not None:
        command.extend(["-b", str(n_batch)])
    
    if flash_attn is True:
        command.append("-fa")
    
    if tensor_split is not None:
        command.extend(["-ts", ",".join(map(str, tensor_split))])
    
    if last_n_tokens_size is not None:
        command.extend(["--repeat-last-n", str(last_n_tokens_size)])
    
    try:
        llama_server_process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True,  # テキストモードで出力を扱う
            encoding='utf-8'  # UTF-8 でエンコード
        )
        # 出力をキャプチャして表示
        for line in llama_server_process.stdout:
            print(f"{line.strip()}")
            if line.strip() == "srv  update_slots: all slots are idle":
                #print("llama-server を正常に起動しました。")
                break
        return "load_complate"
    except Exception as e:
        print(f"llama-server の起動中にエラーが発生しました: {e}")
# 使用例
#start_llama_server(
#    model_path="F:\\gguf\\sarashina2.1-1b-sft-imatrix-Q8_0-4329.gguf",
#    n_gpu_layers=32,
#    n_ctx=512,
#    n_batch=512,
#   flash_attn=True,
#    tensor_split=[100, 0],
#   last_n_tokens_size=64
#)

def stop_llama_server():
    """
    起動中の llama-server.exe を終了する関数
    """
    global llama_server_process  # グローバル変数を使用
    
    if llama_server_process is not None:
        llama_server_process.terminate()  # プロセスを終了
        llama_server_process = None  # プロセスオブジェクトをリセット
        #print("llama-server を正常に終了しました。")
    else:
        #print("llama-server は起動していません。")
        pass
# 使用例
#stop_llama_server()

def response(system_prompt,prompt,temperature=0.8, top_p=0.95, stop=None, stream=False):
    """
    起動中の llama-server.exe に回答してもらう関数
    """
    client = OpenAI(
        api_key="YOUR_API_KEY",
        base_url="http://localhost:8080/v1"
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    
    stream_options = {"include_usage": True} if stream else None
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        stop=stop if stop is not None else [],
        stream=stream,
        stream_options=stream_options,
    )
    
    return response

# 使用例1
#system_prompt="あなたは優秀で誠実なアシスタントです"
#prompt = "東京の魅力を100文字で教えて"
#response = alt_llama_cpp.response(system_prompt,prompt,stream=True)
#print(response)
# ストリーミング出力の処理
#for chunk in response:
#    output =  chunk.choices[0].delta.content
#    if output:
#       print(output,end="",flush=True)
#alt_llama_cpp.stop_llama_server()

# 使用例2
#system_prompt="あなたは優秀で誠実なアシスタントです"
#prompt = "東京の魅力を100文字で教えて"
#response = alt_llama_cpp.response(system_prompt,prompt,stream=False)
#print(response)
# 通常出力の処理
#output = response.choices[0].message.content
#print(output)
#alt_llama_cpp.stop_llama_server()