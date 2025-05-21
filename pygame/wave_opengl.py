import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

# =============================================
# ВЕРШИННЫЙ ШЕЙДЕР (обработка геометрии)
# =============================================
vertex_shader = """
#version 330 core
layout (location = 0) in vec2 position;    // Позиция вершины (X, Y)
layout (location = 1) in vec2 texCoord;    // Текстурные координаты (U, V)

out vec2 uv;  // Передаем текстурные координаты во фрагментный шейдер

void main() {
    gl_Position = vec4(position, 0.0, 1.0); // Проецируем вершину как есть
    uv = texCoord;                         // Просто передаем UV-координаты
}
"""

# =============================================
# ФРАГМЕНТНЫЙ ШЕЙДЕР (эффект волн)
# =============================================
fragment_shader = """
#version 330 core
in vec2 uv;                // Текстурные координаты от вершинного шейдера
out vec4 FragColor;        // Итоговый цвет пикселя

uniform sampler2D texture0; // Текстура фона
uniform vec2 u_resolution;  // Размер окна (для преобразования координат)
uniform vec4 waves[10];     // Массив волн: x, y, radius, time для каждой
uniform int wave_count;     // Активное количество волн

void main() {
    vec2 coord = uv;       // Исходные координаты текстуры
    float distortion = 0.0; // Накопленное искажение

    // Проходим по всем активным волнам
    for(int i = 0; i < wave_count; i++) {
        vec2 center = waves[i].xy;    // Центр волны в UV-координатах
        float radius = waves[i].z;    // Текущий радиус волны
        float time = waves[i].w;      // Время жизни (0.0-1.0)

        // Расстояние от текущего пикселя до центра волны
        float distance = length(center - coord);

        // Если пиксель в зоне действия волны
        if (distance < radius) {
            // Затухание эффекта к краю волны (1 в центре, 0 на краю)
            float falloff = 1.0 - smoothstep(0.0, radius, distance);

            // Волновая функция (синусоидальная форма)
            float wave = sin((distance / radius) * 3.141592 * 2.0);

            // Накопление искажения с учетом времени жизни волны
            distortion += wave * falloff * time;
        }
    }

    // Применяем искажение к координатам текстуры
    coord += distortion * 0.02; // Множитель силы эффекта

    // Получаем цвет из текстуры с искаженными координатами
    FragColor = texture(texture0, coord);
}
"""


class WaveEffect:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.waves = []  # Список активных волн
        self.max_waves = 10  # Максимум одновременно отображаемых волн

        # Инициализация OpenGL контекста через Pygame
        pygame.init()
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        glEnable(GL_TEXTURE_2D)

        # Компиляция шейдерной программы
        self.shader = compileProgram(
            compileShader(vertex_shader, GL_VERTEX_SHADER),
            compileShader(fragment_shader, GL_FRAGMENT_SHADER)
        )

        # =============================================
        # НАСТРОЙКА ГЕОМЕТРИИ (квадрат на весь экран)
        # =============================================
        # Вершины: X, Y, U, V
        vertices = np.array([
            # Позиции       # UV-координаты
            -1, -1, 0, 0,  # Левый нижний угол
            1, -1, 1, 0,  # Правый нижний
            1, 1, 1, 1,  # Правый верхний
            -1, 1, 0, 1  # Левый верхний
        ], dtype=np.float32)

        # Создание Vertex Array Object (VAO) и Vertex Buffer Object (VBO)
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Настройка атрибутов вершин
        # Атрибут 0: Позиция (X, Y)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        # Атрибут 1: Текстурные координаты (U, V)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(8))
        glEnableVertexAttribArray(1)

        # =============================================
        # ЗАГРУЗКА ТЕКСТУРЫ
        # =============================================
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        # Настройка параметров текстуры
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Создание тестовой текстуры (шахматная доска)
        texture_data = np.zeros((512, 512, 3), dtype=np.uint8)
        texture_data[::32, :] = [255, 255, 255]  # Горизонтальные линии
        texture_data[:, ::32] = [255, 255, 255]  # Вертикальные линии
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)

    def add_wave(self, pos):
        """Добавление новой волны в позиции клика мыши"""
        if len(self.waves) >= self.max_waves:
            self.waves.pop(0)  # Удаляем старую волну если достигли максимума

        # Преобразование экранных координат в UV-координаты текстуры
        # X: [0, width] -> [0.0, 1.0]
        # Y: инвертируем, так как в OpenGL ось Y направлена вверх
        x = pos[0] / self.width
        y = 1.0 - pos[1] / self.height
        # Новая волна: (X, Y, начальный радиус, время жизни)
        self.waves.append((x, y, 0.0, 1.0))

    def update(self, dt):
        """Обновление параметров волн"""
        # Идем в обратном порядке для безопасного удаления
        for i in reversed(range(len(self.waves))):
            wave = list(self.waves[i])
            wave[2] += dt * 0.5  # Увеличиваем радиус волны
            wave[3] -= dt * 2.0  # Уменьшаем время жизни

            # Если время жизни закончилось - удаляем волну
            if wave[3] <= 0:
                self.waves.pop(i)
            else:
                self.waves[i] = tuple(wave)

    def render(self):
        """Отрисовка кадра с эффектом"""
        glUseProgram(self.shader)

        # Передаем разрешение экрана в шейдер
        glUniform2f(glGetUniformLocation(self.shader, "u_resolution"), self.width, self.height)

        # Подготавливаем данные волн для шейдера
        wave_data = []
        for wave in self.waves:
            wave_data.extend(wave)  # Разворачиваем в плоский список

        # Дополняем массив до максимального размера нулями
        while len(wave_data) < 4 * self.max_waves:
            wave_data.extend([0.0, 0.0, 0.0, 0.0])

        # Передаем массив волн в шейдер
        glUniform4fv(glGetUniformLocation(self.shader, "waves"), self.max_waves, wave_data)
        # Передаем количество активных волн
        glUniform1i(glGetUniformLocation(self.shader, "wave_count"), len(self.waves))

        # Привязываем текстуру
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glUniform1i(glGetUniformLocation(self.shader, "texture0"), 0)

        # Отрисовываем полноэкранный квад
        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, 4)

    def run(self):
        """Главный цикл приложения"""
        clock = pygame.time.Clock()
        running = True
        while running:
            dt = clock.tick(60) / 1000.0  # Дельта-время в секундах

            # Обработка событий
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    self.add_wave(event.pos)  # Добавляем волну при клике

            # Очистка буфера и рендеринг
            glClear(GL_COLOR_BUFFER_BIT)
            self.update(dt)
            self.render()
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    app = WaveEffect(800, 600)
    app.run()