from Projects.rgb_tester import NeoPixelTester
from Projects.dimming_tester import DimmingTester
from Projects.gyropong_tester import GyroPongTester
from Projects.joystick_tester import JoystickTester
from Projects.any_meter_tester import AnyMeterTester
from Tester.hinter import Hinter
from Tester.tester import Tester
from machine import Pin
start_button = Pin(20, Pin.IN) 
select_button = Pin(21, Pin.IN)


class Demo():
    def __init__(self):
        self.hinter = Hinter()
        self.testers = [
            GyroPongTester(),
            DimmingTester(),
            NeoPixelTester(),
            AnyMeterTester(),
            JoystickTester(),
        ]
        self.selected_tester = self.testers[0]
        self.tester_index = 0
        
    def select_tester(self, tester: Tester):
        self.hinter.clear()
        if self.selected_tester is not None:
            self.selected_tester.stop()
        self.selected_tester = tester
        self.hinter.drawModules(self.selected_tester.config)
        
    def cancel_handler(self, pin):
        self.selected_tester.cancel_handler(pin)
        # self.hinter.drawModules(self.selected_tester.config)
        pin.irq(handler=None)  # Disable the cancel handler

    def start_selected_tester(self):
        if self.selected_tester is not None:
            self.hinter.tester_is_running(self.selected_tester.name)
            select_button.irq(trigger=Pin.IRQ_RISING, handler=self.cancel_handler) 
            self.selected_tester.start()
        else:
            print("No tester selected")
        
    def run(self):
        self.hinter.display.draw_logo(y=90)
        self.hinter.display.fill_rect(100, 300, 140, 20, self.hinter.display.WHITE)
        self.hinter.display.fill_polygon(
            [(10, 285) ,(10, 310), (35, 310), (27, 302), (43, 286), (34, 277), (18, 293), (10, 285)],
            0,
            0,
            self.hinter.display.BLACK
        )

        self.hinter.display.text("start", 10, 261, fg=self.hinter.display.BLACK, bg=self.hinter.display.WHITE)
        self.hinter.display.text("next", 198, 261, fg=self.hinter.display.BLACK, bg=self.hinter.display.WHITE)

        self.hinter.display.text("Press any button", 56, 290, fg=self.hinter.display.BLACK, bg=self.hinter.display.WHITE)
        self.hinter.display.hline(55, 306, 129, self.hinter.display.BLACK)
        # self.hinter.display.text("GP20", 45, 282, font=self.hinter.display.font_bold, fg=self.hinter.display.BLACK, bg=self.hinter.display.WHITE)
        # self.hinter.display.text("start", 48, 270, fg=self.hinter.display.BLACK, bg=self.hinter.display.WHITE)
        # self.hinter.display.text("GP21", 131, 282, font=self.hinter.display.font_bold, fg=self.hinter.display.BLACK, bg=self.hinter.display.WHITE)
        # self.hinter.display.text("next", 157, 270, fg=self.hinter.display.BLACK, bg=self.hinter.display.WHITE)
        self.hinter.display.fill_polygon(
            [(10, 285) ,(10, 310), (35, 310), (27, 302), (43, 286), (34, 277), (18, 293), (10, 285)],
            -80,
            320,
            self.hinter.display.BLACK,
            4.71238898038,
        )
        while select_button.value() == 0 and start_button.value() == 0:
            pass
        self.select_tester(self.selected_tester)
        while True:
            if select_button.value() == 1:
                self.tester_index = (self.tester_index + 1) % len(self.testers)
                self.select_tester(self.testers[self.tester_index])
                while select_button.value() == 1: pass
            if start_button.value() == 1:
                try:
                    self.start_selected_tester()
                except Exception as e:
                    print(f"Error starting tester: {e}")
                    self.hinter.show_error(str(e))