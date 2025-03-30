import gradio as gr
import wave
import os
import pyaudio
from vosk import Model, KaldiRecognizer
from function_calling import PollutionQueryHandler

MODEL_PATH = "vosk-model-small-vn-0.4"

model = Model(MODEL_PATH)

api_key = "CLAUDE_API_KEY"
handler = PollutionQueryHandler(api_key)

def speech_to_text():
    recognizer = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("🎤 Đang lắng nghe...")

    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            try:
                text = result.split('"')[3]  # Trích xuất text
            except IndexError:
                text = "Không nhận diện được âm thanh. Vui lòng thử lại."
            stream.stop_stream()
            stream.close()
            p.terminate()
            print(f"📝 Bạn nói: {text}")
            return text

def chat(prompt):
    result = handler.call_claude_function(prompt)
    final_result = handler.rewrite_result_with_advice(result)
    return final_result


with gr.Blocks() as demo:
    gr.Markdown("## Hệ thống Truy vấn, dự đoán khả năng ô nhiễm ")

    gr.Markdown("""
    **Hướng dẫn sử dụng:**  
    - **Dự đoán mức độ ô nhiễm**, ví dụ:  
      - "Dự đoán mức độ ô nhiễm vào ngày 15 tháng 3 năm 2025 lúc 10 giờ với PT08_S1_CO 120.5, C6H6_GT 5.3, PT08_S5_O3 45.2, PT08_S2_NMHC 220.7, PT08_S4_NO2 34.1."  

    - **Truy vấn dữ liệu chất lượng không khí**, ví dụ:  
      - "Tôi muốn biết chất lượng không khí vào ngày 20 tháng 5 năm 2004."  

    - **Thống kê dữ liệu (mean, median, max, min, count)**, ví dụ:  
      - "Tính trung bình dữ liệu ô nhiễm từ 17 tháng 3 năm 2004 đến 17 tháng 4 năm 2004."  
      - "Tìm giá trị ô nhiễm nhỏ nhất từ 17 tháng 3 năm 2004 đến 17 tháng 4 năm 2004."  

    - **Thêm dữ liệu từ NLP**, ví dụ:  
      - "Thêm chất lượng không khí vào ngày 10 tháng 4 năm 2007, lúc 8 giờ sáng.  
        Tôi có các thông số: PT08_S1_CO = 80, C6H6_GT = 3.1, PT08_S5_O3 = 150, PT08_S2_NMHC = 85, PT08_S4_NO2 = 1.05 hPa, AQI_Label = 3."  
    """)

    textbox = gr.Textbox(label="Nhập truy vấn của bạn:")
    """voice_btn = gr.Button("Nói")"""
    submit_btn = gr.Button("Gửi")
    output = gr.Textbox(label="Phản hồi:")

    """voice_btn.click(fn=speech_to_text, inputs=[], outputs=textbox)  # Nhận giọng nói"""
    submit_btn.click(fn=chat, inputs=textbox, outputs=output)

if __name__ == "__main__":
    demo.launch(share=True)
