# %matplotlib widget # 切换 matplotlib 的绘图后端为 ipymplimport math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from SliderSelector import SliderSelector

init_Data = [
    0,  ## NULL
    2.029,  ## Elastic coefficient  k_1
    2.029,  ## Another Elastic coefficient  k_2
    0.12,  ## Disk quality  M
    0.0475,  ## Disk radius  R
    0,  ## damping factor  gamma
    0.0015,  ## Brass screws quality  M_Cu
    0.06,  ## d(brass screws, disk center) L_Cu
    5.414,  ## Drive angular velocity  omega
]

# 初始化参数
params_init = {
    "k_1": (2.029, 2, 3),
    "k_2": (2.029, 2, 3),
    "M": (0.12, 0.1, 0.2),
    "R": (0.0475, 0.04, 0.05),
    "gamma": (0, 0, 0.01),
    "M_Cu": (0.015, 0.01, 0.02),
    "L_Cu": (0.06, 0.05, 0.07),
    "omega": (5.414, 5, 6)
}
params_pos = {
    "k_1": 1,
    "k_2": 2,
    "M": 3,
    "R": 4,
    "gamma": 5,
    "M_Cu": 6,
    "L_Cu": 7,
    "omega": 8
}

# 更新参数并持久化，然后调用 update_plot 更新图表
def update_data(param_name: str, current_param_value: float):
    current_data = init_Data.copy() # 重置
    current_data[params_pos[param_name]] = current_param_value # 将相应参数变更为对应值
    update_plot(current_data)

def update_plot(current_data):
    g = 9.81
    dt = 0.00001
    x_0 = 0
    y_0 = 0
    z_0 = 0.2
    L_bc0 = 0.107
    L_ab = 0.053
    L_ac = 0.161
    r = 0.0145
    theta = 1.36
    
    def I(R, M):
        return 0.5 * M * (R**2)

    def M(m, l):
        return m * g * l
    
    k_1, k_2, M_disk, R_disk, gamma, M_Cu, L_Cu, omiga = current_data[1:9]
    # I_disk = I(R_disk, M_disk)
    # I_Cu = M(M_Cu, L_Cu)
    I_Cu = 0.006997
    I_disk = 0.0001701
    xdata = []
    ydata = []
    for j in range(0, 2000000):
        #2000000
        x_0 += y_0 * dt
        y_0 += (
            (
                -1 * I_Cu * np.sin(x_0)
                + (k_1 + k_2) * (r**2) * (theta - x_0)
                + k_1
                * r
                * (np.sqrt(L_ab**2 + L_ac**2 - 2 * L_ac * L_ab * np.cos(z_0)) - L_bc0)
            )
            * dt
            / I_disk
        )
        z_0 -= dt * omiga
        #++-
        #--+
        xdata.append(x_0)
        ydata.append(y_0)
    line.set_xdata(xdata)
    line.set_ydata(ydata)
    ax.set_ylim(np.min(ydata), np.max(ydata))
    ax.set_xlim(np.min(xdata), np.max(xdata))
    fig.canvas.draw_idle()


plt.ion()
# 设置图形和滑动条区域
fig, ax = plt.subplots()
(line,) = ax.plot([], [])
fig.subplots_adjust(bottom=0.5)
axmodel = fig.add_axes([0.35, 0.2, 0.55, 0.03])  # 滑动条区域

# 初始化 SliderSelector
# 传入更新对应数据的回调函数 update_data
slider_selector = SliderSelector(fig, [0.35, 0.2, 0.55, 0.03], params_init, update_data)


# 初始显示第一个滑动条
slider_selector.create_slider(list(params_init.keys())[0])

# 定义滑动条模式和切换函数
mode = 1
mode_labels = list(params_init.keys())  # 模式对应的参数名称列表


def last_mode(event):
    """
    切换到上一个模式
    """
    global mode
    mode = (mode - 2) % len(mode_labels) + 1  # 循环减1模式
    slider_selector.update_slider(mode_labels[mode - 1])


def next_mode(event):
    """
    切换到下一个模式
    """
    global mode
    mode = mode % len(mode_labels) + 1  # 循环加1模式
    slider_selector.update_slider(mode_labels[mode - 1])


# 添加按钮
b1 = fig.add_axes([0.3, 0.05, 0.13, 0.05])
b2 = fig.add_axes([0.6, 0.05, 0.13, 0.05])
button1 = Button(b1, "Last Mode", hovercolor="0.975")
button2 = Button(b2, "Next Mode", hovercolor="0.975")
button1.on_clicked(last_mode)
button2.on_clicked(next_mode)


update_plot(init_Data)
# 显示图形
plt.draw()
plt.show()
# plt.pause(1000)