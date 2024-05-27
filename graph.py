import os
import random
import string

from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont

if not os.path.isdir("graphs"):
    os.mkdir("graphs")


data = {
    230: 205.3,
    227: 201.5,
    224: 204.4,
    220: 205.3,
    217: 207.5,
    213: 209.4,

    210: 212.7,
    206: 213.6,
    203: 215.1,
    200: 217.8,
    196: 219.9,
    193: 223.3,

    190: 215.4,
    185: 216.3,
    180: 220.6,
    176: 214.4,
    172: 221.4,
    167: 223.3,

    165: 226.5,
    162: 226.5,
    159: 225.1,
    156: 224.6,
    153: 221.7,
    150: 222.2,

    148: 221.4,
    144: 220.9,
    138: 219.6,
    135: 218.6,
    131: 216.8,
    126: 215.1,

    122: 212.7,
    117: 210.5
}


def get_corridor(data: dict, corridor: int = 5) -> tuple:
    print('get', data)
    results = []
    data_list = list(data.items())
    for k, i in enumerate(data_list):
        results.append([])
        for j in data_list[k:]:
            if not results[-1]:
                results[-1].append(j)
                continue
            temp = results[-1].copy()
            temp.append(j)
            if 0 < max(temp, key=lambda x: x[1])[1] - \
                    min(temp, key=lambda x: x[1])[1] < corridor:
                results[-1].append(j)
            else:
                break

    best_result = max(results, key=lambda x: len(x))
    only_speed = [i[1] for i in best_result]
    only_pressure = [i[0] for i in best_result]
    # if corridor in (2, 3, 4):
    #     print(f'Результат для {corridor}\'х метрового коридора')
    # else:
    #     print(f'Результат для {corridor}\'ти метрового коридора')
    # print(f'Значение скоростей: {", ".join(map(str, only_speed))}')
    # print(f'Средняя скорость: {round(sum(only_speed) / len(only_speed), 1)}')
    # print(f'Давление: {", ".join(map(str, only_pressure))}')
    # print(f'Кол-во выстрелов: {len(best_result)}')
    return only_speed, only_pressure


def draw_graph(data, speed5, pressure5, speed10, pressure10, reverse=False):
    plt.plot(data.keys(), data.values(), marker='o', markersize=5)
    plt.plot([pressure5[-1] - 2, pressure5[0] + 2],
             [min(speed5) - 0.3, min(speed5) - 0.3], color='green',
             label='Пяти метровый коридор')  # Низ

    plt.plot([pressure5[-1] - 2, pressure5[0] + 2],
             [max(speed5) + 0.3, max(speed5) + 0.3], color='green')  # Верх

    plt.plot([pressure5[-1] - 2, pressure5[-1] - 2],
             [min(speed5) - 0.3, max(speed5) + 0.3], color='green')  # Лево

    plt.plot([pressure5[0] + 2, pressure5[0] + 2],
             [min(speed5) - 0.3, max(speed5) + 0.3], color='green')  # Право

    plt.plot([pressure10[-1] - 3, pressure10[0] + 3],
             [min(speed10) - 0.5, min(speed10) - 0.5], color='orange',
             label='Десяти метровый коридор')  # Низ

    plt.plot([pressure10[-1] - 3, pressure10[0] + 3],
             [max(speed10) + 0.5, max(speed10) + 0.5], color='orange')  # Верх

    plt.plot([pressure10[-1] - 3, pressure10[-1] - 3],
             [min(speed10) - 0.5, max(speed10) + 0.5], color='orange')  # Лево

    plt.plot([pressure10[0] + 3, pressure10[0] + 3],
             [min(speed10) - 0.5, max(speed10) + 0.5], color='orange')  # Право

    plt.xlabel('Давление')
    plt.ylabel('Скорость')
    plt.title('График скоростей')
    if reverse:
        plt.gca().invert_xaxis()

    plt.legend()
    img = f'{"".join([random.choice(string.ascii_lowercase) for _ in range(12)])}.png'
    plt.savefig(img)
    plt.ioff()
    plt.close()
    return img


def get_graph(data, reverse=False):
    speed5, pressure5 = get_corridor(data)
    speed10, pressure10 = get_corridor(data, 10)

    # Открываем изображение
    graph_img = draw_graph(data, speed5, pressure5, speed10, pressure10, reverse)
    image = Image.open(graph_img)

    # Получаем размеры изображения
    width, height = image.size

    # Создаем новое изображение с белым фоном
    new_height = height + 310  # Добавляем 200 пикселей снизу
    new_image = Image.new("RGB", (width, new_height), color="white")

    # Вставляем исходное изображение в новое изображение
    new_image.paste(image, (0, 0))

    # Создаем объект для рисования на изображении
    draw = ImageDraw.Draw(new_image)

    # Загружаем шрифт
    font = ImageFont.truetype('arial.ttf', 20)

    # Текст для 5-метрового коридора
    text1 = f"""Результат для 5'ти метрового коридора:
        Значение скоростей: {min(speed5)} - {max(speed5)}
        Средняя скорость: {round(sum(speed5) / len(speed5), 1)}
        Давление: {pressure5[-1]} - {pressure5[0]}
        Кол-во выстрелов: {len(speed5)}
        """
    draw.textbbox((0, 0), text1, font)
    draw.text((20, height + 20), text1, font=font, fill="black")

    # Текст для 10-метрового коридора
    text2 = f"""\nРезультат для 10'ти метрового коридора:
        Значение скоростей: {min(speed10)} - {max(speed10)}
        Средняя скорость: {round(sum(speed10) / len(speed10), 1)}
        Давление: {pressure10[-1]} - {pressure10[0]}
        Кол-во выстрелов: {len(speed10)}
        """
    draw.textbbox((0, 0), text2, font)
    draw.text((20, height + 150), text2, font=font, fill="black")

    # Сохраняем новое изображение
    img = f'{"".join([random.choice(string.ascii_lowercase) for _ in range(12)])}.png'
    new_image.save('graphs/' + img)

    os.remove(graph_img)

    return img


if __name__ == '__main__':
    get_graph(data)
