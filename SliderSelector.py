import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

# 参数全名
full_name = {
    "k_1": "Elastic coefficient[N/m]",
    "k_2": "Another elastic coefficient[N/m]",
    "M": "Disk quality[kg]",
    "R": "Disk radius[m]",
    "gamma": "damping factor[s^(-1)]",
    "M_Cu": "Brass screws quality[kg]",
    "L_Cu": "d(brass screws, disk center)[m]",
    "omega": "Drive angular velocity[m/s]"
}

class SliderSelector:
    def __init__(self, fig, axmodel_rect, params, changed):
        """
        初始化 SliderSelector
        :param fig: Matplotlib 的 Figure 对象
        :param axmodel_rect: 滑动条所在的 Axes 区域 [x, y, width, height]
        :param params: 参数字典，格式为 {param_name: (valmin, valmax, valinit)}
        :param changed: 滑动条更新时的回调函数，要求有两个参数，第一个为参数名称，第二个为滑动条当前取值
        """
        self.fig = fig
        self.axmodel_rect = axmodel_rect
        self.params = params
        self.current_slider = None
        self.current_label = None
        self.changed = changed

    def create_slider(self, param_name):
        """
        创建滑动条
        :param param_name: 参数名称
        """
        self.remove_slider()  # 移除已有的滑动条
        # 重新创建 Axes
        self.axmodel = self.fig.add_axes(self.axmodel_rect)  
        valmin, valmax, valinit = self.params[param_name]
        self.current_slider = Slider(
            ax=self.axmodel,
            # 映射为全名
            label=full_name[param_name],
            valmin=valmin,
            valmax=valmax,
            valinit=valinit,
        )
        # 添加回调
        self.current_slider.on_changed(lambda x: self.changed(param_name, x))
        self.current_label = param_name
        self.current_slider.valtext.set_visible(False)  # 隐藏值显示
        # self.current_slider.ax.set_xticks(np.arange(valmin, valmax, (valmax - valmin) / 6))
        self.fig.canvas.draw_idle()

    def remove_slider(self):
        """
        移除当前滑动条
        """
        if self.current_slider is not None:
            self.current_slider.ax.remove()
            self.current_slider = None
            self.current_label = None
            self.fig.canvas.draw_idle()

    def update_slider(self, param_name):
        """
        更新滑动条
        :param param_name: 要显示的参数名称
        """
        if param_name != self.current_label:
            self.create_slider(param_name)
    
    def val(self):
        return self.val
