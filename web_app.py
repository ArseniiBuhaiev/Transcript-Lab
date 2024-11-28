import gradio as gr
from transcript import main_phonetic as phonetic
from transcript import main_phonematic as phonematic

with gr.Blocks() as web:
    with gr.Row():
        with gr.Column():
            input_box = gr.Textbox(
                label='Текст для транскрибування',
                info='Слово, введене тут, буде транскрибоване.'
            )

        with gr.Column():
            output_box = gr.Textbox(
                label='Транскрибований текст',
                info='Поле для виведення транскрипції обраного типу.'
            )
            func_select = gr.Radio(
                ['Фонетична', 'Фонематична'],
                label='Оберіть тип транскрипції:'
            )

    def choose_func(selection, inp):
        if selection == 'Фонетична':
            return phonetic(inp)
        if selection == 'Фонематична':
            return phonematic(inp)
        
    submit_btn = gr.Button('Транскрибувати')
    input_box.change(
        fn=choose_func,
        inputs=[func_select, input_box],
        outputs=output_box
    )
    func_select.change(
        fn=choose_func,
        inputs=[func_select, input_box],
        outputs=output_box
    )

web.launch()