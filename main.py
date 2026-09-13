from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

Window.size = (360, 640)

class RowCounterTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        self.count = 0
        self.label_count = Label(text=str(self.count), font_size=80)
        self.add_widget(self.label_count)
        btn_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        btn_minus = Button(text='-1', font_size=32)
        btn_minus.bind(on_press=self.decrement)
        btn_layout.add_widget(btn_minus)
        btn_plus = Button(text='+1', font_size=32, background_color=(0.2, 0.6, 0.8, 1))
        btn_plus.bind(on_press=self.increment)
        btn_layout.add_widget(btn_plus)
        self.add_widget(btn_layout)
        btn_reset = Button(text='Сброс', size_hint_y=0.15)
        btn_reset.bind(on_press=self.reset)
        self.add_widget(btn_reset)

    def increment(self, instance):
        self.count += 1
        self.label_count.text = str(self.count)

    def decrement(self, instance):
        if self.count > 0:
            self.count -= 1
            self.label_count.text = str(self.count)

    def reset(self, instance):
        self.count = 0
        self.label_count.text = str(self.count)


class ReglanCalcTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=10, **kwargs)
        from kivy.uix.textinput import TextInput
        self.add_widget(Label(text='Плотность петель в 10 см (гориз.):'))
        self.input_stitches = TextInput(text='22', multiline=False, input_filter='float')
        self.add_widget(self.input_stitches)
        self.add_widget(Label(text='Обхват горловины / ОШ (см):'))
        self.input_neck = TextInput(text='38', multiline=False, input_filter='float')
        self.add_widget(self.input_neck)
        btn_calc = Button(text='Рассчитать горловину', size_hint_y=0.2)
        btn_calc.bind(on_press=self.calculate)
        self.add_widget(btn_calc)
        self.result_label = Label(text='Результат появится здесь', font_size=16)
        self.add_widget(self.result_label)

    def calculate(self, instance):
        try:
            st_10 = float(self.input_stitches.text)
            neck_cm = float(self.input_neck.text)
            total_st = round(neck_cm * (st_10 / 10.0))
            body_st = total_st - 8
            back = front = round(body_st * 0.3)
            sleeve = round((body_st - back - front) / 2)
            self.result_label.text = f'Всего набрать: {total_st} п.\nСпинка/Перед: по {back} п.\nРукава: по {sleeve} п.'
        except ValueError:
            self.result_label.text = 'Ошибка ввода чисел'


class KnitApp(App):
    export_to_desktop = True
    def build(self):
        root = TabbedPanel(do_default_tab=False)
        tab_counter = TabbedPanelItem(text='Счетчик')
        tab_counter.add_widget(RowCounterTab())
        root.add_widget(tab_counter)
        tab_calc = TabbedPanelItem(text='Реглан')
        tab_calc.add_widget(ReglanCalcTab())
        root.add_widget(tab_calc)
        root.switch_to(tab_counter)
        return root

if __name__ == '__main__':
    KnitApp().run()
