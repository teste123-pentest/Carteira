from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import requests

SERVER_IP = "192.168.100.15"  # Troque se o IP mudar

class CarteiraLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.label = Label(text="Insira o valor:")
        self.add_widget(self.label)

        self.valor_input = TextInput(hint_text="R$ 0.00", multiline=False)
        self.add_widget(self.valor_input)

        self.btn_pagar = Button(text="Pagar")
        self.btn_pagar.bind(on_press=self.enviar_pagamento)
        self.add_widget(self.btn_pagar)

        self.btn_extrato = Button(text="Ver Extrato")
        self.btn_extrato.bind(on_press=self.ver_extrato)
        self.add_widget(self.btn_extrato)

        self.resultado = Label(text="")
        self.add_widget(self.resultado)

    def enviar_pagamento(self, instance):
        valor = self.valor_input.text
        try:
            response = requests.post(f"http://{SERVER_IP}:5000/pagar", json={"valor": valor})
            self.resultado.text = response.json().get("mensagem", "Erro ao pagar")
        except Exception as e:
            self.resultado.text = f"Erro: {e}"

    def ver_extrato(self, instance):
        try:
            response = requests.get(f"http://{SERVER_IP}:5000/extrato")
            extrato = response.json().get("extrato", [])
            texto = "\n".join([f"R$ {e['valor']} em {e['data']}" for e in extrato])
            self.resultado.text = texto or "Sem transações"
        except Exception as e:
            self.resultado.text = f"Erro: {e}"

class CarteiraApp(App):
    def build(self):
        return CarteiraLayout()

if __name__ == '__main__':
    CarteiraApp().run()
          
